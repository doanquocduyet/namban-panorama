#!/usr/bin/env python3
"""
Đọc từ khoá · vị trí · lượt hiện · lượt bấm từ Google Search Console (Search Analytics API)
cho Namban Panorama và Nam Ban Villas (cùng một service account), so với kỳ trước, rồi ghi vào
thư mục $GSC_OUT (mặc định ./gsc-out, KHÔNG nằm trong docs/):
  gsc-queries.md   — báo cáo Panorama
  gsc-villas.md    — báo cáo Villas (chỉ khi service account đã được cấp quyền property Villas)
  gsc-so-sanh.md   — bảng so 2 web theo từng từ khoá
  <web>-<ngày>.json — ảnh chụp số
Repo công khai nên workflow MÃ HOÁ cả thư mục này rồi mới commit (docs/gsc-private/*.enc).
Khoá mở nằm trong Google Drive của Chú — xem tools/gsc-decrypt.sh.
Chạy cùng workflow gsc-report.yml (thứ Hai hằng tuần), dùng chung secret GSC_SA_JSON.
- Cửa sổ: 28 ngày gần nhất (lùi 3 ngày vì GSC trễ dữ liệu) so với 28 ngày liền trước.
  Lượt hiện còn ít nên 7 ngày quá thưa, so tuần với tuần chỉ ra nhiễu.
- "Sắp lên trang 1" = vị trí trung bình 11–20, xếp theo lượt hiện.
Không có GSC_SA_JSON → thoát êm.
"""
import os, json, sys, datetime

SA = os.environ.get("GSC_SA_JSON", "").strip()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("GSC_OUT") or os.path.join(ROOT, "gsc-out")
API = "https://searchconsole.googleapis.com/webmasters/v3"
MIN_IMP = 5          # ngưỡng lượt hiện để tính lên/xuống — dưới mức này vị trí nhảy lung tung
WINDOW = 28
SITES = [
    {"key": "panorama", "name": "Namban Panorama", "host": "nambanpanorama.com",
     "want": os.environ.get("GSC_SITE", "sc-domain:nambanpanorama.com").strip(), "out": "gsc-queries.md"},
    {"key": "villas", "name": "Nam Ban Villas", "host": "nambanvillas.vn",
     "want": "sc-domain:nambanvillas.vn", "out": "gsc-villas.md"},
]


def log(*a): print(*a, flush=True)


if not SA:
    log("Chưa có GSC_SA_JSON — bỏ qua.")
    sys.exit(0)

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from urllib.parse import quote


def list_sites(sess):
    r = sess.get(f"{API}/sites", timeout=60)
    r.raise_for_status()
    return [e["siteUrl"] for e in r.json().get("siteEntry", [])]


def pick_site(all_sites, host, want):
    sites = [s for s in all_sites if host in s]
    if not sites:
        return None
    if want in sites:
        return want
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


def short(url, host):
    for pre in (f"https://{host}", f"https://www.{host}", f"http://{host}"):
        if url.startswith(pre):
            return url[len(pre):] or "/"
    return url


def by_query(rows, host):
    """Gộp dòng query×page thành query: tổng hiện/bấm, vị trí trung bình có trọng số, trang nhận nhiều lượt hiện nhất."""
    out = {}
    for r in rows:
        q, p = r["keys"]
        d = out.setdefault(q, {"clicks": 0, "imp": 0, "posw": 0.0, "pages": {}})
        d["clicks"] += r["clicks"]
        d["imp"] += r["impressions"]
        d["posw"] += r["position"] * r["impressions"]
        d["pages"][p] = {"imp": r["impressions"], "clicks": r["clicks"], "pos": round(r["position"], 1)}
    for d in out.values():
        d["pos"] = round(d["posw"] / d["imp"], 1) if d["imp"] else None
        d["page"] = short(max(d["pages"], key=lambda k: d["pages"][k]["imp"]), host)
        d["n_pages"] = len(d["pages"])
        # Giữ từng trang (để soi từ khoá nhiều trang cùng hiện: trang nào, vị trí bao nhiêu)
        d["by_page"] = {short(k, host): v for k, v in sorted(d["pages"].items(), key=lambda kv: -kv[1]["imp"])}
        del d["posw"], d["pages"]
    return out


def totals(rows):
    c = sum(r["clicks"] for r in rows)
    i = sum(r["impressions"] for r in rows)
    p = sum(r["position"] * r["impressions"] for r in rows) / i if i else 0
    return c, i, round(p, 1)


def fmt_delta(cur, prev):
    """Vị trí: số nhỏ hơn là tốt hơn → ↑ khi tụt số."""
    if prev is None:
        return "mới"
    d = round(cur - prev, 1)
    if d == 0:
        return "="
    return f"{'↑' if d < 0 else '↓'} {abs(d):g}"


