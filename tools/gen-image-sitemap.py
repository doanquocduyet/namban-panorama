#!/usr/bin/env python3
"""Sinh image-sitemap.xml từ ảnh THẬT đang dùng trong từng trang.

Chạy lại sau mỗi lần thêm/xóa/đổi ảnh hoặc thêm bài:
    python3 tools/gen-image-sitemap.py

Chỉ ghi <image:loc>. Bốn thẻ <image:caption>, <image:title>,
<image:geo_location>, <image:license> đã bị Google ngừng dùng từ 6/8/2022
(developers.google.com/search/blog/2022/05/spring-cleaning-sitemap-extensions)
nên thêm vào là công cốc — thông tin đó đi bằng ImageObject JSON-LD trong HTML.
"""
import re, glob, os, sys

SITE = "https://nambanpanorama.com"
SKIP = {"_mau-bai-viet.html", "demo-selection.html"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def collect():
    os.chdir(ROOT)
    pages = sorted(glob.glob("*.html") + glob.glob("*/*.html"))
    out = []
    for f in pages:
        if os.path.basename(f) in SKIP:
            continue
        raw = open(f, encoding="utf-8").read()
        c = re.search(r'<link rel="canonical" href="([^"]+)"', raw)
        if not c:
            continue
        imgs = []
        # ảnh hiển thị trong thân trang, giữ thứ tự xuất hiện
        for m in re.finditer(r'<img\b[^>]*src="/images/([^"]+)"', raw):
            s = m.group(1)
            if s not in imgs:
                imgs.append(s)
        # ảnh chia sẻ (og:image) cũng đáng cho Google biết
        for m in re.finditer(r'og:image" content="[^"]*/images/([^"]+)"', raw):
            if m.group(1) not in imgs:
                imgs.append(m.group(1))
        imgs = [s for s in imgs if os.path.exists(os.path.join("images", s))]
        if imgs:
            out.append((c.group(1), imgs))
    return out


def main():
    data = collect()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
             ' xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    n = 0
    for url, imgs in data:
        lines.append("  <url>")
        lines.append("    <loc>%s</loc>" % url)
        for s in imgs:
            lines.append("    <image:image><image:loc>%s/images/%s</image:loc></image:image>" % (SITE, s))
            n += 1
        lines.append("  </url>")
    lines.append("</urlset>")
    open(os.path.join(ROOT, "image-sitemap.xml"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("Đã ghi image-sitemap.xml: %d trang · %d lượt ảnh" % (len(data), n))


if __name__ == "__main__":
    main()
