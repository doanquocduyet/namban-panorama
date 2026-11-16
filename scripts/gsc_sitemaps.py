#!/usr/bin/env python3
"""
Chẩn đoán nhanh phía Google (thêm 16/11/2026) → docs/gsc-sitemaps.md:

  1. Trạng thái sitemap trong Search Console (Sitemaps API): Google tải lần cuối khi nào,
     có lỗi/cảnh báo không, bao nhiêu URL được ghi nhận.
  2. Soi kỹ một danh sách ngắn URL ưu tiên (URL Inspection API): Google có biết URL không,
     đọc lần cuối khi nào, đọc bằng bot nào, tải trang ra sao, thấy URL nằm trong sitemap nào,
     có trang nào dẫn tới không.

Chạy nhanh (khoảng 1 phút), nên workflow gsc-report.yml chạy cả khi chỉ đọc từ khoá.
Dữ liệu ở đây là trạng thái trang, cùng loại với docs/gsc-status.md (không có từ khoá),
nên ghi thẳng ra file công khai. Không có GSC_SA_JSON → thoát êm.
"""
import os, sys, json, time, datetime
from urllib.parse import quote

SA = os.environ.get("GSC_SA_JSON", "").strip()
WANT = os.environ.get("GSC_SITE", "sc-domain:nambanpanorama.com").strip()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://nambanpanorama.com"

# Trang ưu tiên: trụ của phễu + trang Chú hỏi vì sao tìm không thấy. Sửa danh sách ở đây.
PRIORITY = [
    "/", "/nam-ban-la-gi", "/duong-di-nam-ban", "/da-lat-di-nam-ban", "/dat-gan-da-lat",
    "/nam-ban-hay-di-linh", "/nam-ban-hay-duc-trong", "/nam-ban-hay-lac-duong",
    "/nam-ban-hay-dran", "/nam-ban-hay-don-duong", "/thac-voi-nam-ban", "/namban-index",
    "/truoc-khi-xuong-tien", "/khi-hau-nam-ban", "/tach-thua-dat-nam-ban", "/nam-ban-co-gi",
]


def log(*a): print(*a, flush=True)


def day(x):
    return (x or "")[:10] or "chưa"


def main():
    if not SA:
        log("Chưa có GSC_SA_JSON — bỏ qua.")
        return 0
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    creds = service_account.Credentials.from_service_account_info(
        json.loads(SA), scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    sess = AuthorizedSession(creds)

    r = sess.get("https://searchconsole.googleapis.com/webmasters/v3/sites", timeout=60)
    if r.status_code != 200:
        log("Không đọc được danh sách property:", r.status_code, r.text[:200])
        return 0
    sites = [e.get("siteUrl", "") for e in r.json().get("siteEntry", [])
             if "nambanpanorama.com" in e.get("siteUrl", "")]
    if not sites:
        log("Service account chưa có quyền trên property nambanpanorama.com.")
        return 0
    site = WANT if WANT in sites else sorted(sites, key=lambda s: not s.startswith("sc-domain:"))[0]

    now = os.environ.get("RUN_DATE", "") or datetime.date.today().isoformat()
    out = ["# Sitemap và các trang ưu tiên — Google Search Console\n",
           f"Cập nhật: {now} · Property: `{site}`\n",
           "## Sitemap Google đang giữ\n"]

    r = sess.get(f"https://searchconsole.googleapis.com/webmasters/v3/sites/{quote(site, safe='')}/sitemaps",
                 timeout=60)
    if r.status_code != 200:
        out.append(f"Không đọc được danh sách sitemap ({r.status_code}).")
    else:
        maps = r.json().get("sitemap", [])
        if not maps:
            out.append("**Search Console chưa có sitemap nào được gửi cho property này.**")
        else:
            out += ["| Sitemap | Gửi lần cuối | Google tải lần cuối | Đang chờ | Lỗi | Cảnh báo | URL ghi nhận |",
                    "|---|---|---|---|---|---|---|"]
            for m in maps:
                cont = ", ".join(f"{c.get('type')}: {c.get('submitted', '?')}" for c in m.get("contents", [])) or "?"
                out.append(f"| {m.get('path', '').replace(BASE, '') or '/'} | {day(m.get('lastSubmitted'))} "
                           f"| {day(m.get('lastDownloaded'))} | {'có' if m.get('isPending') else 'không'} "
                           f"| {m.get('errors', 0)} | {m.get('warnings', 0)} | {cont} |")

    out += ["\n## Trang ưu tiên\n",
            "| URL | Trạng thái | Đọc lần cuối | Bot | Tải trang | robots.txt | Trong sitemap | Trang dẫn tới |",
            "|---|---|---|---|---|---|---|---|"]
    for path in PRIORITY:
        url = BASE + path
        try:
            r = sess.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                          json={"inspectionUrl": url, "siteUrl": site, "languageCode": "vi-VN"}, timeout=60)
            if r.status_code != 200:
                out.append(f"| {path} | LỖI API {r.status_code} | | | | | | |")
                continue
            x = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
            out.append(f"| {path} | {x.get('coverageState', '?')} | {day(x.get('lastCrawlTime'))} "
                       f"| {x.get('crawledAs', '—')} | {x.get('pageFetchState', '—')} "
                       f"| {x.get('robotsTxtState', '—')} | {len(x.get('sitemap', []))} "
                       f"| {len(x.get('referringUrls', []))} |")
        except Exception as e:
            out.append(f"| {path} | LỖI {str(e)[:80]} | | | | | | |")
        time.sleep(0.6)

    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    open(os.path.join(ROOT, "docs", "gsc-sitemaps.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    log("Xong → docs/gsc-sitemaps.md")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        # Không làm hỏng workflow báo cáo nếu phần chẩn đoán lỗi
        log("Lỗi khi đọc sitemap/URL ưu tiên:", str(e)[:300])
        sys.exit(0)
