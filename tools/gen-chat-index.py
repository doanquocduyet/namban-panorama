#!/usr/bin/env python3
"""Sinh chat-index.json cho bot hỏi–đáp MIỄN PHÍ (bản thử /demo-hoi-dap, thêm 19/11/2026).

Bot KHÔNG dùng AI viết câu: nó chạy trong trình duyệt người đọc, so câu hỏi với kho này và
trả lại NGUYÊN VĂN câu trả lời đã có trên web, kèm link bài. Không máy chủ, không khoá API, 0 đồng.

Kho gồm hai loại dòng:
  faq  — mọi cặp hỏi–đáp trong FAQPage JSON-LD của trang tiếng Việt (mỗi câu một nhà, §7.3:
         câu chỉ hiển thị mà không vào schema là câu có nhà ở bài khác, nên bỏ qua để bot dẫn
         đúng bài nhà).
  muc  — từng mục H2 của bài (tiêu đề mục + đoạn văn đầu), cho câu hỏi chưa có FAQ.
Bỏ: trang noindex, khuôn, trang nháp, trang ngoại ngữ, mục của hub (danh sách link), mục
"Câu hỏi thường gặp", "Nguồn & lưu ý", "Đọc gì tiếp"...

Trường f* = chữ đã bỏ dấu, dựng sẵn để máy người đọc khỏi chuẩn hoá lúc gõ.

    python3 tools/gen-chat-index.py
"""
import glob
import html
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {"404.html", "_mau-bai-viet.html"}
# Hub và trang danh sách: lấy FAQ, KHÔNG lấy mục H2 (mục ở đây là danh sách link, không phải câu trả lời)
NO_SECTIONS = {"index", "nam-ban", "dat", "dau-tu", "brief", "nam-ban-co-gi-moi", "hoi-nhanh",
               "trao-doi", "doc-lo-dat", "namban-index"}
BAD_H2 = re.compile(r"câu hỏi thường gặp|hỏi đáp|nguồn|lưu ý|đọc gì tiếp|đọc tiếp|bài liên quan|"
                    r"mới cập nhật|chia sẻ|xem thêm|tham khảo|trích dẫn|mục lục", re.I)
MAX_A = 700


def clean(s):
    """html.unescape + bỏ \\xa0 (Luật 13d) + gộp khoảng trắng."""
    return re.sub(r"\s+", " ", html.unescape(s).replace("\xa0", " ")).strip()


def strip_tags(s):
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    return clean(re.sub(r"<[^>]+>", " ", s))


def fold(s):
    s = s.lower().replace("đ", "d")
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def cut(s, n=MAX_A):
    if len(s) <= n:
        return s
    s = s[:n]
    k = max(s.rfind(". "), s.rfind("; "))
    return (s[:k + 1] if k > n * 0.5 else s.rsplit(" ", 1)[0] + "…").strip()


def faqs(raw):
    out = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            d = json.loads(m.group(1))
        except ValueError:
            continue
        items = d.get("@graph", [d]) if isinstance(d, dict) else d
        for it in items if isinstance(items, list) else [items]:
            if isinstance(it, dict) and it.get("@type") == "FAQPage":
                for q in it.get("mainEntity", []):
                    a = q.get("acceptedAnswer") or {}
                    if isinstance(a, list):
                        a = a[0] if a else {}
                    qq, aa = clean(q.get("name", "")), strip_tags(a.get("text", ""))
                    if qq and aa:
                        out.append((qq, aa))
    return out


