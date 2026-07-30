#!/usr/bin/env python3
"""Sinh danh sách slug + tiêu đề mọi trang thật (bỏ demo/_mau/404). Chạy lại sau khi thêm/xóa bài."""
import glob,re
rows=[]
for f in sorted(glob.glob('*.html')):
    if f.startswith('demo-') or f.startswith('_mau') or f=='404.html': continue
    slug=f[:-5]
    h=open(f,encoding='utf-8').read()
    m=re.search(r'<title>(.*?)</title>',h,re.S)
    t=(m.group(1) if m else '').split('|')[0].split('—')[0].strip()
    if not t:
        m2=re.search(r'<h1[^>]*>(.*?)</h1>',h,re.S); t=re.sub('<[^>]+>','',m2.group(1)).strip() if m2 else '(?)'
    rows.append((slug,t))
out=[f"# Danh sách bài trên nambanpanorama.com","",
     f"Tự sinh bằng `tools/gen-slug-list.py`. Tổng: **{len(rows)}** trang. Chạy lại sau mỗi lần thêm/xóa bài.","",
     "| slug | tiêu đề |","|---|---|"]
for slug,t in rows:
    out.append(f"| `/{slug}` | {t} |")
open('docs/danh-sach-bai.md','w',encoding='utf-8').write("\n".join(out)+"\n")
print("Đã ghi docs/danh-sach-bai.md —",len(rows),"trang")
