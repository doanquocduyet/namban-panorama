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

def list_sites(sess):
    """Hỏi Google: service account này đang có quyền trên property nào?"""
    try:
        r = sess.get("https://searchconsole.googleapis.com/webmasters/v3/sites", timeout=60)
        if r.status_code != 200:
            return None, f"{r.status_code} — {str(r.text)[:200]}"
        entries = r.json().get("siteEntry", [])
        return entries, None
    except Exception as e:
        return None, str(e)[:200]

def pick_site(entries, want):
    """Chọn đúng property cho nambanpanorama.com từ danh sách SA thực sự có quyền."""
    match = [e for e in entries if "nambanpanorama.com" in e.get("siteUrl", "")]
    if not match:
        return None, match
    # ưu tiên đúng cái env yêu cầu (nếu SA có quyền), rồi tới sc-domain, rồi URL-prefix
    for e in match:
        if e.get("siteUrl") == want:
            return e, match
    for e in match:
        if e.get("siteUrl", "").startswith("sc-domain:"):
            return e, match
    return match[0], match

def write_config_error(client_email, entries, note):
    """Ghi báo cáo lỗi cấu hình quyền — hướng dẫn Chú thêm SA vào đúng property."""
    out = ["# Trạng thái index — Google Search Console\n",
           "## ⚠️ Chưa đọc được — service account thiếu quyền trên property\n",
           f"**Email service account cần cấp quyền:** `{client_email}`\n",
           note + "\n",
           "### Cách sửa (1 lần, ~1 phút)\n",
           "1. Vào https://search.google.com/search-console → chọn property **nambanpanorama.com**",
           "2. **Cài đặt** (bánh răng góc trái dưới) → **Người dùng và quyền** → **Thêm người dùng**",
           f"3. Dán email trên (`{client_email}`) → Quyền **Toàn quyền (Full)** → **Thêm**",
           "4. Actions → chạy lại workflow *Báo cáo index Google Search Console* (hoặc chờ em chạy).\n"]
    if entries is not None:
        out.append("### Property mà SA đang thấy (Google trả về)\n")
        if entries:
            for e in entries:
                out.append(f"- `{e.get('siteUrl')}` — quyền: {e.get('permissionLevel','?')}")
        else:
            out.append("- (trống) — SA chưa được thêm vào bất kỳ property nào.")
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    open(os.path.join(ROOT, "docs", "gsc-status.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    log("Lỗi cấu hình quyền — đã ghi hướng dẫn vào docs/gsc-status.md")

def main():
    global SITE
    info = json.loads(SA)
    client_email = info.get("client_email", "(không đọc được client_email)")
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    sess = AuthorizedSession(creds)

    # Bước 0: hỏi Google xem SA có quyền trên property nào → tự chọn đúng, khỏi đoán kiểu property
    entries, err = list_sites(sess)
    if entries is None:
        write_config_error(client_email, None,
            f"Không gọi được API danh sách property (lỗi: {err}). "
            "Thường do **Search Console API chưa bật** trong project Google Cloud "
            "(bật tại https://console.cloud.google.com/apis/library/searchconsole.googleapis.com).")
        sys.exit(0)
    chosen, match = pick_site(entries, SITE)
    if chosen is None:
        write_config_error(client_email, entries,
            f"SA xác thực OK nhưng **chưa được thêm vào property nambanpanorama.com**. "
            f"Google đang thấy SA có quyền trên {len(entries)} property (liệt kê dưới), "
            "không có cái nào là nambanpanorama.com.")
        sys.exit(0)
    SITE = chosen["siteUrl"]
    perm = chosen.get("permissionLevel", "?")
    log(f"Tự chọn property: {SITE} (quyền: {perm})")
    if perm not in ("siteOwner", "siteFullUser"):
        write_config_error(client_email, entries,
            f"SA đã có trong property `{SITE}` nhưng quyền là **{perm}** — "
            "URL Inspection API cần **Toàn quyền (Full)** hoặc **Chủ sở hữu (Owner)**. "
            "Vào GSC → Người dùng và quyền → sửa quyền của email SA thành **Toàn quyền**.")
        sys.exit(0)

    urls = sitemap_urls()
    log(f"Kiểm {len(urls)} URL trên property {SITE}")
    rows = []
    tally = {}
    err_samples = []   # (status, message) — để chẩn đoán
    for u in urls:
        body = {"inspectionUrl": u, "siteUrl": SITE, "languageCode": "vi-VN"}
        try:
            r = sess.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                          json=body, timeout=60)
            if r.status_code != 200:
                try: msg = r.json().get("error", {}).get("message", "")[:200]
                except Exception: msg = str(r.text)[:200]
                rows.append((u, "LỖI-API", f"{r.status_code} — {msg}", ""))
                if len(err_samples) < 1: err_samples.append((r.status_code, msg))
                # lỗi 403/401/400 là lỗi hệ thống (quyền/property) → dừng sớm, khỏi quét hết
                if r.status_code in (400, 401, 403) and len(rows) >= 3:
                    break
                continue
            res = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
            verdict = res.get("verdict", "?")                 # PASS / NEUTRAL / FAIL
            coverage = res.get("coverageState", "?")          # "Submitted and indexed" / "Crawled - currently not indexed" ...
            rows.append((u, verdict, coverage, res.get("lastCrawlTime", "")))
            tally[coverage] = tally.get(coverage, 0) + 1
        except Exception as e:
            rows.append((u, "LỖI", str(e)[:200], ""))
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
