#!/usr/bin/env python3
"""Rà bài liệt kê nhiều tên riêng mà FAQ không phủ hết.

Bối cảnh: bài kể ra tám cái hồ, hai chục tên thôn, rồi chỉ có ba FAQ chung.
Người ta gõ TỪNG tên một; mình chỉ mở cửa cho câu tổng. Mất long-tail ở đúng
chỗ dễ thắng nhất, vì tên riêng địa phương gần như không ai cạnh tranh.

CHỈ BÁO, KHÔNG SỬA. Nhồi FAQ cho đủ số là đúng thứ Luật 14 cấm — bảng này để
người đọc chọn bài nào đáng bổ sung.

Ranh giới thân bài theo Luật 13c: <div|article class="art-body"> -> <div class="share-row">.
Chuẩn hoá &nbsp; theo Luật 13d trước khi so chuỗi.

Ba bẫy đã vấp khi viết bộ trích này, ghi lại để đừng lặp:
  1. re.IGNORECASE trên mẫu "hồ X" làm phần tên nuốt luôn chữ thường -> ra
     "đang được nhắc". Không dùng IGNORECASE; liệt kê cả hai dạng viết.
  2. Không cắt theo câu thì tên cuối câu dính chữ đầu câu sau -> "Nam Ban Nhiều".
     Phải tách câu trước khi dò.
  3. Chỉ lọc chữ ĐẦU của cụm là chưa đủ; phải lọc TỪNG chữ trong cụm.

    python3 tools/scan-faq-coverage.py [số dòng]
"""
import re, os, glob, json, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_FILES = {"_mau-bai-viet.html", "demo-selection.html", "404.html"}

UP = "A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐĨŨƠƯẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴÝỶỸ"
LO = "a-zà-ỹ"
CAP = r"[%s][%s%s]*" % (UP, LO, UP)

# Tên vùng chung, thương hiệu, tên tỉnh xa — không phải long-tail của bài.
STOP = {
    "Nam Ban", "Lâm Hà", "Lâm Đồng", "Đà Lạt", "Việt Nam", "Nam Ban Lâm Hà",
    "Panorama", "Namban Panorama", "Namban", "Google", "Google Maps",
    "Facebook", "Zalo", "Hà Nội", "Sài Gòn", "Hồ Chí Minh", "TP HCM",
    "Bảo Lộc", "Di Linh", "Đức Trọng", "Đơn Dương", "Lạc Dương",
    "Bình Dương", "Đồng Nai", "Cần Thơ", "Phan Thiết", "Vĩnh Phúc",
    "Thanh Hóa", "Thái Nguyên", "Nghệ An", "Hà Tĩnh", "Nam Định",
    "Brief", "Index", "Namban Index", "OCOP", "AI", "Loại III",
}

# Chữ viết hoa nhưng KHÔNG phải tên riêng: đầu câu, đại từ, danh từ chung.
COMMON = set("""Nhưng Nếu Còn Và Vì Khi Cái Người Một Hai Ba Bốn Năm Sáu Bảy Tám Chín Mười
Đây Đó Cả Chỗ Mấy Tôi Ai Không Có Với Cùng Sau Trước Trong Ngoài Trên Dưới Theo Từ Đến Tới
Ở Là Thì Mà Nên Đừng Hãy Rồi Đã Đang Sẽ Chưa Vẫn Cứ Chỉ Thứ Lô Đất Giá Nhà Bài Trang Phần
Khoảng Tùy Muốn Biết Nhìn Hỏi Xem Đi Về Lên Xuống Ra Vào Qua Qua Này Kia Nọ Ấy Vậy Thế Sao
Bạn Mình Họ Nó Chúng Những Các Mỗi Nhiều Ít Rất Hơi Quá Lắm Thật Đúng Sai Tốt Xấu Được Bị
Cách Kiểu Loại Dạng Mức Số Con Chiếc Cây Quả Trái Miếng Mảnh Khu Vùng Nơi Chốn Bên Phía Hướng
Trưởng Thôn Xã Huyện Tỉnh Thành Phố Phường Đường Cầu Hồ Thác Đèo Suối Núi Đồi Chợ Quán Trường
Sáng Trưa Chiều Tối Đêm Ngày Tháng Tuần Mùa Nay Mai Qua Trước Sau Giờ Lúc Hồi Dạo Đợt Lần
Muốn Cần Phải Nếu Dù Tuy Song Mặc Bởi Do Nhờ Tại Vì Nên Cho Của Cùng Và Hay Hoặc Rằng Là
Trụ Long Địa Sân Nguồn Cuộc Nhắc Đội Tìm Gọi Ghi Đọc Viết Nghe Nói Kể Làm Mua Bán Trả Nhận""".split())


def body_text(raw):
    m = re.search(r'<(?:div|article)[^>]*art-body[^>]*>', raw)
    if not m:
        return ""
    end = raw.find('<div class="share-row')
    seg = raw[m.end():end if end > 0 else len(raw)]
    seg = re.sub(r'<figure.*?</figure>', ' ', seg, flags=re.S)
    seg = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', seg, flags=re.S)
    # thẻ khối -> dấu chấm, để câu không dính nhau qua ranh thẻ
    seg = re.sub(r'</(p|h2|h3|li|div|blockquote|figcaption)>', ' . ', seg)
    seg = re.sub(r'<[^>]+>', ' ', seg)
    return re.sub(r'\s+', ' ', html.unescape(seg).replace('\xa0', ' '))


