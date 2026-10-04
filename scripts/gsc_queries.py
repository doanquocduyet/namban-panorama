#!/usr/bin/env python3
"""
Đọc từ khoá · vị trí · lượt hiện · lượt bấm từ Google Search Console (Search Analytics API),
so với kỳ trước, ghi báo cáo docs/gsc-queries.md và lưu ảnh chụp docs/gsc/queries-<ngày>.json.

Chạy cùng workflow gsc-report.yml (thứ Hai hằng tuần), dùng chung secret GSC_SA_JSON.
- Cửa sổ: 28 ngày gần nhất (lùi 3 ngày vì GSC trễ dữ liệu) so với 28 ngày liền trước.
  Panorama còn ít lượt hiện nên 7 ngày quá thưa, so tuần với tuần chỉ ra nhiễu.
- "Sắp lên trang 1" = từ khoá đang ở vị trí 11–20, xếp theo lượt hiện.
docs/ không lên web (.vercelignore).
Không có GSC_SA_JSON → thoát êm.
"""
import os, json, sys, datetime

SA = os.environ.get("GSC_SA_JSON", "").strip()
WANT = os.environ.get("GSC_SITE", "sc-domain:nambanpanorama.com").strip()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://searchconsole.googleapis.com/webmasters/v3"
DOMAIN = "https://nambanpanorama.com"
MIN_IMP = 5          # ngưỡng lượt hiện để tính lên/xuống — dưới mức này vị trí nhảy lung tung
WINDOW = 28


def log(*a): print(*a, flush=True)


if not SA:
    log("Chưa có GSC_SA_JSON — bỏ qua.")
    sys.exit(0)

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from urllib.parse import quote


def pick_site(sess):
    r = sess.get(f"{API}/sites", timeout=60)
    r.raise_for_status()
    sites = [e["siteUrl"] for e in r.json().get("siteEntry", []) if "nambanpanorama.com" in e.get("siteUrl", "")]
    if not sites:
        return None
    if WANT in sites:
        return WANT
    dom = [s for s in sites if s.startswith("sc-domain:")]
    return (dom or sites)[0]


def query(sess, site, start, end, dims):
    rows, start_row = [], 0
    while True:
        body = {"startDate": start.isoformat(), "endDate": end.isoformat(), "dimensions": dims,
                "rowLimit": 25000, "startRow": start_row, "dataState": "final"}
        r = sess.post(f"{API}/sites/{quote(site, safe='')}/searchAnalytics/query", json=body, timeout=120)
        r.raise_for_status()
        got = r.json().get("rows", [])
        rows += got
        if len(got) < 25000:
            return rows
        start_row += 25000


def short(url):
    return url.replace(DOMAIN, "") or "/"


def by_query(rows):
    """Gộp dòng query×page thành query: tổng hiện/bấm, vị trí trung bình có trọng số, trang nhận nhiều lượt hiện nhất."""
    out = {}
    for r in rows:
        q, p = r["keys"]
        d = out.setdefault(q, {"clicks": 0, "imp": 0, "posw": 0.0, "pages": {}})
        d["clicks"] += r["clicks"]
        d["imp"] += r["impressions"]
        d["posw"] += r["position"] * r["impressions"]
        d["pages"][p] = d["pages"].get(p, 0) + r["impressions"]
    for d in out.values():
        d["pos"] = round(d["posw"] / d["imp"], 1) if d["imp"] else None
        d["page"] = short(max(d["pages"], key=d["pages"].get))
        d["n_pages"] = len(d["pages"])
        del d["posw"], d["pages"]
    return out


def totals(rows):
    c = sum(r["clicks"] for r in rows)
    i = sum(r["impressions"] for r in rows)
    p = sum(r["position"] * r["impressions"] for r in rows) / i if i else 0
    return c, i, round(p, 1)


def fmt_delta(cur, prev, lower_is_better=False):
    if prev is None:
        return "mới"
    d = round(cur - prev, 1)
    if d == 0:
        return "="
    good = d < 0 if lower_is_better else d > 0
    arrow = "↑" if good else "↓"
    return f"{arrow} {abs(d):g}"


