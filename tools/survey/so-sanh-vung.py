#!/usr/bin/env python3
"""Lượt đo so sánh giá rao Tà Nung / Đà Lạt nội thành / Đà Lạt ven khác — BẢN CHẠY RIÊNG (phiếu 2/10/2026).

KHÔNG thay crawl.py / aggregate.py của Index (bộ quét Nam Ban hằng tuần giữ nguyên). File này nạp crawl.py như một
thư viện để dùng ĐÚNG các hàm đọc giá, diện tích, ngày, phân loại đất, rồi chỉ thay hai thứ:
  1. danh sách trang (theo vùng thay vì theo xã Nam Ban);
  2. bộ phân vùng (thay classify_khu của Nam Ban).
Nam Ban cùng ngày đo bằng chính crawl.py (workflow so-sanh-vung.yml chạy cả hai).

Chỉ lưu như crawl.py: nguồn, URL tin, ngày, vùng, loại, diện tích, giá. KHÔNG lưu tiêu đề, SĐT, tên người đăng.
Kết quả thô vào survey/out-vung/ (không lên repo); so-sanh-aggregate.py gộp thành tools/survey/so-sanh-da-lat-<ngày>.json.
"""
import os, re, sys, importlib.util, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("crawl", os.path.join(HERE, "crawl.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
C.OUT = "survey/out-vung"; os.makedirs(C.OUT, exist_ok=True)

DLX = "__DL__"  # ctx của danh sách cấp thành phố Đà Lạt: biết là Đà Lạt, chưa biết phường
TA_NUNG, NOI, NOI_RONG, VEN = "Tà Nung", "Đà Lạt nội thành (ghi rõ phường 1–12)", "Đà Lạt (chỉ ghi Đà Lạt, không nêu phường/xã)", "Đà Lạt ven khác (Xuân Thọ, Xuân Trường, Trạm Hành)"

def un(s):
    s = unicodedata.normalize("NFD", (s or "").lower().replace("đ", "d"))
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", s)

OUTER = ["nam ban", "lam ha", "dong thanh", "me linh", "gia lam", "nam ha", "phi to", "dinh van", "lac duong", "lang biang", "langbiang",
         "duc trong", "lien nghia", "hiep thanh", "don duong", "d ran", "bao loc", "di linh", "bao lam", "da huoai", "lam vien", "xuan huong", "cam ly"]
VEN_K = ["xuan tho", "xuan truong", "tram hanh", "cau dat", "loc quy"]

def region(title, addr, ctx):
    """addr ở đây = địa chỉ + đường dẫn tin (đường dẫn có tên phường/xã). Tên cũ cụ thể thắng ctx của trang danh sách."""
    t = " " + un((title or "") + " " + (addr or "")) + " "
    if " ta nung " in t: return TA_NUNG
    if any(" " + k + " " in t for k in VEN_K): return VEN
    m = re.search(r" (?:phuong|p) ?(1[0-2]|[1-9]) ", t)
    has_dl = " da lat " in t or " dalat " in t or ctx == DLX
    outer = [k for k in OUTER if " " + k + " " in t]
    if m and has_dl and not [k for k in outer if k not in ("lam vien", "xuan huong", "cam ly")]: return NOI
    if outer: return "ngoài vùng: " + outer[0]
    if ctx == DLX: return NOI_RONG
    if ctx: return ctx
    if has_dl: return NOI_RONG
    return "mơ hồ (không nêu nơi)"

C.classify_khu = region
_add = C.add_row
def add(src, url, title, addr, attrs, date, approx, area, ptot, pm2, ctx):
    _add(src, url, title, (addr or "") + " | " + url.replace("-", " ").replace("/", " "), attrs, date, approx, area, ptot, pm2, ctx)

TRANG = lambda b, p: b + ("&" if "?" in b else "?") + f"trang={p}"

def run_lists(src, host, lists, pat, detail, cap_total=900, pager=None, max_pages=30):
    seen = set()
    for base, ctx, cap in lists:
        links = C.paginate(src, base, pager or C.PAGE_VARIANTS[0], pat, host, max_pages=max_pages)
        C.log(f"[{src}] {base}: {len(links)} link")
        n = 0
        for u in links:
            if u in seen or n >= cap or len(seen) >= cap_total: continue
            seen.add(u); n += 1
            r = C.get(src, u)
            if r is None: continue
            soup = C.soup_of(r); C.st(src, "details")
            detail(src, u, soup, ctx)
        C.flush()

# ---------- chi tiết từng trang: chép nguyên từ crawl.py ----------
def d_guland(src, u, soup, ctx):
    title = C.text_of(soup.find("h1"))
    date, approx, ptot, pm2, area, addr, attrs = C.generic_detail(soup)
    e = soup.select_one(".dtl-prc__ttl")
    if e:
        v, un_ = C.parse_money(C.text_of(e))
        if un_ == "total": ptot = v
    e = soup.select_one(".dtl-prc__dtc")
    if e: area = C.parse_area(C.text_of(e)) or area
    for e in soup.select(".dtl-prc__sgl"):
        tx = C.text_of(e)
        if "/m" in tx and not pm2:
            v, un_ = C.parse_money(tx)
            if un_ == "per_m2": pm2 = v
    if not addr:
        m = re.search(r"(xã|thị trấn|phường)\s+[^,\-]{2,40}", title, re.I)
        if m: addr = m.group(0)
    add(src, u, title, addr, attrs, date, approx, area, ptot, pm2, ctx)

def d_bdsonline(src, u, soup, ctx):
    title = C.text_of(soup.find("h1"))
    date, approx, ptot, pm2, area, addr, attrs = C.generic_detail(soup)
    e = soup.select_one(".amount") or soup.select_one(".price")
    if e:
        v, un_ = C.parse_money(C.text_of(e))
        if un_ == "total": ptot = v
        elif un_ == "per_m2": pm2 = v
    tx = C.text_of(soup)
    m = re.search(r"Diện tích\s*:\s*" + C.NUM + r"\s*m", tx, re.I)
    if m: area = C.parse_area(m.group(1) + " m2") or area
    m = re.search(r"Ngày đăng\s*:\s*(\d{1,2}/\d{1,2}/\d{4})", tx, re.I)
    if m: date, approx = C.parse_date(m.group(1))
    m = re.search(r"Địa chỉ\s*:\s*([^|]{3,80}?)(Lâm Đồng|$)", tx, re.I)
    if m: addr = m.group(1) + " Lâm Đồng"
    add(src, u, title, addr, attrs, date, approx, area, ptot, pm2, ctx)

def d_tvnd(src, u, soup, ctx):
    title = C.text_of(soup.find("h1"))
    date, approx, ptot, pm2, area, addr, attrs = C.generic_detail(soup)
    tx = C.text_of(soup)
    m = re.search(r"Diện tích\s*" + C.NUM + r"\s*m", tx, re.I)
    if m: area = C.parse_area(m.group(1) + " m2") or area
    m = re.search(r"Mức giá\s*([^\n]{0,20}?(tỷ|triệu))", tx, re.I)
    if m and not ptot:
        v, un_ = C.parse_money(m.group(1))
        if un_ == "total": ptot = v
    add(src, u, title, addr, attrs, date, approx, area, ptot, pm2, ctx)

def d_mogi(src, u, soup, ctx):
    title = C.text_of(soup.find("h1"))
    date, approx, ptot, pm2, area, addr, attrs = C.generic_detail(soup)
    e = soup.select_one(".price")
    if e:
        v, un_ = C.parse_money(C.text_of(e))
        if un_ == "total": ptot = v
        elif un_ == "per_m2": pm2 = v
    tx = C.text_of(soup)
    m = re.search(r"Diện tích\s*(đất|sử dụng)?\s*:?\s*" + C.NUM + r"\s*m", tx, re.I)
    if m: area = C.parse_area(m.group(2) + " m2") or area
    m = re.search(r"Ngày đăng\s*(\d{1,2}/\d{1,2}/\d{4})", tx, re.I)
    if m: date, approx = C.parse_date(m.group(1))
    add(src, u, title, addr, attrs, date, approx, area, ptot, pm2, ctx)

# ---------- danh sách theo vùng ----------
# (trang, ctx mặc định nếu tin không tự nêu nơi, trần số tin đọc từ trang này)
DL = "thanh-pho-da-lat-lam-dong"
def s_guland():
    lists = [(f"https://guland.vn/mua-ban-bat-dong-san-xa-ta-nung-{DL}", TA_NUNG, 200),
             (f"https://guland.vn/mua-ban-bat-dong-san-xa-xuan-tho-{DL}", VEN, 150),
             (f"https://guland.vn/mua-ban-bat-dong-san-xa-xuan-truong-{DL}", VEN, 150),
             (f"https://guland.vn/mua-ban-bat-dong-san-xa-tram-hanh-{DL}", VEN, 150)]
    lists += [(f"https://guland.vn/mua-ban-bat-dong-san-phuong-{i}-{DL}", NOI, 45) for i in range(1, 13)]
    run_lists("guland.vn", "guland.vn", lists, r"/post/", d_guland, cap_total=1100, pager=lambda b, p: f"{b}?page={p}", max_pages=12)

def s_bdsonline():
    lists = [("https://batdongsanonline.vn/nha-dat-xa-ta-nung/", TA_NUNG, 200), ("https://batdongsanonline.vn/nha-dat-xa-xuan-tho/", VEN, 120),
             ("https://batdongsanonline.vn/nha-dat-xa-xuan-truong/", VEN, 120), ("https://batdongsanonline.vn/nha-dat-xa-tram-hanh/", VEN, 120)]
    lists += [(f"https://batdongsanonline.vn/nha-dat-phuong-{i}-da-lat/", DLX, 40) for i in range(1, 13)]
    run_lists("batdongsanonline.vn", "batdongsanonline.vn", lists, r"-\d{3,}/?$", d_bdsonline, max_pages=12)

def s_datnen():
    pat = r"datnenlamdong\.com\.vn/(?!ban-dat-|ban-nha-|cho-thue|tin-tuc|du-an|ban-do|page|trang)[a-z0-9-]{20,}/?$"
    lists = [("https://datnenlamdong.com.vn/ban-dat-xa-ta-nung/", TA_NUNG, 200), ("https://datnenlamdong.com.vn/ban-dat-xa-xuan-tho/", VEN, 120),
             ("https://datnenlamdong.com.vn/ban-dat-xa-xuan-truong/", VEN, 120), ("https://datnenlamdong.com.vn/ban-dat-xa-tram-hanh/", VEN, 120),
             ("https://datnenlamdong.com.vn/ban-dat-thanh-pho-da-lat/", DLX, 400)]
    run_lists("datnenlamdong.com.vn", "datnenlamdong.com.vn", lists, pat, d_bdsonline, max_pages=15)

def s_tvnd():
    lists = [("https://thuviennhadat.vn/ban-nha-dat-xa-ta-nung", TA_NUNG, 200), ("https://thuviennhadat.vn/ban-nha-dat-xa-xuan-tho", VEN, 120),
             ("https://thuviennhadat.vn/ban-nha-dat-xa-xuan-truong", VEN, 120), ("https://thuviennhadat.vn/ban-nha-dat-xa-tram-hanh", VEN, 120),
             ("https://thuviennhadat.vn/ban-nha-dat-thanh-pho-da-lat", DLX, 400)]
    run_lists("thuviennhadat.vn", "thuviennhadat.vn", lists, r"-pst\d+\.html", d_tvnd, pager=TRANG, max_pages=15)

def s_mogi():
    lists = [("https://mogi.vn/lam-dong/tp-da-lat/mua-dat", DLX, 300), ("https://mogi.vn/lam-dong/tp-da-lat/mua-nha-dat", DLX, 200)]
    run_lists("mogi.vn", "mogi.vn", lists, r"-id\d+", d_mogi, pager=lambda b, p: f"{b}?cp={p}", max_pages=10)

def s_muaban():
    """Chép khung src_muaban (đọc __NEXT_DATA__ của trang danh sách), đổi trang gốc sang Đà Lạt."""
    src = "muaban.net"; seen = set()
    for base in ["https://muaban.net/bat-dong-san/ban-dat-tp-da-lat-lam-dong", "https://muaban.net/bat-dong-san/tp-da-lat-lam-dong",
                 "https://muaban.net/bat-dong-san/ban-dat-xa-ta-nung-tp-da-lat-lam-dong"]:
        ctx = TA_NUNG if "ta-nung" in base else DLX
        for p in range(1, 10):
            url = base if p == 1 else f"{base}?page={p}"
            r = C.get(src, url)
            if r is None: break
            soup = C.soup_of(r); items = []
            nd = soup.find("script", id="__NEXT_DATA__")
            if nd:
                try:
                    import json
                    d = json.loads(nd.string)
                    def walk(o):
                        if isinstance(o, list) and o and isinstance(o[0], dict) and any(k in o[0] for k in ("price", "price_text", "priceText")) and any(k in o[0] for k in ("title", "name")):
                            items.extend(o); return
                        if isinstance(o, dict):
                            for v in o.values(): walk(v)
                        elif isinstance(o, list):
                            for v in o: walk(v)
                    walk(d)
                except Exception: pass
            if not items:
                for u in C.links_matching(soup, url, r"-id\d+", "muaban.net"): items.append({"url": u})
            new = 0
            for it in items:
                u = it.get("url") or it.get("link") or ""
                if u and not u.startswith("http"): u = C.urljoin("https://muaban.net/", u)
                if not u or u in seen: continue
                seen.add(u); new += 1
                title = it.get("title") or it.get("name") or ""
                addr = " ".join(str(it.get(k, "")) for k in ("ward", "ward_name", "district", "district_name", "address", "location", "area_name"))
                area = None; ptot = None; pm2 = None
                for k in ("area", "size", "acreage"):
                    if it.get(k):
                        try: area = float(str(it[k]).replace(",", ".")); break
                        except Exception: area = C.parse_area(str(it[k]) + " m2")
                for k in ("price", "price_text", "priceText"):
                    if it.get(k):
                        v, un_ = C.parse_money(str(it[k])) if not isinstance(it[k], (int, float)) else (float(it[k]), "total")
                        if un_ == "total": ptot = v
                        elif un_ == "per_m2": pm2 = v
                        break
                date, approx = C.parse_date(str(it.get("date") or it.get("created_at") or it.get("publish_date") or it.get("time") or ""))
                if not title or area is None or (ptot is None and pm2 is None) or date is None:
                    r2 = C.get(src, u)
                    if r2 is None: continue
                    s2 = C.soup_of(r2); C.st(src, "details")
                    title = title or C.text_of(s2.find("h1"))
                    d2, ap2, pt2, pm22, ar2, ad2, at2 = C.generic_detail(s2)
                    e = s2.select_one(".price")
                    if e:
                        v, un_ = C.parse_money(C.text_of(e))
                        if un_ == "total": pt2 = v
                    date = date or d2; approx = approx or ap2; ptot = ptot or pt2; pm2 = pm2 or pm22; area = area or ar2; addr = addr or ad2
                    m = re.search(C.NUM + r"\s*m²\s*\(", C.text_of(s2))
                    if m and not area: area = C.parse_area(m.group(1) + " m2")
                    bc = s2.find("nav") or s2.find(class_=re.compile("breadcrumb", re.I))
                    if bc: addr = (addr or "") + " " + C.text_of(bc)
                add(src, u, title, addr, "", date, approx, area, ptot, pm2, ctx)
            if new == 0: break
        C.flush()

SOURCES = {"guland": s_guland, "batdongsanonline": s_bdsonline, "datnenlamdong": s_datnen, "thuviennhadat": s_tvnd, "mogi": s_mogi, "muaban": s_muaban}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "all"
    C.SRC_NAME = "vung-" + name
    C.log(f"Bắt đầu so sánh vùng · nguồn={name}")
    for k, fn in SOURCES.items():
        if name not in ("all", k): continue
        try: fn()
        except Exception as e:
            import traceback; C.log("LỖI nguồn:", type(e).__name__, str(e)[:200]); C.log(traceback.format_exc()[-1500:])
        C.flush()
    C.flush(); C.log("XONG", len(C.ROWS), "dòng"); C.log(str(C.STATS))
    open(f"{C.OUT}/log-{C.SRC_NAME}.txt", "w", encoding="utf-8").write("\n".join(C.LOG))