HEAD = "| Từ khoá | Vị trí | So kỳ trước | Lượt hiện | Lượt bấm | Trang nhận |\n|---|---|---|---|---|---|"
EMPTY = ["| — | | | | | |"]


def report(sess, cfg, site, win):
    start, end, pstart, pend = win
    host = cfg["host"]
    cur_rows = query(sess, site, start, end, ["query", "page"])
    prev_rows = query(sess, site, pstart, pend, ["query", "page"])
    page_rows = query(sess, site, start, end, ["page"])
    prev_page_rows = query(sess, site, pstart, pend, ["page"])
    cur, prev = by_query(cur_rows, host), by_query(prev_rows, host)
    # Tổng lấy theo trang: Google giấu các truy vấn hiếm (ẩn danh) khỏi bảng từ khoá, nên cộng từ khoá sẽ thiếu.
    tc, ti, tp = totals(page_rows)
    pc, pi, pp = totals(prev_page_rows)

    os.makedirs(OUT, exist_ok=True)
    json.dump({"site": site, "start": start.isoformat(), "end": end.isoformat(),
               "totals": {"clicks": tc, "impressions": ti, "position": tp}, "queries": cur},
              open(os.path.join(OUT, f"{cfg['key']}-{end.isoformat()}.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=0, sort_keys=True)

    def row(q, d):
        p = prev.get(q)
        more = f" (+{d['n_pages'] - 1} trang)" if d["n_pages"] > 1 else ""
        return (f"| {q} | {d['pos']} | {fmt_delta(d['pos'], p['pos'] if p else None)} "
                f"| {d['imp']} | {d['clicks']} | {d['page']}{more} |")

    L = [f"# Từ khoá Google Search — {cfg['name']}\n",
         f"Kỳ này **{start:%d/%m}–{end:%d/%m/%Y}** ({WINDOW} ngày) so với **{pstart:%d/%m}–{pend:%d/%m}**. "
         f"Property `{site}`. Số do bot đọc thẳng từ Search Console, không ước.\n",
         "| | Kỳ này | Kỳ trước |\n|---|---|---|",
         f"| Lượt bấm | **{tc}** | {pc} |",
         f"| Lượt hiện | **{ti}** | {pi} |",
         f"| Vị trí trung bình | **{tp}** | {pp} |",
         f"| Số từ khoá có lượt hiện | **{len(cur)}** | {len(prev)} |\n",
         "Tổng lượt bấm/lượt hiện tính theo trang. Bảng từ khoá bên dưới thiếu các truy vấn Google giấu vì quá hiếm.\n"]

    near = sorted([(q, d) for q, d in cur.items() if d["pos"] and 10.5 < d["pos"] <= 20.5], key=lambda x: -x[1]["imp"])
    L += ["## Sắp lên trang 1 (vị trí 11–20)\n", "Làm thêm một chút là lên trang 1. Xếp theo lượt hiện, nhiều nhất trước.\n", HEAD]
    L += [row(q, d) for q, d in near[:40]] or EMPTY

    L += ["\n## 50 từ khoá nhiều lượt hiện nhất\n", HEAD]
    L += [row(q, d) for q, d in sorted(cur.items(), key=lambda x: -x[1]["imp"])[:50]] or EMPTY

    moved = [(round(prev[q]["pos"] - d["pos"], 1), q, d) for q, d in cur.items()
             if q in prev and d["imp"] >= MIN_IMP and prev[q]["imp"] >= MIN_IMP and d["pos"] and prev[q]["pos"]]
    L += [f"\n## Lên mạnh nhất (≥ 2 bậc, cả hai kỳ ≥ {MIN_IMP} lượt hiện)\n", HEAD]
    L += [row(q, d) for _, q, d in sorted([m for m in moved if m[0] >= 2], key=lambda x: -x[0])[:15]] or EMPTY
    L += [f"\n## Xuống mạnh nhất (≥ 2 bậc, cả hai kỳ ≥ {MIN_IMP} lượt hiện)\n", HEAD]
    L += [row(q, d) for _, q, d in sorted([m for m in moved if m[0] <= -2], key=lambda x: x[0])[:15]] or EMPTY

    multi = sorted([(q, d) for q, d in cur.items() if d["n_pages"] > 1 and d["imp"] >= MIN_IMP], key=lambda x: -x[1]["imp"])[:20]
    L += [f"\n## Một từ khoá, nhiều trang của {cfg['name']} cùng hiện (soi xem có tự giành chỗ không)\n", HEAD]
    L += [row(q, d) for q, d in multi] or EMPTY
    for q, d in multi:
        L.append(f"\n**{q}** — từng trang:\n")
        L.append("| Trang | Vị trí | Lượt hiện | Lượt bấm |\n|---|---|---|---|")
        L += [f"| {pg} | {v['pos']} | {v['imp']} | {v['clicks']} |" for pg, v in d["by_page"].items()]

    L += ["\n## 30 trang nhiều lượt hiện nhất\n", "| Trang | Lượt hiện | Lượt bấm | Vị trí |\n|---|---|---|---|"]
    L += [f"| {short(r['keys'][0], host)} | {r['impressions']} | {r['clicks']} | {round(r['position'], 1)} |"
          for r in sorted(page_rows, key=lambda r: -r["impressions"])[:30]]

    open(os.path.join(OUT, cfg["out"]), "w", encoding="utf-8").write("\n".join(L) + "\n")
    log(f"{cfg['name']}: {len(cur)} từ khoá, {ti} lượt hiện, {tc} lượt bấm, {len(near)} ở vị trí 11–20 → {cfg['out']}")
    return cur


def compare(pano, vil, win):
    start, end = win[0], win[1]
    P1 = lambda d: d is not None and d["pos"] is not None and d["pos"] <= 10.5
    keys = set(pano) | set(vil)
    both, only_p, only_v, none = [], [], [], []
    for q in keys:
        p, v = pano.get(q), vil.get(q)
        imp = (p["imp"] if p else 0) + (v["imp"] if v else 0)
        item = (imp, q, p, v)
        if P1(p) and P1(v):
            both.append(item)
        elif P1(p):
            only_p.append(item)
        elif P1(v):
            only_v.append(item)
        else:
            none.append(item)

    def cell(d):
        return f"{d['pos']} · {d['imp']} hiện · {d['clicks']} bấm" if d else "không hiện"

    def table(items, n=40):
        out = ["| Từ khoá | Panorama | Villas | Tổng lượt hiện |", "|---|---|---|---|"]
        out += [f"| {q} | {cell(p)} | {cell(v)} | {imp} |" for imp, q, p, v in sorted(items, key=lambda x: -x[0])[:n]]
        return out if len(out) > 2 else out + ["| — | | | |"]

    L = ["# So 2 web theo từ khoá — Namban Panorama × Nam Ban Villas\n",
         f"Kỳ **{start:%d/%m}–{end:%d/%m/%Y}** ({WINDOW} ngày). \"Trang 1\" = vị trí trung bình ≤ 10. "
         "Ô ghi: vị trí · lượt hiện · lượt bấm. Chỉ tính từ khoá có lượt hiện ở ít nhất một web.\n",
         "| Nhóm | Số từ khoá |\n|---|---|",
         f"| Cả 2 web cùng trang 1 | **{len(both)}** |",
         f"| Chỉ Panorama trang 1 | **{len(only_p)}** |",
         f"| Chỉ Villas trang 1 | **{len(only_v)}** |",
         f"| Cả 2 chưa vào trang 1 | **{len(none)}** |\n",
         "## Cả 2 web cùng trang 1\n"] + table(both)
    L += ["\n## Chỉ Panorama trang 1 (Villas chưa có hoặc dưới trang 1)\n"] + table(only_p)
    L += ["\n## Chỉ Villas trang 1 (Panorama chưa có hoặc dưới trang 1)\n"] + table(only_v)
    L += ["\n## Cả 2 chưa vào trang 1 — xếp theo lượt hiện (chỗ trống lớn nhất ở trên)\n"] + table(none, 50)
    open(os.path.join(OUT, "gsc-so-sanh.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    log(f"So sánh: cả 2 trang 1 {len(both)} · chỉ Panorama {len(only_p)} · chỉ Villas {len(only_v)} · cả 2 chưa {len(none)} → gsc-so-sanh.md")


def main():
    info = json.loads(SA)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    sess = AuthorizedSession(creds)
    all_sites = list_sites(sess)
    end = datetime.date.today() - datetime.timedelta(days=3)
    start = end - datetime.timedelta(days=WINDOW - 1)
    pend = start - datetime.timedelta(days=1)
    pstart = pend - datetime.timedelta(days=WINDOW - 1)
    win = (start, end, pstart, pend)
    log(f"Kỳ này {start}→{end} · kỳ trước {pstart}→{pend} · SA thấy {len(all_sites)} property")

    res = {}
    for cfg in SITES:
        site = pick_site(all_sites, cfg["host"], cfg["want"])
        if not site:
            log(f"{cfg['name']}: service account chưa có quyền property {cfg['host']} — bỏ qua.")
            continue
        try:
            res[cfg["key"]] = report(sess, cfg, site, win)
        except Exception as e:
            log(f"{cfg['name']}: lỗi khi đọc Search Analytics:", str(e)[:300])
    if "panorama" in res and "villas" in res:
        compare(res["panorama"], res["villas"], win)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Không làm hỏng workflow báo cáo index nếu phần từ khoá lỗi
        log("Lỗi khi đọc Search Analytics:", str(e)[:300])
        sys.exit(0)