def main():
    info = json.loads(SA)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    sess = AuthorizedSession(creds)
    site = pick_site(sess)
    if not site:
        log("Service account chưa có quyền trên nambanpanorama.com — bỏ qua (xem docs/gsc-status.md).")
        sys.exit(0)

    end = datetime.date.today() - datetime.timedelta(days=3)
    start = end - datetime.timedelta(days=WINDOW - 1)
    pend = start - datetime.timedelta(days=1)
    pstart = pend - datetime.timedelta(days=WINDOW - 1)
    log(f"Property {site} · kỳ này {start}→{end} · kỳ trước {pstart}→{pend}")

    cur_rows = query(sess, site, start, end, ["query", "page"])
    prev_rows = query(sess, site, pstart, pend, ["query", "page"])
    page_rows = query(sess, site, start, end, ["page"])
    prev_page_rows = query(sess, site, pstart, pend, ["page"])
    cur, prev = by_query(cur_rows), by_query(prev_rows)
    # Tổng lấy theo trang: Google giấu các truy vấn hiếm (ẩn danh) khỏi bảng từ khoá, nên cộng từ khoá sẽ thiếu.
    tc, ti, tp = totals(page_rows)
    pc, pi, pp = totals(prev_page_rows)

    snap_dir = os.path.join(ROOT, "docs", "gsc")
    os.makedirs(snap_dir, exist_ok=True)
    snap = {"site": site, "start": start.isoformat(), "end": end.isoformat(),
            "totals": {"clicks": tc, "impressions": ti, "position": tp}, "queries": cur}
    json.dump(snap, open(os.path.join(snap_dir, f"queries-{end.isoformat()}.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=0, sort_keys=True)

    L = []
    L.append("# Từ khoá Google Search — Namban Panorama\n")
    L.append(f"Kỳ này **{start:%d/%m}–{end:%d/%m/%Y}** ({WINDOW} ngày) so với **{pstart:%d/%m}–{pend:%d/%m}**. "
             f"Property `{site}`. Số do bot đọc thẳng từ Search Console, không ước.\n")
    L.append("| | Kỳ này | Kỳ trước |\n|---|---|---|")
    L.append(f"| Lượt bấm | **{tc}** | {pc} |")
    L.append(f"| Lượt hiện | **{ti}** | {pi} |")
    L.append(f"| Vị trí trung bình | **{tp}** | {pp} |")
    L.append(f"| Số từ khoá có lượt hiện | **{len(cur)}** | {len(prev)} |\n")
    L.append("Tổng lượt bấm/lượt hiện tính theo trang. Bảng từ khoá bên dưới thiếu các truy vấn Google giấu vì quá hiếm.\n")

    def row(q, d):
        p = prev.get(q)
        return (f"| {q} | {d['pos']} | {fmt_delta(d['pos'], p['pos'] if p else None, lower_is_better=True)} "
                f"| {d['imp']} | {d['clicks']} | {d['page']}{' (+' + str(d['n_pages'] - 1) + ' trang)' if d['n_pages'] > 1 else ''} |")
    head = "| Từ khoá | Vị trí | So kỳ trước | Lượt hiện | Lượt bấm | Trang nhận |\n|---|---|---|---|---|---|"

    near = sorted([(q, d) for q, d in cur.items() if d["pos"] and 10.5 < d["pos"] <= 20.5],
                  key=lambda x: -x[1]["imp"])
    L.append("## Sắp lên trang 1 (vị trí 11–20)\n")
    L.append("Làm thêm một chút là lên trang 1. Xếp theo lượt hiện, nhiều nhất trước.\n")
    L.append(head)
    L += [row(q, d) for q, d in near[:40]] or ["| — | | | | | |"]

    top = sorted(cur.items(), key=lambda x: -x[1]["imp"])[:50]
    L.append("\n## 50 từ khoá nhiều lượt hiện nhất\n")
    L.append(head)
    L += [row(q, d) for q, d in top]

    moved = []
    for q, d in cur.items():
        p = prev.get(q)
        if p and d["imp"] >= MIN_IMP and p["imp"] >= MIN_IMP and d["pos"] and p["pos"]:
            moved.append((round(p["pos"] - d["pos"], 1), q, d, p))
    up = sorted([m for m in moved if m[0] >= 2], key=lambda x: -x[0])[:15]
    down = sorted([m for m in moved if m[0] <= -2], key=lambda x: x[0])[:15]
    L.append(f"\n## Lên mạnh nhất (≥ 2 bậc, cả hai kỳ ≥ {MIN_IMP} lượt hiện)\n")
    L.append(head)
    L += [row(q, d) for _, q, d, _ in up] or ["| — | | | | | |"]
    L.append(f"\n## Xuống mạnh nhất (≥ 2 bậc, cả hai kỳ ≥ {MIN_IMP} lượt hiện)\n")
    L.append(head)
    L += [row(q, d) for _, q, d, _ in down] or ["| — | | | | | |"]

    multi = sorted([(q, d) for q, d in cur.items() if d["n_pages"] > 1 and d["imp"] >= MIN_IMP],
                   key=lambda x: -x[1]["imp"])[:20]
    L.append("\n## Một từ khoá, nhiều trang Panorama cùng hiện (soi xem có tự giành chỗ không)\n")
    L.append(head)
    L += [row(q, d) for q, d in multi] or ["| — | | | | | |"]

    pages = sorted(page_rows, key=lambda r: -r["impressions"])[:30]
    L.append("\n## 30 trang nhiều lượt hiện nhất\n")
    L.append("| Trang | Lượt hiện | Lượt bấm | Vị trí |\n|---|---|---|---|")
    L += [f"| {short(r['keys'][0])} | {r['impressions']} | {r['clicks']} | {round(r['position'], 1)} |" for r in pages]

    open(os.path.join(ROOT, "docs", "gsc-queries.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    log(f"Xong: {len(cur)} từ khoá, {ti} lượt hiện, {tc} lượt bấm, {len(near)} từ khoá ở vị trí 11–20 → docs/gsc-queries.md")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Không làm hỏng workflow báo cáo index nếu phần từ khoá lỗi
        log("Lỗi khi đọc Search Analytics:", str(e)[:300])
        sys.exit(0)