def faq_pairs(raw):
    out = []
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            o = json.loads(blk)
        except Exception:
            continue
        if isinstance(o, dict) and o.get("@type") == "FAQPage":
            for q in o.get("mainEntity", []):
                out.append((q.get("name", ""),
                            q.get("acceptedAnswer", {}).get("text", "")))
    return out


KINDS = ("hồ|Hồ|thác|Thác|đập|Đập|đèo|Đèo|thôn|Thôn|chùa|Chùa|cầu|Cầu|suối|Suối|"
         "núi|Núi|chợ|Chợ|quán|Quán|trường|Trường|farm|Farm|hill|Hill|"
         "buôn|Buôn|làng|Làng|nhà thờ|Nhà thờ|thiền viện|Thiền viện")

# CHỈ bắt tên có danh từ chỉ loại đứng trước — "hồ Bãi Công", "thác Bảy Tầng".
# Đã BỎ bộ dò cụm-viết-hoa chung: nó kéo vào "Chơi Đà Lạt", "Rời Sài Gòn",
# cả danh sách tỉnh quê — nhiễu nhiều hơn tín hiệu (Luật 14).
# Đổi lại bảng này CHÍNH XÁC chứ không ĐẦY ĐỦ: tên không có danh từ loại
# đứng trước (Nacasoo Hill, King Coffee, Yellow Bourbon) sẽ KHÔNG lọt vào.
RE_KIND = re.compile(r"\b((?:%s)\s+(?:%s)(?:\s+%s){0,2})" % (KINDS, CAP, CAP))
RE_ROAD = re.compile(r"\b(ĐT\.?\s?\d{3}|QL\s?\d{1,3}|T-\d{2})\b")


def trim(name):
    """Chỉ bỏ chữ THƯỜNG ở đuôi cụm.

    KHÔNG bỏ chữ nằm trong COMMON: làm vậy cắt nát tên thật —
    "Thăng Long" -> "Thăng", "Ba Đình" -> "Đình", "Thác Voi" -> "Voi".
    """
    w = name.split()
    while len(w) > 1 and not re.match(r"[%s]" % UP, w[-1]):
        w.pop()
    return " ".join(w)


def find_names(text):
    found = {}
    # tách câu trước, để tên cuối câu không dính chữ đầu câu sau
    for sent in re.split(r'(?<=[.!?;:])\s+|\s+[—–]\s+', text):
        for pat, group in ((RE_KIND, 1), (RE_ROAD, 1)):
            for m in pat.finditer(sent):
                n = trim(re.sub(r'\s+', ' ', m.group(group)).strip(' ,.;:"“”()'))
                if len(n) < 3 or n in STOP:
                    continue
                # phần sau danh từ loại phải có ít nhất một chữ viết hoa thật
                parts = n.split()
                if len(parts) < 2 and not RE_ROAD.fullmatch(n):
                    continue

                found[n] = found.get(n, 0) + 1
    # LUẬT 4: gộp không phân biệt hoa thường — "Hồ Bãi Công" và "hồ Bãi Công"
    # là MỘT tên, đếm hai lần là thổi phồng số "chưa phủ".
    ci = {}
    for k, v in found.items():
        key = k.lower()
        if key not in ci or len(k) > len(ci[key][0]):
            ci[key] = (k, ci.get(key, (k, 0))[1] + v)
        else:
            ci[key] = (ci[key][0], ci[key][1] + v)
    found = {v[0]: v[1] for v in ci.values()}
    # gộp tên nằm gọn trong tên dài hơn (cũng không phân biệt hoa thường)
    merged = {}
    for k in sorted(found, key=len, reverse=True):
        if any(k != o and k.lower() in o.lower() for o in merged):
            continue
        merged[k] = found[k]
    return merged


def main():
    os.chdir(ROOT)
    rows = []
    for f in sorted(glob.glob("*.html")):
        if f in SKIP_FILES:
            continue
        raw = open(f, encoding="utf-8").read()
        if 'lang="vi"' not in raw[:400] or "art-body" not in raw:
            continue
        bt = body_text(raw)
        if not bt:
            continue
        names = find_names(bt)
        if len(names) < 5:
            continue
        fq = faq_pairs(raw)
        # LUẬT 4: so phủ cũng không phân biệt hoa thường
        blob = " ".join(q + " " + a for q, a in fq).lower()
        unc = [n for n in names if n.lower() not in blob]
        rows.append({"slug": f[:-5], "n_names": len(names), "n_faq": len(fq),
                     "uncovered": sorted(unc, key=lambda x: -names[x]),
                     "names": sorted(names, key=lambda x: -names[x])})
    rows.sort(key=lambda r: -len(r["uncovered"]))
    return rows


if __name__ == "__main__":
    rows = main()
    top = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    print("Bài có >=5 tên riêng trong thân bài: %d\n" % len(rows))
    print("%-38s %5s %5s %6s" % ("slug", "tên", "FAQ", "chưa phủ"))
    print("-" * 60)
    for r in rows[:top]:
        print("%-38s %5d %5d %6d" % (r["slug"], r["n_names"], r["n_faq"], len(r["uncovered"])))
