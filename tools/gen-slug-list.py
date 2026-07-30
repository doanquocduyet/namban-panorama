#!/usr/bin/env python3
"""Sinh danh sách slug + tiêu đề + hub mọi trang thật (bỏ demo/_mau/404).
Cột hub = bài được liệt kê ở hub nào (nam-ban / dat / dau-tu / cap-nhat), lấy từ
membership thật của các trang hub + badge chuẩn hóa. Chạy lại sau khi thêm/xóa/đổi hub bài."""
import glob, re

# 1) hub membership: mỗi hub page liệt kê slug nào
HUBS = {
    'nam-ban.html': 'Về Nam Ban',
    'dat.html': 'Về Đất',
    'dau-tu.html': 'Đầu tư',
    'nam-ban-co-gi-moi.html': 'Cập nhật',
}
member = {}  # slug -> set(hub labels)
for hf, label in HUBS.items():
    try:
        h = open(hf, encoding='utf-8').read()
    except FileNotFoundError:
        continue
    for slug in re.findall(r'href="/?([a-z0-9\-]+)(?:\.html)?"', h):
        if slug in ('nam-ban', 'dat', 'dau-tu', 'trao-doi', 'index') or slug.startswith('favicon'):
            continue
        member.setdefault(slug, set()).add(label)

rows = []
for f in sorted(glob.glob('*.html')):
    if f.startswith('demo-') or f.startswith('_mau') or f == '404.html':
        continue
    slug = f[:-5]
    h = open(f, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', h, re.S)
    t = (m.group(1) if m else '').split('|')[0].split('—')[0].strip()
    if not t:
        m2 = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
        t = re.sub('<[^>]+>', '', m2.group(1)).strip() if m2 else '(?)'
    # badge chuẩn hóa (nếu có) làm phụ trợ khi bài chưa nằm hub nào
    mb = re.search(r'<span class="issue-badge">([^<]*)</span>', h)
    badge = mb.group(1).strip() if mb else ''
    hub = ' + '.join(sorted(member.get(slug, set()))) or (badge if badge else '—')
    rows.append((slug, t, hub))

out = ["# Danh sách bài trên nambanpanorama.com", "",
       f"Tự sinh bằng `tools/gen-slug-list.py`. Tổng: **{len(rows)}** trang. "
       "Cột hub = hub thật liệt kê bài (sau dedup mỗi bài về đúng 1 hub). "
       "Chạy lại sau mỗi lần thêm/xóa/đổi hub bài.", "",
       "| slug | tiêu đề | hub |", "|---|---|---|"]
for slug, t, hub in rows:
    out.append(f"| `/{slug}` | {t} | {hub} |")
open('docs/danh-sach-bai.md', 'w', encoding='utf-8').write("\n".join(out) + "\n")
print("Đã ghi docs/danh-sach-bai.md —", len(rows), "trang")
