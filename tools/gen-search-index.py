#!/usr/bin/env python3
"""Sinh search-index.json cho ô tìm kiếm trên trang chủ và thanh menu.

Chạy CLIENT-SIDE, không backend. Mỗi trang tiếng Việt góp một dòng:
slug · tiêu đề · mô tả ngắn · từ khoá · hub.

Ba chỗ dễ sai, đã xử sẵn:
  1. `&nbsp;` (Luật 13d) — phải html.unescape() rồi bỏ \xa0, nếu không
     "Nam Ban" trong index thành "Nam\xa0Ban" và gõ "nam ban" không ra.
  2. Tiêu đề có đuôi "| Namban Panorama" — cắt, để không trang nào cũng
     khớp khi người ta gõ "panorama".
  3. Trang tiếng nước ngoài (en/ fr/ zh/ ko/ ja/) KHÔNG vào index này —
     ô search nằm ở trang tiếng Việt, trộn vào là ra kết quả người đọc
     không mở được.

Trường `f` = chuỗi đã bỏ dấu, dựng sẵn lúc build. Làm ở đây thay vì làm
trong trình duyệt để máy người đọc khỏi phải chuẩn hoá 166 dòng mỗi lần gõ.

    python3 tools/gen-search-index.py
"""
import glob
import gzip
import html
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {"_mau-bai-viet.html", "demo-selection.html", "404.html"}

# Hub lấy từ badge chuyên mục có sẵn trên trang.
HUBS = {"Về Nam Ban", "Về Đất", "Đầu tư", "Cập nhật", "Tra cứu"}


def clean(s):
    """html.unescape rồi bỏ \xa0 — Luật 13d."""
    return re.sub(r"\s+", " ", html.unescape(s).replace("\xa0", " ")).strip()


def fold(s):
    """Bỏ dấu để gõ 'ho bai cong' vẫn ra 'hồ Bãi Công'. Đ/đ phải xử riêng
    vì NFD không tách được dấu gạch ngang của nó."""
    s = s.lower().replace("đ", "d")
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def main():
    os.chdir(ROOT)
    rows = []
    for f in sorted(glob.glob("*.html")):
        if f in SKIP:
            continue
        raw = open(f, encoding="utf-8").read()
        if 'lang="vi"' not in raw[:400]:
            continue
        m = re.search(r"<title>(.*?)</title>", raw, re.S)
        if not m:
            continue
        title = clean(m.group(1)).split("|")[0].strip()
        d = re.search(r'<meta name="description" content="(.*?)">', raw, re.S)
        k = re.search(r'<meta name="keywords" content="(.*?)">', raw, re.S)
        b = re.search(r'issue-badge">(.*?)</span>', raw, re.S)
        desc = clean(d.group(1)) if d else ""
        hub = clean(b.group(1)) if b else ""
        if hub not in HUBS:
            hub = ""
        row = {
            "s": f[:-5],
            "t": title,
            "d": desc[:130],
            "h": hub,
        }
        # Hai chuỗi dò, để xếp hạng được: khớp trong TIÊU ĐỀ đáng giá hơn
        # khớp trong mô tả hay từ khoá. Gộp một chuỗi thì gõ "ho bai cong"
        # ra bài đường Hà Bắc trước bài hồ Bãi Công — đã vấp thật.
        row["ft"] = fold(title)
        row["f"] = fold(" ".join([title, desc, clean(k.group(1)) if k else ""]))
        rows.append(row)

    out = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    open("search-index.json", "w", encoding="utf-8").write(out)
    n = len(out.encode())
    print("Đã ghi search-index.json: %d trang · %d KB · gzip ~%d KB"
          % (len(rows), n // 1024, len(gzip.compress(out.encode())) // 1024))


if __name__ == "__main__":
    main()
