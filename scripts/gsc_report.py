#!/usr/bin/env python3
"""
Đọc trạng thái lập chỉ mục (index) của từng URL trong sitemap.xml qua Google
Search Console URL Inspection API, rồi ghi báo cáo docs/gsc-status.md.

Cần:
  - Secret GSC_SA_JSON : nội dung file JSON của service account (Google Cloud).
  - Biến GSC_SITE      : property trong GSC. Mặc định "sc-domain:nambanpanorama.com".
                         (Nếu Chú xác minh kiểu URL-prefix thì đặt "https://nambanpanorama.com/")

Nếu không có GSC_SA_JSON → script thoát êm (chưa cấu hình), KHÔNG lỗi.
"""
import os, json, re, sys, time, datetime

SA = os.environ.get("GSC_SA_JSON", "").strip()
SITE = os.environ.get("GSC_SITE", "sc-domain:nambanpanorama.com").strip()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def log(*a): print(*a, flush=True)

if not SA:
    log("Chưa có GSC_SA_JSON — bỏ qua (workflow chỉ chạy khi Chú đã thêm secret).")
    sys.exit(0)

try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
except Exception as e:
    log("Thiếu thư viện google-auth:", e); sys.exit(1)

def sitemap_urls():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    return re.findall(r"<loc>([^<]+)</loc>", s)

def main():
    info = json.loads(SA)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    sess = AuthorizedSession(creds)
    urls = sitemap_urls()
    log(f"Kiểm {len(urls)} URL trên property {SITE}")
    rows = []
    tally = {}
    for u in urls:
        body = {"inspectionUrl": u, "siteUrl": SITE, "languageCode": "vi-VN"}
        try:
            r = sess.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                          json=body, timeout=60)
            if r.status_code != 200:
                rows.append((u, "LỖI-API", r.status_code, str(r.text)[:120])); continue
            res = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
            verdict = res.get("verdict", "?")                 # PASS / NEUTRAL / FAIL
            coverage = res.get("coverageState", "?")          # "Submitted and indexed" / "Crawled - currently not indexed" ...
            rows.append((u, verdict, coverage, res.get("lastCrawlTime", "")))
            tally[coverage] = tally.get(coverage, 0) + 1
        except Exception as e:
            rows.append((u, "LỖI", "", str(e)[:120]))
        time.sleep(0.6)   # nhẹ tay với quota
    # ghi báo cáo
    now = os.environ.get("RUN_DATE", "") or "hôm nay"
    indexed = sum(1 for _,v,_,_ in rows if v == "PASS")
    out = []
    out.append(f"# Trạng thái index — Google Search Console\n")
    out.append(f"Cập nhật: {now} · Property: `{SITE}` · Tổng URL: {len(urls)} · **Đã index (PASS): {indexed}**\n")
    out.append("## Tổng hợp theo trạng thái\n")
    for k,v in sorted(tally.items(), key=lambda x:-x[1]):
        out.append(f"- **{v}** — {k}")
    out.append("\n## Trang CHƯA index (cần chú ý)\n")
    bad = [r for r in rows if r[1] != "PASS"]
    if not bad:
        out.append("Không có — tất cả URL trong sitemap đã index. 🎉")
    else:
        out.append("| URL | Verdict | Trạng thái |")
        out.append("|---|---|---|")
        for u,v,c,_ in bad:
            out.append(f"| {u.replace('https://nambanpanorama.com','')} | {v} | {c} |")
    os.makedirs(os.path.join(ROOT,"docs"), exist_ok=True)
    open(os.path.join(ROOT,"docs","gsc-status.md"),"w",encoding="utf-8").write("\n".join(out)+"\n")
    log(f"Xong. Đã index {indexed}/{len(urls)}. Chưa index: {len(bad)}. → docs/gsc-status.md")

if __name__ == "__main__":
    main()
