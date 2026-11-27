#!/usr/bin/env python3
"""Nhịp đăng mạng xã hội + bộ tự chọn bài (Chú chốt 26/11/2026).

Chú: "làm lại auto 5 ngày đăng 1 bài trên facebook, instagram và thread, ưu tiên các bài có tính chất
thời điểm mới nhất". Trước đó hàng đợi `data/fb-queue.json` chỉ chạy khi có người viết tay từng mục;
62 mục đăng hết ngày 20/11/2026 thì ba kênh đứng im.

Luật, dùng chung cho Facebook (`posted`), Instagram (`posted_ig`), Threads (`posted_threads`):

1. **Bắt kịp.** Mục đã lên một kênh khác trong vòng GAP_DAYS ngày mà kênh này chưa có → đăng luôn, không
   chờ nhịp. Nhờ vậy ba kênh đăng cùng một bài, kênh nào hỏng một hôm thì hôm sau tự đuổi kịp.
2. **Nhịp 5 ngày.** Kênh này đăng lần cuối chưa đủ GAP_DAYS ngày (tính theo ngày giờ Việt Nam) → không
   đăng. Ngoại lệ: mục viết tay có `"now": true` (tin gấp), hoặc bấm chạy tay (`SOCIAL_FORCE=1`).
3. **Mục viết tay đi trước.** Mục trong hàng đợi chưa đăng, `date` tới hạn → lấy theo `priority`
   (0 tin mới · 1 cập nhật · 2 bài nền · 5 còn lại), như trước.
4. **Hết mục viết tay → tự chọn**, theo độ "thời điểm":
     A. tin của xã trên /nam-ban-co-gi-moi trong NEWS_DAYS ngày, bài nhà chưa đăng từ ngày tin;
     B. Nam Ban Index sang kỳ tháng mới (số + ngày đo + khối tín hiệu tháng nếu đã viết);
     C. bài đăng trong NEW_DAYS ngày, chưa lên mạng xã hội lần nào;
     D. bài đúng mùa (SEASON: mùa cà phê, mùa bơ, mùa mưa…), chưa đăng trong SEASON_REPEAT ngày;
     E. bài chưa từng đăng, mới sửa trước.
   Mục tự chọn có `key` riêng `<slug>#<ngày>-…`, `full: false`, câu mồi lấy từ ô "Trả lời nhanh" / "Nếu
   hỏi nhanh" của bài (Chú viết sẵn), không thì từ mô tả trang. Phiếu đánh dấu mang theo nguyên mục, nên
   `apply-mark.py` tự chèn mục vào hàng đợi lúc ghi dấu — hàng đợi vẫn là sổ ghi đủ mọi bài đã đăng.

Chạy thử (chỉ in, không đăng, không sửa gì):  python3 tools/social_auto.py [YYYY-MM-DD]
"""
import datetime
import glob
import html as H
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://nambanpanorama.com"
VN = datetime.timezone(datetime.timedelta(hours=7))
FIELDS = ("posted", "posted_ig", "posted_threads")

GAP_DAYS = 5          # một bài mỗi 5 ngày (Chú chốt 26/11/2026)
NEWS_DAYS = 14        # tin xã cũ hơn thì không còn là "tin"
EVENT_DAYS = 3        # tin mời/dự báo/sự kiện ("mấy hôm này", "dự báo"…) chỉ đăng trong 3 ngày sau ngày cuối
STALE_DAYS = 120      # câu mồi có mốc "tính tới / giá … ngày d/m/yyyy" cũ hơn thì không tự đăng
NEW_DAYS = 30         # bài mới đăng
INDEX_QUIET = 14      # Index vừa đăng trong 14 ngày thì thôi
SEASON_REPEAT = 300   # bài theo mùa: năm sau mới đăng lại
STALE_NEWS_DAYS = 30  # NewsArticle cũ hơn thì không đưa vào nhóm E
TAGS = "#NamBan #LamDong"
THREADS_MAX = 500     # trần một bài Threads (tính cả link nối cuối)
# Chỉ đăng trong khung giờ VN này (trừ bấm tay). GitHub chạy lịch trễ 7–10 giờ: đo 30 lượt 11–25/11/2026, lịch
# 03:30 UTC chạy 10:41–13:59 UTC (17:41–20:59 giờ VN), lịch 12:30 UTC chạy 18:21–22:38 UTC (1:21–5:38 sáng giờ VN).
# Lượt rơi vào ban đêm thì bỏ, lượt sau trong khung giờ đăng; nhịp 5 ngày bảo đảm không đăng hai lần.
POST_HOURS = (7, 22)

