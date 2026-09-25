#!/usr/bin/env python3
"""Thăm dò tin rao đất Nam Ban — bước 2: lấy số liệu từ các nguồn ĐÃ KIỂM robots.txt + điều khoản.

Chỉ lưu: nguồn, URL tin, ngày đăng (nếu có), ngày ghi nhận, khu, loại đất, diện tích,
giá rao cả lô, giá/m². KHÔNG lưu tiêu đề, mô tả, ảnh, số điện thoại, tên người đăng.
Tiêu đề/địa chỉ chỉ dùng trong bộ nhớ để phân loại khu + loại đất rồi bỏ.
Kết quả ghi vào survey/out/ (csv + json + log) — nhánh làm việc, không lên main.
"""
import re, sys, os, time, json, csv, hashlib, datetime as dt
from urllib import robotparser
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import warnings
try:
    from bs4 import XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
except Exception:
    pass

UA = "Mozilla/5.0 (compatible; NambanPanoramaResearch/1.0; +https://nambanpanorama.com/trao-doi)"
S = requests.Session(); S.headers.update({"User-Agent": UA, "Accept-Language": "vi,en;q=0.8"})
OUT = "survey/out"; os.makedirs(OUT, exist_ok=True)
TODAY = dt.date.today()
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

# ---------- fetch ----------
ROBOTS = {}
def robots(host):
    if host in ROBOTS: return ROBOTS[host]
    rp = robotparser.RobotFileParser()
    try:
        r = S.get(f"https://{host}/robots.txt", timeout=30)
        rp.parse(r.text.splitlines() if r.status_code == 200 else [])
    except Exception:
        rp.parse([])
    ROBOTS[host] = rp; return rp

STATS = {}
def st(src, k, n=1): STATS.setdefault(src, {}); STATS[src][k] = STATS[src].get(k, 0) + n

def get(src, url, delay=1.5):
    host = urlparse(url).netloc
    rp = robots(host)
    if not (rp.can_fetch("*", url) or rp.can_fetch(UA, url)):
        st(src, "robots_block"); log(f"  robots chặn: {url}"); return None
    time.sleep(delay)
    try:
        r = S.get(url, timeout=35, allow_redirects=True)
    except Exception as e:
        st(src, "fetch_err"); log(f"  lỗi fetch {url}: {type(e).__name__}"); return None
    st(src, "req")
    if r.status_code != 200:
        st(src, f"http_{r.status_code}"); log(f"  HTTP {r.status_code}: {url}"); return None
    return r

# ---------- parse helpers ----------
def _num(s):
    """'1.378,5' -> 1378.5 ; '5.919' -> 5919 ; '1,65' -> 1.65 ; '2.21' -> 2.21 ; '24.511' -> 24511"""
    s = s.strip().replace(" ", "")
    if "," in s and "." in s:
        # kiểu VN: chấm nghìn, phẩy thập phân
        return float(s.replace(".", "").replace(",", "."))
    if "," in s:
        a, b = s.split(",", 1)
        return float(a + "." + b) if len(b) != 3 or len(a) > 3 else float(a + b)  # 1,650 -> 1650 ; 1,65 -> 1.65
    if "." in s:
        a, b = s.rsplit(".", 1)
        if len(b) == 3 and len(a) <= 3 and "." not in a: return float(a + b)   # 5.919 -> 5919
        if "." in a: return float(s.replace(".", ""))                          # 1.234.567
        return float(s)                                                        # 2.21
    return float(s)

NUM = r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?|\d+(?:[.,]\d+)?)"

def parse_money(text):
    """Trả (giá_vnd, đơn vị) — đơn vị: total | per_m2 | per_sao | None. Lấy số tiền ĐẦU TIÊN rõ ràng."""
    if not text: return None, None
    t = text.lower().replace("\xa0", " ")
    if re.search(r"thỏa thuận|thoả thuận|liên hệ", t) and not re.search(r"tỷ|triệu|\btr\b", t): return None, None
    # 1 tỷ 350 triệu / 1 tỷ 3
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*tỷ\s*(\d{1,3})\s*(triệu|tr\b)?", t)
    if m and not re.search(r"tỷ\s*/", t):
        v = _num(m.group(1)) * 1e9 + float(m.group(2)) * (1e6 if (m.group(3) or len(m.group(2)) == 3) else 1e8)
        return v, "total"
    m = re.search(NUM + r"\s*(tỷ|ty|tỉ|triệu|trieu|tr)\b\s*(/\s*(m2|m²|m|sào|sao|1\.?000\s*m2|1\.?000\s*m²|nền|lô)|/m)?", t)
    if not m: return None, None
    raw = m.group(1); u = m.group(2); per = m.group(4) or ""
    if u in ("tỷ", "ty", "tỉ"):
        # đơn vị tỷ: dấu chấm hay phẩy đều là thập phân (1.599 tỷ = 1,599 tỷ)
        v = float(raw.replace(",", ".")) if raw.count(".") + raw.count(",") == 1 else _num(raw)
        v *= 1e9
    else:
        v = _num(raw) * 1e6
    if per:
        if re.search(r"m2|m²|^m$|/m", per) and not re.search(r"1\.?000", per): return v, "per_m2"
        if re.search(r"sào|sao|1\.?000", per): return v, "per_sao"
        return v, "total"  # /nền, /lô
    return v, "total"

