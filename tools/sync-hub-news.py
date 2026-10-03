#!/usr/bin/env python3
"""Đồng bộ khối "Nam Ban có gì mới" trên hub /nam-ban từ /nam-ban-co-gi-moi.

/nam-ban-co-gi-moi là nguồn (dòng thời gian, mới nhất trên cùng); /nam-ban chỉ hiện
3 mục đầu. Script ghi thẳng vào HTML (không dùng JS) để Googlebot và bot AI đọc được.

- Lấy 3 `.tl-item` đầu tiên: ngày, tiêu đề (giữ nguyên HTML, kể cả &nbsp;), link bài nhà.
  Mục không có link bài nhà thì dẫn về /nam-ban-co-gi-moi.
- Dòng mô tả ngắn dưới tiêu đề: chỉ hiện khi mục tin có `data-hub-sum="…"` viết tay.
  Không tự cắt câu từ đoạn tóm tắt — câu cắt dở đọc rất xấu.
- Chỉ ghi giữa hai marker HUB-NEWS:START / HUB-NEWS:END. Có đổi thì cập nhật
  dateModified của /nam-ban theo giờ Việt Nam và lastmod của /nam-ban trong sitemap.xml.

Chạy: python3 tools/sync-hub-news.py   (workflow hub-news-sync.yml tự chạy khi trang tin đổi)
"""
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'nam-ban-co-gi-moi.html'
SITEMAP = ROOT / 'sitemap.xml'
HUB = ROOT / 'nam-ban.html'
N = 3
START = '<!-- HUB-NEWS:START (sinh bởi tools/sync-hub-news.py từ /nam-ban-co-gi-moi — đừng sửa tay) -->'
END = '<!-- HUB-NEWS:END -->'

A = ('<a href="{href}" style="display:block;text-decoration:none;padding:14px 0;'
     'border-top:1px solid var(--line);{last}">')
DATE = ('<span style="display:block;font-family:\'Fraunces\',serif;font-weight:600;font-size:12px;'
        'letter-spacing:.5px;color:var(--forest);margin-bottom:4px;">{}</span>')
TITLE = ('<span style="display:block;font-family:\'Fraunces\',serif;font-weight:500;font-size:16px;'
         'line-height:1.3;color:var(--ink);margin-bottom:3px;text-wrap:balance;">{}</span>')
SUM = ('<span style="display:block;font-size:13.5px;line-height:1.6;color:var(--muted);'
       'font-weight:300;">{}</span>')


def items(src):
    body = src[src.index('<div class="tl">'):]
    out = []
    for m in re.finditer(r'<div class="tl-item"([^>]*)>(.*?)\n    </div>', body, re.S):
        attrs, inner = m.group(1), m.group(2)
        date = re.search(r'<div class="tl-date">(.*?)</div>', inner, re.S)
        title = re.search(r'<div class="tl-title">(.*?)</div>', inner, re.S)
        link = re.search(r'<a class="tl-link" href="([^"]+)"', inner)
        hs = re.search(r'data-hub-sum="([^"]*)"', attrs)
        if not (date and title):
            continue
        href = link.group(1) if link else 'nam-ban-co-gi-moi'
        if not href.startswith(('/', 'http')):
            href = '/' + href
        out.append((date.group(1).strip(), title.group(1).strip(), href, hs.group(1) if hs else ''))
        if len(out) == N:
            break
    return out


def block(rows):
    lines = [START]
    for i, (date, title, href, hs) in enumerate(rows):
        last = 'border-bottom:1px solid var(--line);' if i == len(rows) - 1 else ''
        lines.append('        ' + A.format(href=href, last=last))
        lines.append('          ' + DATE.format(date))
        lines.append('          ' + TITLE.format(title))
        if hs:
            lines.append('          ' + SUM.format(hs))
        lines.append('        </a>')
    lines.append('        ' + END)
    return '\n'.join(lines)


def main():
    src = SRC.read_text(encoding='utf-8')
    hub = HUB.read_text(encoding='utf-8')
    rows = items(src)
    if len(rows) < N:
        sys.exit(f'!! chỉ đọc được {len(rows)} mục tin — dừng, không ghi đè hub')
    if hub.count(START) != 1 or hub.count(END) != 1:
        sys.exit('!! nam-ban.html thiếu hoặc thừa marker HUB-NEWS')
    a = hub.index(START)
    b = hub.index(END) + len(END)
    new = hub[:a] + block(rows) + hub[b:]
    if new == hub:
        print('Không đổi: hub đã khớp 3 tin mới nhất.')
        return
    now = datetime.now(timezone(timedelta(hours=7))).strftime('%Y-%m-%dT%H:%M:00+07:00')
    new, n = re.subn(r'("dateModified": ")[^"]+(")', r'\g<1>' + now + r'\g<2>', new, count=1)
    if n != 1:
        sys.exit('!! không tìm thấy dateModified trong nam-ban.html')
    HUB.write_text(new, encoding='utf-8')
    sm = SITEMAP.read_text(encoding='utf-8')
    sm2 = re.sub(r'(<loc>https://nambanpanorama.com/nam-ban</loc><lastmod>)[^<]*', r'\g<1>' + now[:10], sm, count=1)
    if sm2 != sm:
        SITEMAP.write_text(sm2, encoding='utf-8')
    print('Đã cập nhật hub:', ' · '.join(re.sub('<[^>]+>|&nbsp;', ' ', r[1])[:50] for r in rows))


if __name__ == '__main__':
    main()
