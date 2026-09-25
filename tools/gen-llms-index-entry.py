#!/usr/bin/env python3
"""Sinh lại entry /namban-index trong llms-full.txt từ HTML hiện tại của trang.
Chạy sau tools/gen-index-history.py khi bố cục hoặc chữ của trang Index đổi.
Kiểm Luật 25: tổng URL không đổi, không khối nào >1 URL, không khối rỗng."""
import re, html, sys

s = open("namban-index.html", encoding="utf-8").read()
desc = re.search(r'<meta name="description" content="([^"]+)"', s).group(1)
body = s[s.index('<div class="idx-header">'):s.index('<div class="share-row">')]
body = re.sub(r"<(script|svg|button)[\s\S]*?</\1>", "", body)
tables = []
def tbl(m):
    out = []
    for tr in re.findall(r"<tr>([\s\S]*?)</tr>", m.group(0)):
        cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).replace("\xa0", " ").strip() for c in re.findall(r"<t[hd][^>]*>([\s\S]*?)</t[hd]>", tr)]
        out.append(" | ".join(cells))
    tables.append("\n".join(out)); return f"<p>@@TBL{len(tables)-1}@@</p>"
body = re.sub(r"<table[\s\S]*?</table>", tbl, body)
lines = []
pat = r'<(h1|h2|h3|p|li|dt|dd|figcaption|div class="(?:price-tier|price-range|price-unit|price-desc|price-band|price-total|obs-text|idx-tile-t|idx-tile-d|idx-eyebrow)")[^>]*>([\s\S]*?)</(?:h1|h2|h3|p|li|dt|dd|figcaption|div)>'
for m in re.finditer(pat, body):
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(2))).replace("\xa0", " ")).strip()
    mm = re.fullmatch(r"@@TBL(\d+)@@", t)
    if mm: lines.append(tables[int(mm.group(1))]); continue
    if t: lines.append(t)
H = "## Giá đất Nam Ban 2026: bảng giá rao theo từng loại"
entry = f"{H}\n\nURL: https://nambanpanorama.com/namban-index\n\nTóm tắt: {desc}\n\n" + "\n\n".join(lines) + "\n"

L = open("llms-full.txt", encoding="utf-8").read(); before = L.count("https://nambanpanorama.com/")
a = L.index(H); b = L.index("\n---\n", a)
L2 = L[:a] + entry + L[b:]
blocks = L2.split("\n---\n")
multi = [i for i, k in enumerate(blocks) if k.count("\nURL: https://") > 1]; empty = [i for i, k in enumerate(blocks) if not k.strip()]
after = L2.count("https://nambanpanorama.com/")
if before != after or multi or empty:
    sys.exit(f"DỪNG (Luật 25): URL {before}->{after}, khối >1 URL {multi}, khối rỗng {empty}")
open("llms-full.txt", "w", encoding="utf-8").write(L2)
print(f"OK: entry Index {len(lines)} dòng · URL {after}")