def parse_area(text):
    """Trả m². Hiểu m², m2, sào (1.000 m² Tây Nguyên), ha."""
    if not text: return None
    t = text.lower().replace("\xa0", " ")
    m = re.search(NUM + r"\s*(m²|m2|mét vuông)", t) or re.search(r"(?:diện tích|dt)\s*:?\s*" + NUM + r"\s*m\b", t)
    if m:
        v = _num(m.group(1))
        if 10 <= v <= 500000: return v
    m = re.search(NUM + r"\s*(ha|héc ta|hecta)\b", t)
    if m:
        v = _num(m.group(1)) * 10000
        if 100 <= v <= 500000: return v
    m = re.search(NUM + r"\s*(sào|sao)\b", t)
    if m:
        v = _num(m.group(1)) * 1000
        if 100 <= v <= 500000: return v
    return None

def parse_date(text):
    """dd/mm/yyyy | yyyy-mm-dd | 'N giờ/ngày/tuần/tháng trước' | 'hôm qua'. Trả (date, approx)"""
    if not text: return None, False
    t = text.lower()
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", t)
    if m:
        try: return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))), False
        except ValueError: pass
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", t)
    if m:
        try: return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))), False
        except ValueError: pass
    m = re.search(r"(\d+)\s*(phút|giờ|ngày|tuần|tháng|năm)\s*trước", t)
    if m:
        n = int(m.group(1)); u = m.group(2)
        days = {"phút": 0, "giờ": 0, "ngày": n, "tuần": 7 * n, "tháng": 30 * n, "năm": 365 * n}[u]
        return TODAY - dt.timedelta(days=days), True
    if "hôm qua" in t: return TODAY - dt.timedelta(days=1), True
    if "hôm nay" in t or "vừa xong" in t: return TODAY, True
    return None, False

def strip_vn(s):
    return s.lower().replace("\xa0", " ")

EXCL = [("nam hà", "Nam Hà"), ("phi tô", "Phi Tô"), ("tà nung", "Tà Nung"), ("đinh văn", "Đinh Văn"), ("đạ đờn", "Đạ Đờn"),
        ("tân hà", "Tân Hà"), ("tân văn", "Tân Văn"), ("hoài đức", "Hoài Đức"), ("phúc thọ", "Phúc Thọ"), ("đan phượng", "Đan Phượng"),
        ("liên hà", "Liên Hà"), ("phú sơn", "Phú Sơn"), ("tân thanh", "Tân Thanh"), ("bảo lộc", "Bảo Lộc"), ("di linh", "Di Linh"),
        ("đức trọng", "Đức Trọng"), ("lạc dương", "Lạc Dương"), ("đơn dương", "Đơn Dương"), ("cam ly", "Cam Ly"), ("xuân trường", "Xuân Trường"), ("trại mát", "Trại Mát")]
INCL = [("đông thanh", "Đông Thanh"), ("dong thanh", "Đông Thanh"), ("mê linh", "Mê Linh"), ("buôn chuối", "Mê Linh"), ("gia lâm", "Gia Lâm"),
        ("nam ban", "Nam Ban"), ("thăng long", "Nam Ban"), ("chi lăng", "Nam Ban"), ("đông anh", "Nam Ban"), ("bãi công", "Nam Ban"),
        ("từ liêm", "Nam Ban"), ("thanh trì", "Nam Ban"), ("linh ẩn", "Nam Ban"), ("thác voi", "Nam Ban"), ("tổng đội", "Nam Ban"), ("ba đình", "Nam Ban"),
        ("hai bà trưng", "Nam Ban"), ("hoàn kiếm", "Nam Ban"), ("đống đa", "Nam Ban"), ("đt 725", "Nam Ban"), ("đt725", "Nam Ban"), ("tl725", "Nam Ban")]