def sections(raw):
    """H2 + đoạn văn đầu tiên (tới H2 kế tiếp), chỉ trong thân bài."""
    body = raw
    m = re.search(r'<div class="art-body">', raw)
    if m:
        body = raw[m.start():]
    stop = re.search(r"<h2[^>]*>\s*Câu hỏi thường gặp", body)
    if stop:
        body = body[:stop.start()]
    out = []
    parts = re.split(r"(<h2\b[^>]*>.*?</h2>)", body, flags=re.S)
    for i in range(1, len(parts) - 1, 2):
        h = parts[i]
        title = strip_tags(h)
        if not title or BAD_H2.search(title) or len(title) < 8:
            continue
        idm = re.search(r'\bid="([^"]+)"', h)
        ps = [strip_tags(p) for p in re.findall(r"<p\b[^>]*>(.*?)</p>", parts[i + 1], re.S)]
        ps = [p for p in ps if len(p) > 40]
        if not ps:
            continue
        text = ps[0] if len(ps[0]) >= 220 or len(ps) == 1 else ps[0] + " " + ps[1]
        out.append((title, cut(text), idm.group(1) if idm else ""))
    return out


def main():
    os.chdir(ROOT)
    rows, plist, n_faq, n_muc, pages = [], [], 0, 0, 0
    for f in sorted(glob.glob("*.html")):
        if f in SKIP or f.startswith(("_", "demo")):
            continue
        raw = open(f, encoding="utf-8").read()
        if 'lang="vi"' not in raw[:400]:
            continue
        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', raw, re.I):
            continue
        slug = f[:-5]
        url = "/" if slug == "index" else "/" + slug
        tm = re.search(r"<title>(.*?)</title>", raw, re.S)
        title = re.split(r"\s+[|—–-]\s+Nam\s+Ban\s+Panorama", clean(tm.group(1)) if tm else slug)[0].strip()
        pages += 1
        pi = len(plist)
        plist.append([url, title])
        for q, a in faqs(raw):
            rows.append([0, q, cut(a), pi, ""])
            n_faq += 1
        if slug in NO_SECTIONS:
            continue
        for h, a, hid in sections(raw):
            rows.append([1, h, a, pi, hid])
            n_muc += 1
    # Tin mới: mỗi mục .tl-item của /nam-ban-co-gi-moi thành một dòng (loại 2), dẫn về bài nhà của tin
    # (tl-link) nếu có, không thì về trang tin. Trang tin là hub nên không lấy mục H2 ở trên.
    n_tin = 0
    idx = {p[0]: i for i, p in enumerate(plist)}
    if "/nam-ban-co-gi-moi" in idx and os.path.exists("nam-ban-co-gi-moi.html"):
        raw = open("nam-ban-co-gi-moi.html", encoding="utf-8").read()
        for blk in re.findall(r'<div class="tl-item"[^>]*>(.*?)\n\s*</div>\s*(?=<div class="tl-item"|</div>|<!--)', raw, re.S):
            dm = re.search(r'<div class="tl-date">(.*?)</div>', blk, re.S)
            tm = re.search(r'<div class="tl-title">(.*?)</div>', blk, re.S)
            sm = re.search(r'<div class="tl-sum"[^>]*>(.*?)</div>', blk, re.S)
            lm = re.search(r'<a class="tl-link" href="/?([^"#?]+)', blk)
            if not (tm and sm):
                continue
            pi = idx.get("/" + lm.group(1), idx["/nam-ban-co-gi-moi"]) if lm else idx["/nam-ban-co-gi-moi"]
            date = strip_tags(dm.group(1)) if dm else ""
            rows.append([2, strip_tags(tm.group(1)), cut((date + " — " if date else "") + strip_tags(sm.group(1))), pi, ""])
            n_tin += 1
    # Gọn: mỗi dòng [loại 0=hỏi–đáp 1=mục bài 2=tin, câu hỏi/tiêu đề mục, trả lời, chỉ số trang, neo #id];
    # bỏ dấu làm ở trình duyệt lúc tải (vài chục mili-giây), đỡ gần nửa dung lượng.
    data = {"v": 2, "pages": plist, "rows": rows}
    out = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    open("chat-index.json", "w", encoding="utf-8").write(out)
    import gzip
    print(f"Đã ghi chat-index.json: {pages} trang · {n_faq} hỏi–đáp · {n_muc} mục bài · {n_tin} tin · "
          f"{len(out.encode()) // 1024} KB · gzip ~{len(gzip.compress(out.encode())) // 1024} KB")


if __name__ == "__main__":
    main()