# Trang không phải bài: hub, mục lục, trang tin (đã có nhóm A), Index (nhóm B).
SKIP = {"index", "nam-ban", "dat", "dau-tu", "hoi-nhanh", "trao-doi", "doc-lo-dat", "brief", "nam-ban-co-gi-moi",
        "namban-index", "404", "ve-panorama", "doc-nhanh"}
# Bài cố ý không tự đăng — mỗi dòng một lý do. Muốn đăng thì viết tay một mục trong hàng đợi.
NO_AUTO = {
    "thi-truong-dat-nam-ban-quy-3-2026": "thân bài còn nhận định theo số tháng 9 cũ, chờ Chú quyết viết lại",
    "thi-truong-dat-nam-ban-6-thang-dau-nam-2026": "báo cáo theo kỳ, số cũ",
    "tour-ca-phe-nam-ban": "nêu tên cơ sở kinh doanh — đăng lên mạng dễ thành quảng cáo (§5 kill-list luật 2)",
    "cay-xang-petro-moi-o-nam-ban": "tin cửa hàng xăng tháng 7, đã cũ",
    "doc-lo-dat-02-view-ho": "đọc một lô cụ thể với giá rao tháng 6, đã cũ",
    "brief-01": "số Brief theo kỳ", "brief-02": "số Brief theo kỳ", "brief-03": "số Brief theo kỳ",
    # rà phản biện 27/11/2026
    "ram-vu-lan-nam-ban": "bài sự kiện theo năm (rằm tháng Bảy 2026) — năm sau viết tay một mục khi trang đã cập nhật",
    "trung-thu-nam-ban": "bài sự kiện theo năm (Trung thu 2026) — như trên",
    "mua-dat-nam-ban": "ô trả lời nhanh còn khoảng giá giữa 2026, lệch Index",
    "mua-dat-duong-gia-nam-ban": "ô trả lời nhanh còn khoảng giá không ghi kỳ, lệch Index",
    "tiem-nang-dau-tu": "ô trả lời nhanh còn khoảng giá nửa đầu 2026, lệch Index",
    "ocop-nam-ban": "câu mồi mở bằng tên thương hiệu sản phẩm (§5 kill-list luật 2)",
    "nen-xem-khu-nao-o-nam-ban": "câu mồi dùng tên khu dự án làm mốc giới thiệu (§5 kill-list luật 2)",
    "mot-ngay-o-nam-ban": "câu mồi có \"bài này\" — trên mạng đọc thành chính bài đăng",
}
# Năm bài "giá hiện tại" bộ sinh Index tự đổi số mỗi tuần (LIVE trong gen-index-history.py): câu mồi có giá/m² vẫn đúng kỳ.
LIVE = {"hoi-nhanh", "dat-gan-da-lat", "dat-nam-ban-gia-re", "mua-dat-nam-ban-500-trieu-1-ty", "vung-ven-da-lat-nao-tot-nhat"}
# Bài theo mùa → tháng (dương lịch) đáng đăng. Ngoài mùa thì nhóm E cũng không lấy.
SEASON = {
    "mua-ca-phe-nam-ban": [2, 3, 10, 11, 12],   # mùa hoa 2–4 rộ tháng 3; thu hoạch 10→1, rộ 11–12
    "thue-nguoi-lam-vuon-nam-ban": [11, 12],    # công hái mùa cà phê
    "mua-vuon-ca-phe-nam-ban": [11, 12, 1],     # giá nhân, vụ thu hoạch
    "ca-phe-nam-ban": [11, 12],
    "mua-bo-nam-ban": [5, 6, 9, 10, 11],        # bơ 034 rộ cuối 5 đầu 6; Booth 8–12
    "mua-mua-nam-ban": [5, 6, 7, 8],
}
LABELS = [("tach_thua_150_300", "đất nền tách thửa 150–300 m²"), ("lo_500_tho_cu", "lô khoảng 500 m² có thổ cư"),
          ("dat_tren_1000", "đất trên 1.000 m²"), ("view", "lô có view hồ, đồi, toàn cảnh")]