def classify_khu(title, addr, ctx):
    """ctx: khu mặc định do trang danh sách (vd 'Nam Ban' khi lấy từ list thị trấn Nam Ban) hoặc None."""
    a = strip_vn(addr or ""); t = strip_vn(title or "")
    ex_a = [n for k, n in EXCL if k in a]; ex_t = [n for k, n in EXCL if k in t]
    in_a = [n for k, n in INCL if k in a]; in_t = [n for k, n in INCL if k in t]
    if ex_a: return "ngoài xã: " + ex_a[0]
    if in_a:
        # ưu tiên tên xã cụ thể hơn "Nam Ban" nếu cả hai
        spec = [x for x in in_a if x != "Nam Ban"]
        return spec[0] if spec else "Nam Ban"
    if ex_t and not in_t: return "ngoài xã: " + ex_t[0]
    if in_t and ex_t: return "mơ hồ (nhiều địa danh)"
    if in_t:
        spec = [x for x in in_t if x != "Nam Ban"]
        return spec[0] if spec else "Nam Ban"
    if ctx: return ctx
    return "mơ hồ (không nêu khu)"

def classify_type(title, attrs, area):
    t = strip_vn((title or "") + " " + (attrs or ""))
    house = re.search(r"(?<!xây )(?<!làm )(?<!hợp )(?<!dựng )nhà (cấp 4|cấp bốn|gỗ|vườn|riêng|mặt tiền|phố|\d tầng|mới|đẹp|kiên cố)|bán nhà|có nhà|sẵn nhà|căn nhà|biệt thự|villa|homestay|farmstay|khách sạn|căn hộ", t)
    if area is not None and area >= 2000: return "đất ≥2.000 m² (nông nghiệp / diện tích lớn)" + (" · có nhà" if house else "")
    if house: return "nhà / biệt thự"
    if re.search(r"đất nền dự án|dự án|phân lô|khu dân cư mới|kdc", t) and (area is None or area < 1500):
        return "đất nền dự án"
    if re.search(r"thổ cư|tho cu|đất ở|odt|ont|full thổ|có thổ|sẵn thổ|lên thổ", t): return "đất <2.000 m² có thổ cư"
    if re.search(r"nông nghiệp|cln|rẫy|cà phê|cafe|vườn|sào|nương", t): return "đất <2.000 m² nông nghiệp / vườn"
    return "đất <2.000 m² chưa rõ thổ cư"

def view_flag(title):
    t = strip_vn(title or "")
    if re.search(r"view hồ|view ho\b|hồ bãi công|hồ từ liêm|hồ đông thanh|hồ thanh trì|sát hồ|gần hồ|ven hồ|view toàn cảnh|toàn cảnh|panorama|view thung lũng|view đồi|view núi|view thông|săn mây", t): return "view"
    return ""

def h10(s): return hashlib.sha1(strip_vn(s or "").encode()).hexdigest()[:10]

ROWS = []
def add_row(src, url, title, addr, attrs, date, approx, area, price_total, price_m2, ctx):
    if area and price_total and not price_m2: price_m2 = price_total / area
    if area and price_m2 and not price_total: price_total = price_m2 * area
    khu = classify_khu(title, addr, ctx); typ = classify_type(title, attrs, area)
    if len(ROWS) % 20 == 19: flush()
    ROWS.append({"nguon": src, "url": url, "ngay_dang": date.isoformat() if date else "", "ngay_uoc": "1" if approx else "",
                 "ngay_ghi_nhan": TODAY.isoformat(), "khu": khu, "loai": typ, "view": view_flag(title),
                 "dien_tich_m2": round(area, 1) if area else "", "gia_ca_lo_vnd": int(price_total) if price_total else "",
                 "gia_m2_vnd": int(price_m2) if price_m2 else "", "ma_tin": h10(title)})
    st(src, "rows")