# ------------------------------------------------------------------ ngày tháng

def today_vn():
    return datetime.datetime.now(VN).date()


def _vn_date(s):
    """'2026-11-20T20:36:49+00:00' → ngày giờ Việt Nam. Chuỗi chỉ có ngày thì lấy nguyên ngày đó."""
    s = str(s or "").strip()
    if not s:
        return None
    try:
        if len(s) == 10:
            return datetime.date.fromisoformat(s)
        d = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=datetime.timezone.utc)
        return d.astimezone(VN).date()
    except ValueError:
        return None


def posted_on(p, field):
    """Ngày (giờ VN) mục này lên kênh `field`; None nếu chưa lên. Mục cũ không ghi giờ → lấy `date`."""
    if not p.get(field):
        return None
    return _vn_date(p.get(field + "_at")) or _vn_date(p.get("date"))


def last_post(queue, field):
    ds = [d for d in (posted_on(p, field) for p in queue) if d]
    return max(ds) if ds else None


def slug_posts(queue, slug):
    """Mọi ngày trang `slug` đã lên bất kỳ kênh nào."""
    out = []
    for p in queue:
        if p.get("slug") == slug:
            out += [d for d in (posted_on(p, f) for f in FIELDS) if d]
    return out


def key_of(p):
    return p.get("key") or p.get("slug")


# ------------------------------------------------------------------ chữ

def clean(s):
    s = re.sub(r"<br\s*/?>\s*<br\s*/?>", "\n\n", s)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = H.unescape(s).replace("\xa0", " ")
    s = "\n".join(" ".join(ln.split()) for ln in s.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def sentences(text):
    return [x for x in re.split(r"(?<=[.!?…])\s+", " ".join(text.split())) if x]


def fit(text, limit):
    """Cắt theo câu cho vừa `limit` ký tự; câu đầu đã quá thì trả None (không cắt giữa câu)."""
    out = ""
    for snt in sentences(text):
        nxt = (out + " " + snt).strip()
        if len(nxt) > limit:
            break
        out = nxt
    return out or None


def fit_paras(text, limit):
    """Như `fit` nhưng giữ đoạn: lấy trọn từng đoạn, đoạn cuối không vừa thì cắt theo câu."""
    out = []
    for para in text.split("\n\n"):
        cur = "\n\n".join(out)
        room = limit - len(cur) - (2 if out else 0)
        if len(para) <= room:
            out.append(para)
            continue
        part = fit(para, room) if "\n" not in para else None
        if part:
            out.append(part)
        break
    return "\n\n".join(out) or None


def threads_text(lead, body, slug):
    """Bản Threads: `lead` (tựa, có thể rỗng) + `body` cắt theo câu, tính cả link nối cuối."""
    room = THREADS_MAX - len("%s/%s" % (SITE, slug)) - 2
    head = (lead + "\n\n") if lead else ""
    t = fit(body, room - len(head))
    if t and len(t) < len(" ".join(body.split())) and re.search(PROMISE, t, re.I):
        t = None                      # bị cắt mà câu giữ lại hứa "bốn điểm / ba việc…" → không dùng
    return (head + t) if t else (fit(lead, room) or "")


PROMISE = r"\b(hai|ba|bốn|năm|sáu|bảy|tám|chín|mười|\d+)\s+(điểm|thứ|việc|cách|bước|loại|chỗ|câu|điều|lý do|khoản)\b"


# ------------------------------------------------------------------ đọc trang

def read(slug):
    try:
        with open(os.path.join(ROOT, slug + ".html"), encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def ld_blocks(s):
    out = []
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(j)
        except ValueError:
            continue
        for o in (d.get("@graph", [d]) if isinstance(d, dict) else d):
            if isinstance(o, dict):
                out.append(o)
    return out


def _types(o):
    t = o.get("@type")
    return set(t) if isinstance(t, list) else {t}


def page_meta(slug):
    """Ngày đăng, ngày sửa, có phải tin không, H1, câu trả lời nhanh, mô tả."""
    s = read(slug)
    if not s:
        return None
    pub = mod = None
    news = False
    for o in ld_blocks(s):
        if _types(o) & {"Article", "NewsArticle", "BlogPosting", "Report", "AnalysisNewsArticle"}:
            pub = pub or _vn_date(o.get("datePublished"))
            mod = mod or _vn_date(o.get("dateModified"))
            news = news or "NewsArticle" in _types(o)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    # <br> trong H1 chỉ để ngắt dòng cho đẹp ("…mua bán hơn<br>các vùng ven Đà Lạt khác?") → nối lại thành một câu
    title = " ".join(clean(re.sub(r"<br\s*/?>", " ", h1.group(1))).split()) if h1 else ""
    qa = ""
    m = re.search(r'<div class="tldr">.*?<p>(.*?)</p>', s, re.S)
    if m:
        qa = clean(m.group(1))
    else:
        m = re.search(r'<div class="quick-answer">(.*?)</div>', s, re.S)
        if m:
            raw = m.group(1).strip()
            # nhãn "Nếu hỏi nhanh:", "Hỏi nhanh.", "Nói ngắn gọn:"… nằm trong <strong> đầu khối → bỏ;
            # nhãn là câu hỏi ("Nam Ban hay Lạc Dương?") thì giữ, vì nó chính là câu đang được trả lời
            lm = re.match(r"<strong>(.*?)</strong>\s*", raw, re.S)
            if lm and clean(lm.group(1)).endswith((":", ".")):
                raw = raw[lm.end():]
            qa = re.sub(r"^(Nếu hỏi nhanh|Hỏi nhanh|Trả lời nhanh|Nói ngắn gọn|Nếu chỉ cần câu trả lời ngắn)\s*[:.]?\s*",
                        "", clean(raw))
    qa = qa[:1].upper() + qa[1:]
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    return {"pub": pub, "mod": mod or pub, "news": news, "title": title, "qa": qa,
            "desc": clean(d.group(1)) if d else "",
            "vi": 'lang="vi"' in s[:400],
            "noindex": bool(re.search(r'<meta name="robots" content="[^"]*noindex', s))}


def news_items():
    """Mục tin trên /nam-ban-co-gi-moi, mới nhất trước: (ngày, tựa, tóm tắt, slug bài nhà, chữ link)."""
    s = read("nam-ban-co-gi-moi")
    if '<div class="tl">' not in s:
        return []
    body = s[s.index('<div class="tl">'):]
    out = []
    for m in re.finditer(r'<div class="tl-item"([^>]*)>(.*?)\n    </div>', body, re.S):
        if 'data-social="no"' in m.group(1):
            continue
        inner = m.group(2)
        date = re.search(r'<div class="tl-date">(.*?)</div>', inner, re.S)
        title = re.search(r'<div class="tl-title">(.*?)</div>', inner, re.S)
        summ = re.search(r'<div class="tl-sum">(.*?)</div>', inner, re.S)
        link = re.search(r'<a class="tl-link" href="([^"]+)"[^>]*>(.*?)</a>', inner, re.S)
        if not (date and title and summ):
            continue
        ds = re.findall(r"(\d{1,2})/(\d{1,2})/(20\d\d)", clean(date.group(1)))
        if not ds:                      # "Tháng 10/2026" — không có ngày cụ thể
            continue
        d, mo, y = map(int, ds[-1])
        try:
            nd = datetime.date(y, mo, d)
        except ValueError:
            continue
        home, ltxt = "nam-ban-co-gi-moi", "Nam Ban có gì mới"
        if link:
            href = link.group(1).split("#")[0].strip("/")
            if href and not href.startswith("http") and os.path.exists(os.path.join(ROOT, href + ".html")):
                home = href
                ltxt = re.sub(r"^Đọc bài\s*[—–-]\s*", "", clean(link.group(2))).rstrip(" →").strip()
        # câu nhắc sang bài khác ("Tôi viết riêng ở bài đất nguồn gốc lâm nghiệp.") mất thẻ <a> khi lên mạng,
        # còn link dưới bài lại trỏ bài nhà → bỏ câu đó khỏi câu mồi
        others = [clean(a.group(2)) for a in re.finditer(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', summ.group(1), re.S)
                  if a.group(1).split("#")[0].strip("/") != home]
        text = clean(summ.group(1))
        if others:
            paras = []
            for para in text.split("\n\n"):
                keep = [x for x in sentences(para) if not any(o and o in x for o in others)] if "\n" not in para else (
                    [para] if not any(o and o in para for o in others) else [])
                if keep:
                    paras.append(" ".join(keep))
            text = "\n\n".join(paras)
        if text:
            out.append((nd, clean(title.group(1)), text, home, ltxt))
    return out


# ------------------------------------------------------------------ dựng mục

def _entry(slug, key, today, prio, tier, note, title, body, threads, comment):
    msg = title + "\n\n" + body + "\n\nBản đầy đủ ở comment.\n\n" + TAGS
    comment = comment.split("?")[0].strip()
    if len(comment) > 70 and ":" in comment:      # chữ dẫn link ngắn: lấy vế trước dấu hai chấm
        comment = comment.split(":")[0].strip()
    return {"date": today.isoformat(), "slug": slug, "key": key, "priority": prio, "full": False,
            "auto": tier, "note": note, "comment": comment + " —",
            "message": msg, "threads": threads}


def article_entry(slug, today, prio, tier, note):
    m = page_meta(slug)
    if not m or not m["title"]:
        return None
    src = m["qa"] or m["desc"]
    body = fit_paras(src, 1200) if src else None
    if not body:
        return None
    th = threads_text(m["title"], src, slug)
    if not th or th == fit(m["title"], THREADS_MAX):
        th = threads_text(m["title"], m["desc"], slug) or th
    # khoá KHÔNG gắn ngày chọn: hai kênh chọn cùng bài ở hai phía nửa đêm (cron trễ) vẫn ra cùng một khoá
    key = "%s#mua-%d" % (slug, today.year) if tier == "D-mua" else "%s#auto" % slug
    return _entry(slug, key, today, prio, tier, note, m["title"], body, th, m["title"])


def ascii_slug(text, words=4):
    t = unicodedata.normalize("NFD", text.replace("đ", "d").replace("Đ", "D"))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    return "-".join(re.findall(r"[a-z0-9]+", t)[:words])


def news_key(item):
    """Khoá riêng mỗi mục tin: hai tin cùng ngày cùng bài nhà (vd hai tin 9/10/2026) không được trùng khoá."""
    nd, title, _, home, _ = item
    return "%s#%s-tin-%s" % (home, nd.isoformat(), ascii_slug(title))


def news_entry(item, today):
    nd, title, summ, home, ltxt = item
    body = fit_paras(summ, 1500)
    if not body:
        return None
    first = summ.split("\n\n")[0]
    th = threads_text(title, first, home)
    return _entry(home, news_key(item), today, 0, "A-tin",
                  "Tự chọn: tin xã %s trên /nam-ban-co-gi-moi." % nd.strftime("%-d/%-m/%Y"),
                  title, body, th, ltxt)


def index_entry(today):
    try:
        with open(os.path.join(ROOT, "tools", "idx-live-state.json"), encoding="utf-8") as fh:
            st = json.load(fh)
    except (OSError, ValueError):
        return None
    ky, dfull, med = st.get("ky"), st.get("d_full"), st.get("med2") or {}
    if not (ky and dfull):
        return None
    parts = ["%s %s" % (lab, med[k]) for k, lab in LABELS if med.get(k)]
    if len(parts) < 3:
        return None
    mo, yy = ky.split("/")
    # Không đưa số "tin còn đang rao": mốc nền đang lẫn tin cũ của một nguồn (CLAUDE.md, chờ Chú quyết).
    paras = ["Trung vị giá rao, triệu đồng/m²: " + " · ".join(parts) + "."]
    s = read("namban-index")
    h2 = "Tín hiệu thị trường đất Nam Ban tháng %s" % ky
    for m in re.finditer(r'<h2[^>]*>((?:(?!</h2>).)*)</h2>\s*<div class="signal-now">\s*<p>(.*?)</p>', s, re.S):
        if clean(m.group(1)) == h2:
            sig = fit(clean(m.group(2)), 1100)
            if sig:
                paras.append(sig)
            break
    paras.append("Đây là giá rao, chưa phải giá chốt.")
    title = "Giá đất Nam Ban tháng %s: giá rao từng loại đất, đo tới %s." % (ky, dfull)
    short = "; ".join("%s %s" % (lab.replace("lô có view hồ, đồi, toàn cảnh", "lô view hồ, đồi"), med[k])
                      for k, lab in LABELS if med.get(k))
    th = ("Giá rao đất Nam Ban tháng %s, đo tới %s — trung vị, triệu đồng/m²: %s. Giá rao, chưa phải giá chốt."
          % (ky, dfull, short))
    e = _entry("namban-index", "namban-index#ky-%s-%s" % (yy, mo.zfill(2)), today, 1, "B-index",
               "Tự chọn: Nam Ban Index sang kỳ tháng %s." % ky, title, "\n\n".join(paras), th,
               "Giá đất Nam Ban hôm nay")
    e["message"] = e["message"].replace(TAGS, TAGS + " #GiaDatNamBan")
    if yy != "2026":                  # ảnh og của Index in chữ "Giá đất Nam Ban 2026"
        e["image"] = "/images/nam-ban-toan-canh-og.jpg"
    return e


def candidates(queue, today):
    """Sinh mục tự chọn theo thứ tự ưu tiên A → E (lười: chỉ dựng tới khi có mục qua kiểm)."""
    keys = {key_of(p) for p in queue}
    # trang đang có mục viết tay chờ tới hẹn → không tự chọn trang đó (tránh đăng hai lần cách nhau vài ngày)
    pending = {p.get("slug") for p in queue if not p.get("auto") and not any(p.get(f) for f in FIELDS)}

    def since(slug, d0):
        return any(d >= d0 for d in slug_posts(queue, slug))

    def covered(it):
        """Tin đã lên mạng chưa: đúng khoá tin, hoặc bài nhà đã đăng (bằng mục không phải tin tự chọn) từ ngày tin,
        hoặc mục viết tay cũ cho tin đó (khoá chứa ngày tin)."""
        nd, home = it[0], it[3]
        if news_key(it) in keys:
            return True
        for p in queue:
            if p.get("slug") != home or p.get("auto") == "A-tin":
                continue
            if not any(d and d >= nd for d in (posted_on(p, f) for f in FIELDS)):
                continue
            if home != "nam-ban-co-gi-moi" or nd.isoformat() in str(p.get("key") or ""):
                return True
        return False

    # A — tin xã mới
    for it in news_items():
        nd, home = it[0], it[3]
        if (today - nd).days > NEWS_DAYS or nd > today or home in pending or covered(it):
            continue
        if (today - nd).days > EVENT_DAYS and re.search(EVENT_WORDS, it[1] + " " + it[2], re.I):
            continue                  # tin mời / dự báo / sự kiện đã qua
        e = news_entry(it, today)
        if e:
            yield e
    # B — Index sang tháng mới
    e = index_entry(today)
    if e and e["key"] not in keys and not since("namban-index", today - datetime.timedelta(days=INDEX_QUIET)):
        yield e
    # C, D, E — bài
    pages = {}
    for f in glob.glob(os.path.join(ROOT, "*.html")):
        slug = os.path.basename(f)[:-5]
        if slug in SKIP or slug in NO_AUTO or slug.startswith(("_", "demo")):
            continue
        m = page_meta(slug)
        if m and m["vi"] and not m["noindex"] and m["pub"]:
            pages[slug] = m
    never = {s: m for s, m in pages.items() if not slug_posts(queue, s) and s not in pending}
    in_season = lambda s: s not in SEASON or today.month in SEASON[s]
    for s, m in sorted(never.items(), key=lambda x: (x[1]["pub"], x[0]), reverse=True):
        if (today - m["pub"]).days <= NEW_DAYS and in_season(s):
            e = article_entry(s, today, 1, "C-moi", "Tự chọn: bài mới đăng %s, chưa lên mạng xã hội."
                              % m["pub"].strftime("%-d/%-m/%Y"))
            if e and good(e, today):
                yield e
    # Bài theo mùa xen với bài khác: lượt trước đã là bài mùa (trong 2 nhịp gần nhất) thì lượt này nhường nhóm E,
    # để tháng 12 không ra bốn bài cà phê liền nhau.
    recent_d = any(p.get("auto") == "D-mua" and any(d and (today - d).days < 2 * GAP_DAYS
                                                    for d in (posted_on(p, f) for f in FIELDS)) for p in queue)
    for s in ([] if recent_d else SEASON):
        if s in pages and s not in pending and today.month in SEASON[s]:
            last = max(slug_posts(queue, s), default=None)
            # đăng lại năm sau chỉ khi trang đã được làm mới sau lần đăng trước (không đăng lại số của năm cũ)
            if last is None or ((today - last).days >= SEASON_REPEAT and pages[s]["mod"] > last):
                e = article_entry(s, today, 2, "D-mua", "Tự chọn: bài đúng mùa (tháng %d)." % today.month)
                if e and good(e, today):
                    yield e
    for s, m in sorted(never.items(), key=lambda x: (x[1]["mod"], x[1]["pub"], x[0]), reverse=True):
        if s in SEASON:               # bài theo mùa chỉ đi đường D, để luật xen kẽ còn tác dụng
            continue
        if m["news"] and (today - m["pub"]).days > STALE_NEWS_DAYS:
            continue
        e = article_entry(s, today, 5, "E-chua-dang", "Tự chọn: bài chưa từng lên mạng xã hội, sửa gần nhất %s."
                          % m["mod"].strftime("%-d/%-m/%Y"))
        if e and good(e, today):
            yield e


EVENT_WORDS = r"dự báo|mấy hôm này|mấy ngày này|sẽ diễn ra|cứ ghé|xin mời|mời bà con"
DATE_AT = re.compile(r"(?:tính tới|tính đến|tới ngày|đến ngày|đo tới|ghi nhận|cập nhật|tới|đến)\s+(?:ngày\s+)?"
                     r"(\d{1,2})/(\d{1,2})/(20\d\d)", re.I)
PRICE_AT = re.compile(r"giá[^.]{0,60}?(?:ngày|tháng)\s+(?:(\d{1,2})/)?(\d{1,2})/(20\d\d)", re.I)
# trang có giá/m² nhưng giá đó còn hiệu lực tới một ngày biết trước (bảng giá nhà nước theo năm)
PRICE_OK_UNTIL = {"bang-gia-dat-nam-ban": datetime.date(2026, 12, 31)}
PER_M2 = re.compile(r"(?:tr|triệu)\s*(?:đồng\s*)?/\s*m(?:²|2)", re.I)


def good(e, today):
    """Chốt chất lượng cho câu mồi bài (C/D/E), rút từ vòng phản biện 27/11/2026."""
    text = e["message"] + "\n" + e["threads"]
    body = e["message"].split("\n\n")[1] if "\n\n" in e["message"] else ""
    if re.search(r"\bbài này\b", text, re.I):
        print("  (bỏ /%s — câu mồi có 'bài này')" % e["slug"]); return False
    if not body[:1].isupper() and not body[:1].isdigit():
        print("  (bỏ /%s — câu mồi không mở bằng chữ hoa)" % e["slug"]); return False
    if e["slug"] not in LIVE and PER_M2.search(text) and today > PRICE_OK_UNTIL.get(e["slug"], datetime.date.min):
        print("  (bỏ /%s — câu mồi có giá theo m² không tự cập nhật)" % e["slug"]); return False
    for rx in (DATE_AT, PRICE_AT):
        for m in rx.finditer(text):
            d, mo, y = m.group(1), m.group(2), m.group(3)
            try:
                dt = datetime.date(int(y), int(mo), int(d) if d else 28)
            except ValueError:
                continue
            if (today - dt).days > STALE_DAYS:
                print("  (bỏ /%s — mốc '%s' đã cũ)" % (e["slug"], m.group(0)[:40])); return False
    return True


# ------------------------------------------------------------------ chọn

def pick(queue, field, force=False, ok=lambda p: True, today=None):
    """Trả (mục, lý do) hoặc (None, lý do). `ok(mục)` → True nếu mục qua kiểm luật §2.1 / caption.
    `today` chỉ truyền khi mô phỏng — lúc đó không xét khung giờ."""
    if today is None and not force:
        now = datetime.datetime.now(VN)
        if not POST_HOURS[0] <= now.hour < POST_HOURS[1]:
            return None, ("ngoài giờ đăng: %s giờ VN, chỉ đăng %d:00–%d:00 — đợi lượt chạy sau"
                          % (now.strftime("%H:%M"), POST_HOURS[0], POST_HOURS[1]))
    today = today or today_vn()
    others = [f for f in FIELDS if f != field]

    def other_day(p):
        ds = [d for d in (posted_on(p, f) for f in others) if d]
        return min(ds) if ds else None

    recent = {p.get("slug") for p in queue if posted_on(p, field)
              and (today - posted_on(p, field)).days < 2 * GAP_DAYS}
    catch = [p for p in queue if not p.get(field) and other_day(p)
             and (today - other_day(p)).days <= GAP_DAYS
             and ("-tin-" in str(p.get("key") or "") or p.get("slug") not in recent)]
    if catch:
        p = sorted(catch, key=other_day)[0]
        return p, "bắt kịp: /%s đã lên kênh khác ngày %s" % (p.get("slug"), other_day(p))

    t = today.isoformat()
    # mục tự chọn của kênh khác chỉ sang kênh này qua đường bắt kịp (≤ GAP_DAYS); quá hạn thì bỏ, không đăng bù
    due = sorted([p for p in queue if not p.get(field) and not p.get("auto") and str(p.get("date") or "9999") <= t],
                 key=lambda p: (p.get("priority", 5), str(p.get("date") or "9999")))
    urgent = [p for p in due if p.get("now")]
    if urgent:
        return urgent[0], "mục gấp (`now: true`)"

    last = last_post(queue, field)
    if not force and last and (today - last).days < GAP_DAYS:
        return None, ("chưa tới lượt: kênh này đăng lần cuối %s, nhịp %d ngày → lượt tới %s"
                      % (last, GAP_DAYS, last + datetime.timedelta(days=GAP_DAYS)))
    lead = "bấm chạy tay, bỏ qua nhịp — " if force else ""
    if due:
        return due[0], lead + "mục viết tay trong hàng đợi (ưu tiên %s)" % due[0].get("priority", 5)
    for e in candidates(queue, today):
        if ok(e):
            return e, lead + "tự chọn %s: /%s" % (e["auto"], e["slug"])
        print("  (bỏ mục tự chọn /%s — không qua kiểm)" % e["slug"])
    return None, "không còn bài nào để tự chọn"


if __name__ == "__main__":
    with open(os.path.join(ROOT, "data", "fb-queue.json"), encoding="utf-8") as fh:
        q = json.load(fh)
    day = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else today_vn()
    for f in FIELDS:
        p, why = pick(q, f, today=day)
        print("%-15s %s" % (f, why))
    print("\nNăm mục tự chọn đầu tiên (ngày %s):" % day)
    for i, e in enumerate(candidates(q, day)):
        if i == 5:
            break
        print("\n=== %s · %s · key %s" % (e["auto"], e["slug"], e["key"]))
        print(e["message"])
        print("--- comment:", e["comment"])
        print("--- threads (%d ký tự + link):" % len(e["threads"]), e["threads"])