SRC_NAME = "all"
def flush():
    if not ROWS: return
    with open(f"{OUT}/tin-rao-{SRC_NAME}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(ROWS[0].keys())); w.writeheader(); w.writerows(ROWS)
    json.dump({"ngay": TODAY.isoformat(), "stats": STATS, "rows": len(ROWS)}, open(f"{OUT}/stats-{SRC_NAME}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(f"{OUT}/log-{SRC_NAME}.txt", "w", encoding="utf-8").write("\n".join(LOG))

def soup_of(r):
    return BeautifulSoup(r.text, "lxml") if r is not None else None

def text_of(el): return re.sub(r"\s+", " ", el.get_text(" ", strip=True)) if el else ""

def jsonld(soup):
    out = []
    for s in soup.find_all("script", type="application/ld+json"):
        try: out.append(json.loads(s.string or ""))
        except Exception: pass
    return out

def deep_find(obj, keys):
    """tìm giá trị đầu tiên của bất kỳ key nào trong cây JSON"""
    if isinstance(obj, dict):
        for k in keys:
            if k in obj and obj[k] not in (None, "", []): return obj[k]
        for v in obj.values():
            r = deep_find(v, keys)
            if r is not None: return r
    elif isinstance(obj, list):
        for v in obj:
            r = deep_find(v, keys)
            if r is not None: return r
    return None

def generic_detail(soup):
    """Trả (date, approx, price_total, price_m2, area, addr, attrs_text) từ JSON-LD + regex chung."""
    date = None; approx = False; ptot = None; pm2 = None; area = None; addr = ""; attrs = ""
    for d in jsonld(soup):
        dp = deep_find(d, ["datePosted", "datePublished", "dateCreated"])
        if dp and not date: date, approx = parse_date(str(dp))
        pr = deep_find(d, ["price"])
        if pr and not ptot:
            try:
                v = float(str(pr).replace(",", "").replace(".", "")) if not isinstance(pr, (int, float)) else float(pr)
                if 1e7 <= v <= 1e12: ptot = v
            except Exception: pass
        ad = deep_find(d, ["address"])
        if ad and not addr: addr = ad if isinstance(ad, str) else json.dumps(ad, ensure_ascii=False)
        fs = deep_find(d, ["floorSize", "area"])
        if fs and not area:
            area = parse_area(json.dumps(fs, ensure_ascii=False) + " m2") if isinstance(fs, dict) else parse_area(str(fs) + " m2")
    if not date:
        m = soup.find("meta", attrs={"property": "article:published_time"}) or soup.find("meta", attrs={"name": "pubdate"})
        if m and m.get("content"): date, approx = parse_date(m["content"])
    if not date:
        tm = soup.find("time", attrs={"datetime": True})
        if tm: date, approx = parse_date(tm["datetime"])
    body = text_of(soup)
    if not date:
        m = re.search(r"(ngày đăng|đăng ngày|đăng lúc|ngày cập nhật|cập nhật)\s*[:\-]?\s*([^\n]{0,40})", body, re.I)
        if m: date, approx = parse_date(m.group(2))
    m = re.search(r"(diện tích|dt)\s*[:\-]?\s*" + NUM + r"\s*(m²|m2|m\b)", body, re.I)
    if m and not area: area = parse_area(m.group(2) + " m2")
    m = re.search(r"(mức giá|giá bán|giá)\s*[:\-]?\s*([^\n]{0,30}?(tỷ|triệu|tr\b)[^\n]{0,12})", body, re.I)
    if m and not ptot:
        v, u = parse_money(m.group(2))
        if u == "total": ptot = v
        elif u == "per_m2": pm2 = v
        elif u == "per_sao": pm2 = v / 1000
    bc = soup.find(class_=re.compile(r"breadcrumb|crumb", re.I))
    if bc and not addr: addr = text_of(bc)
    return date, approx, ptot, pm2, area, addr, attrs

def links_matching(soup, base, pat, host):
    out, seen = [], set()
    for a in soup.find_all("a", href=True):
        u = urljoin(base, a["href"]).split("#")[0].split("?")[0]
        if re.search(pat, u) and host in urlparse(u).netloc and u not in seen and u.rstrip("/") != base.rstrip("/"):
            seen.add(u); out.append(u)
    return out

PAGE_VARIANTS = [lambda b, p: b.rstrip("/") + f"/trang/{p}/", lambda b, p: b.rstrip("/") + f"/page-{p}/",
                 lambda b, p: b.rstrip("/") + f"/trang--{p}.html", lambda b, p: b + ("&" if "?" in b else "?") + f"page={p}",
                 lambda b, p: b + ("&" if "?" in b else "?") + f"p={p}", lambda b, p: b + ("&" if "?" in b else "?") + f"cp={p}"]

def paginate(src, base, variants, pat, host, max_pages=30):
    """Duyệt trang 1..N, dừng khi không có link mới. variants: hàm page->url ưu tiên; nếu trang 2 không ra link mới thì thử các biến thể khác."""
    all_links, seen = [], set()
    r = get(src, base)
    if r is None: return all_links
    ls = links_matching(soup_of(r), base, pat, host)
    for u in ls: seen.add(u)
    all_links.extend(ls); st(src, "list_pages"); st(src, "links_page1", len(ls))
    if not ls: return all_links
    # tìm biến thể phân trang sống
    fn = None
    for cand in [variants] + [v for v in PAGE_VARIANTS if v is not variants]:
        url2 = cand(base, 2)
        r2 = get(src, url2)
        if r2 is None: continue
        ls2 = [u for u in links_matching(soup_of(r2), url2, pat, host) if u not in seen]
        if ls2:
            fn = cand; log(f"  phân trang: {url2} -> {len(ls2)} link mới")
            for u in ls2: seen.add(u)
            all_links.extend(ls2); st(src, "list_pages"); break
    if fn is None: log(f"  không tìm được cách phân trang cho {base} (chỉ lấy trang 1)"); return all_links
    for p in range(3, max_pages + 1):
        url = fn(base, p)
        r = get(src, url)
        if r is None: break
        ls = [u for u in links_matching(soup_of(r), url, pat, host) if u not in seen]
        if not ls: break
        for u in ls: seen.add(u)
        all_links.extend(ls); st(src, "list_pages")
    return all_links

# ---------- nguồn ----------
def src_guland():
    src = "guland.vn"; host = "guland.vn"
    lists = [("https://guland.vn/mua-ban-bat-dong-san-xa-nam-ban-lam-ha-lam-dong", None),
             ("https://guland.vn/mua-ban-bat-dong-san-thi-tran-nam-ban-huyen-lam-ha-lam-dong", "Nam Ban"),
             ("https://guland.vn/mua-ban-bat-dong-san-xa-dong-thanh-huyen-lam-ha-lam-dong", "Đông Thanh"),
             ("https://guland.vn/mua-ban-bat-dong-san-xa-me-linh-huyen-lam-ha-lam-dong", "Mê Linh"),
             ("https://guland.vn/mua-ban-bat-dong-san-xa-gia-lam-huyen-lam-ha-lam-dong", "Gia Lâm")]
    seen = set()
    for base, ctx in lists:
        links = paginate(src, base, lambda b, p: f"{b}?page={p}", r"/post/", host)
        log(f"[{src}] {base}: {len(links)} link")
        for u in links:
            if u in seen: continue
            seen.add(u)
            if len(seen) > 450: break
            r = get(src, u)
            if r is None: continue
            soup = soup_of(r); st(src, "details")
            title = text_of(soup.find("h1"))
            date, approx, ptot, pm2, area, addr, attrs = generic_detail(soup)
            e = soup.select_one(".dtl-prc__ttl");
            if e:
                v, un = parse_money(text_of(e));
                if un == "total": ptot = v
            e = soup.select_one(".dtl-prc__dtc")
            if e: area = parse_area(text_of(e)) or area
            for e in soup.select(".dtl-prc__sgl"):
                tx = text_of(e)
                if "/m" in tx and not pm2:
                    v, un = parse_money(tx)
                    if un == "per_m2": pm2 = v
            # địa chỉ: breadcrumb hoặc dòng "Xã ... Huyện ..." trong tiêu đề
            if not addr:
                m = re.search(r"(xã|thị trấn|phường)\s+[^,\-]{2,40}", title, re.I)
                if m: addr = m.group(0)
            add_row(src, u, title, addr, attrs, date, approx, area, ptot, pm2, ctx)

def src_bdsonline_like(src, host, lists, detail_pat):
    """batdongsanonline.vn và datnenlamdong.com.vn cùng một khung"""
    seen = set()
    for base, ctx in lists:
        links = paginate(src, base, PAGE_VARIANTS[0], detail_pat, host)
        log(f"[{src}] {base}: {len(links)} link")
        for u in links:
            if u in seen or "/tin-dang-thanh-vien-" in u: continue
            seen.add(u)
            if len(seen) > 520: break
            r = get(src, u)
            if r is None: continue
            soup = soup_of(r); st(src, "details")
            title = text_of(soup.find("h1"))
            date, approx, ptot, pm2, area, addr, attrs = generic_detail(soup)
            e = soup.select_one(".amount") or soup.select_one(".price")
            if e:
                v, un = parse_money(text_of(e))
                if un == "total": ptot = v
                elif un == "per_m2": pm2 = v
            m = re.search(r"Diện tích\s*:\s*" + NUM + r"\s*m", text_of(soup), re.I)
            if m: area = parse_area(m.group(1) + " m2") or area
            m = re.search(r"Ngày đăng\s*:\s*(\d{1,2}/\d{1,2}/\d{4})", text_of(soup), re.I)
            if m: date, approx = parse_date(m.group(1))
            # địa chỉ: dòng "Địa chỉ" hoặc breadcrumb
            m = re.search(r"Địa chỉ\s*:\s*([^|]{3,80}?)(Lâm Đồng|$)", text_of(soup), re.I)
            if m: addr = m.group(1) + " Lâm Đồng"
            add_row(src, u, title, addr, attrs, date, approx, area, ptot, pm2, ctx)

def src_thuviennhadat():
    src = "thuviennhadat.vn"; host = "thuviennhadat.vn"
    lists = [("https://thuviennhadat.vn/ban-dat-o-thi-tran-nam-ban", "Nam Ban"),
             ("https://thuviennhadat.vn/ban-nha-dat-thi-tran-nam-ban", "Nam Ban"),
             ("https://thuviennhadat.vn/ban-nha-dat-xa-dong-thanh", "Đông Thanh"),
             ("https://thuviennhadat.vn/ban-nha-dat-xa-me-linh", "Mê Linh"),
             ("https://thuviennhadat.vn/ban-nha-dat-xa-gia-lam", None)]
    seen = set()
    for base, ctx in lists:
        links = paginate(src, base, lambda b, p: f"{b}?p={p}", r"-pst\d+\.html", host)
        log(f"[{src}] {base}: {len(links)} link")
        for u in links:
            if u in seen: continue
            seen.add(u)
            if len(seen) > 300: break
            r = get(src, u)
            if r is None: continue
            soup = soup_of(r); st(src, "details")
            title = text_of(soup.find("h1"))
            date, approx, ptot, pm2, area, addr, attrs = generic_detail(soup)
            m = re.search(r"Diện tích\s*" + NUM + r"\s*m", text_of(soup), re.I)
            if m: area = parse_area(m.group(1) + " m2") or area
            m = re.search(r"Mức giá\s*([^\n]{0,20}?(tỷ|triệu))", text_of(soup), re.I)
            if m and not ptot:
                v, un = parse_money(m.group(1))
                if un == "total": ptot = v
            # trang Gia Lâm có thể là Gia Lâm Hà Nội -> kiểm địa chỉ
            if ctx is None and not re.search(r"lâm hà|lâm đồng", strip_vn(text_of(soup.find("h1")) + addr)):
                st(src, "skip_gia_lam_hn"); continue
            add_row(src, u, title, addr, attrs, date, approx, area, ptot, pm2, ctx if ctx else "Gia Lâm")

def src_muaban():
    src = "muaban.net"; host = "muaban.net"
    seen = set()
    for base in ["https://muaban.net/bat-dong-san/ban-dat-huyen-lam-ha-lam-dong", "https://muaban.net/bat-dong-san/huyen-lam-ha-lam-dong"]:
        for p in range(1, 8):
            url = base if p == 1 else f"{base}?page={p}"
            r = get(src, url)
            if r is None: break
            soup = soup_of(r)
            nd = soup.find("script", id="__NEXT_DATA__")
            items = []
            if nd:
                try:
                    d = json.loads(nd.string)
                    # tìm mảng có phần tử chứa 'price' và 'title'
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
                # fallback: link chi tiết
                for u in links_matching(soup, url, r"-id\d+", host):
                    items.append({"url": u})
            new = 0
            for it in items:
                u = it.get("url") or it.get("link") or ""
                if u and not u.startswith("http"): u = urljoin("https://muaban.net/", u)
                if not u or u in seen: continue
                seen.add(u); new += 1
                title = it.get("title") or it.get("name") or ""
                addr = " ".join(str(it.get(k, "")) for k in ("ward", "ward_name", "district", "district_name", "address", "location", "area_name"))
                area = None; ptot = None; pm2 = None
                for k in ("area", "size", "acreage"):
                    if it.get(k):
                        try: area = float(str(it[k]).replace(",", ".")); break
                        except Exception: area = parse_area(str(it[k]) + " m2")
                for k in ("price", "price_text", "priceText"):
                    if it.get(k):
                        v, un = parse_money(str(it[k])) if not isinstance(it[k], (int, float)) else (float(it[k]), "total")
                        if un == "total": ptot = v
                        elif un == "per_m2": pm2 = v
                        break
                date, approx = parse_date(str(it.get("date") or it.get("created_at") or it.get("publish_date") or it.get("time") or ""))
                if not title or area is None or (ptot is None and pm2 is None) or date is None:
                    r2 = get(src, u)
                    if r2 is None: continue
                    s2 = soup_of(r2); st(src, "details")
                    title = title or text_of(s2.find("h1"))
                    d2, ap2, pt2, pm22, ar2, ad2, at2 = generic_detail(s2)
                    e = s2.select_one(".price")
                    if e:
                        v, un = parse_money(text_of(e))
                        if un == "total": pt2 = v
                    date = date or d2; approx = approx or ap2; ptot = ptot or pt2; pm2 = pm2 or pm22; area = area or ar2; addr = addr or ad2
                    m = re.search(NUM + r"\s*m²\s*\(", text_of(s2))
                    if m and not area: area = parse_area(m.group(1) + " m2")
                    bc = s2.find("nav") or s2.find(class_=re.compile("breadcrumb", re.I))
                    if bc: addr = (addr or "") + " " + text_of(bc)
                add_row(src, u, title, addr, "", date, approx, area, ptot, pm2, None)
            if new == 0: break
            st(src, "list_pages")

def src_mogi():
    src = "mogi.vn"; host = "mogi.vn"
    seen = set()
    for base, ctx in [("https://mogi.vn/lam-dong/huyen-lam-ha/mua-dat", None), ("https://mogi.vn/lam-dong/huyen-lam-ha/mua-nha-dat", None)]:
        links = paginate(src, base, lambda b, p: f"{b}?cp={p}", r"-id\d+", host, max_pages=10)
        log(f"[{src}] {base}: {len(links)} link")
        for u in links:
            if u in seen: continue
            seen.add(u)
            if len(seen) > 200: break
            r = get(src, u)
            if r is None: continue
            soup = soup_of(r); st(src, "details")
            title = text_of(soup.find("h1"))
            date, approx, ptot, pm2, area, addr, attrs = generic_detail(soup)
            e = soup.select_one(".price")
            if e:
                v, un = parse_money(text_of(e))
                if un == "total": ptot = v
                elif un == "per_m2": pm2 = v
            m = re.search(r"Diện tích\s*(đất|sử dụng)?\s*:?\s*" + NUM + r"\s*m", text_of(soup), re.I)
            if m: area = parse_area(m.group(2) + " m2") or area
            m = re.search(r"Ngày đăng\s*(\d{1,2}/\d{1,2}/\d{4})", text_of(soup), re.I)
            if m: date, approx = parse_date(m.group(1))
            add_row(src, u, title, addr, attrs, date, approx, area, ptot, pm2, ctx)

def src_villas():
    src = "nambanvillas.vn"; host = "nambanvillas.vn"
    seen = set()
    for base in ["https://nambanvillas.vn/dat-nen-nam-ban/", "https://nambanvillas.vn/nha-ban-nam-ban/"]:
        r = get(src, base, delay=0.8)
        if r is None: continue
        soup = soup_of(r); st(src, "list_pages")
        cards = soup.select(".sp-title")
        log(f"[{src}] {base}: {len(cards)} thẻ")
        for h in cards:
            a = h.find("a", href=True) or (h.find_parent("a", href=True))
            card = h.find_parent(class_=re.compile(r"sp-|card|item")) or h.parent
            u = urljoin(base, a["href"]) if a else ""
            if not u:
                # tìm link trong khối cha
                pa = card.find("a", href=True) if card else None
                u = urljoin(base, pa["href"]) if pa else base + "#" + h10(text_of(h))
            if u in seen: continue
            seen.add(u)
            title = text_of(h)
            ptxt = text_of(card.select_one(".sp-price")) if card else ""
            atxt = text_of(card.select_one(".sp-area")) if card else ""
            chips = text_of(card.select_one(".sp-chips")) if card else ""
            if "&" in atxt or re.search(r"\d\s*&\s*\d", atxt): st(src, "skip_multi_lot"); continue  # nhiều lô một thẻ, bỏ
            area = parse_area(atxt) or parse_area(title)
            v, un = parse_money(ptxt)
            ptot = pm2 = None
            if un == "total": ptot = v
            elif un == "per_m2": pm2 = v
            elif un == "per_sao": pm2 = v / 1000
            if not ptot and not pm2:
                v, un = parse_money(chips)
                if un == "per_m2": pm2 = v
                elif un == "total": ptot = v
            date = None; approx = False; addr = ""
            if u.startswith("http") and "#" not in u:
                r2 = get(src, u, delay=0.8)
                if r2 is not None:
                    s2 = soup_of(r2); st(src, "details")
                    d2, ap2, pt2, pm22, ar2, ad2, at2 = generic_detail(s2)
                    date, approx, addr = d2, ap2, ad2
                    ptot = ptot or pt2; pm2 = pm2 or pm22; area = area or ar2
            add_row(src, u, title, addr, chips, date, approx, area, ptot, pm2, "Nam Ban")

def src_villas_digest():
    """Trang tin rao Villas tổng hợp (video môi giới + sàn, Villas đã mở lại nguồn gốc từng tin).
    KHÁC src_villas (lô Villas tự bán): đây là tin của người khác, có ngày đăng. Trang không để link gốc,
    nên URL giả chỉ dùng để băm khử lặp — không vào repo. aggregate.py chỉ dùng nhóm này cho bảng tháng."""
    src = "video môi giới + sàn (tổng hợp)"; base = "https://nambanvillas.vn/thi-truong/tin-rao-dat-nam-ban-moi/"
    r = get(src, base, delay=0.8)
    if r is None: return
    parts = re.split(r"<!-- DAY:(\d{4}-\d{2}-\d{2}) -->", r.text)
    for i in range(1, len(parts), 2):
        day = dt.date.fromisoformat(parts[i])
        for li in BeautifulSoup(parts[i + 1], "lxml").select("li.tin-item"):
            title = text_of(li.select_one(".tin-title")); desc = text_of(li.select_one(".tin-desc"))
            specs = [text_of(x) for x in li.select(".tin-specs span")]
            if not specs or re.search(r"không quy ra đơn giá|lệch nhau", desc): st(src, "skip_conflict"); continue
            feat = re.sub(r"^Tin rao [^.]*\.\s*", "", desc).split("Cần kiểm")[0]
            area = parse_area(specs[0]); ptot = None
            for x in specs:
                v, un = parse_money(x)
                if un == "total": ptot = v; break
            u = f"{base}#{day.isoformat()}-{area}-{ptot}"
            add_row(src, u, f"{title}. {feat}", specs[-1], " ".join(specs), day, False, area, ptot, None, None)

SOURCES = {
    "guland": src_guland,
    "batdongsanonline": lambda: src_bdsonline_like("batdongsanonline.vn", "batdongsanonline.vn",
        [("https://batdongsanonline.vn/nha-dat-thi-tran-nam-ban/", "Nam Ban"), ("https://batdongsanonline.vn/nha-dat-xa-dong-thanh/", "Đông Thanh"),
         ("https://batdongsanonline.vn/nha-dat-xa-me-linh/", "Mê Linh"), ("https://batdongsanonline.vn/nha-dat-xa-gia-lam/", None)], r"-\d{3,}/?$"),
    "datnenlamdong": lambda: src_bdsonline_like("datnenlamdong.com.vn", "datnenlamdong.com.vn",
        [("https://datnenlamdong.com.vn/ban-dat-thi-tran-nam-ban/", "Nam Ban"), ("https://datnenlamdong.com.vn/ban-dat-xa-dong-thanh/", "Đông Thanh"),
         ("https://datnenlamdong.com.vn/ban-dat-xa-me-linh/", "Mê Linh"), ("https://datnenlamdong.com.vn/ban-dat-xa-gia-lam/", None)],
        r"datnenlamdong\.com\.vn/(?!ban-dat-|ban-nha-|cho-thue|tin-tuc|du-an|ban-do|page|trang)[a-z0-9-]{20,}/?$"),
    "bandatlamdong": lambda: src_bdsonline_like("bandatlamdong.com.vn", "bandatlamdong.com.vn",
        [("https://bandatlamdong.com.vn/ban-dat-thi-tran-nam-ban/", "Nam Ban"), ("https://bandatlamdong.com.vn/ban-dat-xa-dong-thanh/", "Đông Thanh"),
         ("https://bandatlamdong.com.vn/ban-dat-xa-me-linh/", "Mê Linh"), ("https://bandatlamdong.com.vn/ban-dat-xa-gia-lam/", None)],
        r"bandatlamdong\.com\.vn/(?!ban-dat-|ban-nha-|cho-thue|tin-tuc|du-an|ban-do|page|trang)[a-z0-9-]{20,}/?$"),
    "thuviennhadat": src_thuviennhadat, "muaban": src_muaban, "mogi": src_mogi, "nambanvillas": src_villas,
    "villasdigest": src_villas_digest,
}

def main():
    global SRC_NAME
    t0 = time.time()
    SRC_NAME = sys.argv[1] if len(sys.argv) > 1 else "all"
    log(f"Bắt đầu {dt.datetime.utcnow().isoformat()}Z · nguồn={SRC_NAME} · UA={UA}")
    todo = [SOURCES[SRC_NAME]] if SRC_NAME in SOURCES else list(SOURCES.values())
    for fn in todo:
        try:
            fn()
        except Exception as e:
            import traceback; log("LỖI nguồn:", type(e).__name__, str(e)[:200]); log(traceback.format_exc()[-1500:])
        flush()
    flush()
    log("XONG", len(ROWS), "dòng ·", int(time.time() - t0), "giây"); log(json.dumps(STATS, ensure_ascii=False))
    open(f"{OUT}/log-{SRC_NAME}.txt", "w", encoding="utf-8").write("\n".join(LOG))

if __name__ == "__main__":
    main()
