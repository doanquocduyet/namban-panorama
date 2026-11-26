#!/usr/bin/env python3
"""Báo (không chặn) chỗ còn ghi ngày đo / kỳ Index cũ ở các trang "giá hiện tại" và trang EN (26/11/2026).

Chạy sau gen-index-history.py trong index-weekly.yml. Bộ sinh tự thay số ở danh sách LIVE; trang EN
/en/land-prices-nam-ban có đoạn kể theo tháng nên vẫn sửa tay mỗi tháng — bước này nhắc khi nó lệch kỳ.
In dòng ::warning:: cho GitHub; thoát 0 dù có lệch.
"""
import json, re, html, os

st = json.load(open("tools/idx-live-state.json", encoding="utf-8"))
ky, d_full = st["ky"], st["d_full"]  # "11/2026", "25/11/2026"
EN_MONTH = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
dd, mm, yy = map(int, d_full.split("/"))
en_date = f"{dd} {EN_MONTH[mm - 1]} {yy}"
en_ky = f"{EN_MONTH[int(ky.split('/')[0]) - 1]} {ky.split('/')[1]}"

LIVE = ["hoi-nhanh.html", "dat-gan-da-lat.html", "dat-nam-ban-gia-re.html", "mua-dat-nam-ban-500-trieu-1-ty.html",
        "vung-ven-da-lat-nao-tot-nhat.html"]
warn = []

def norm(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")

for f in LIVE:
    if not os.path.exists(f): continue
    t = norm(open(f, encoding="utf-8").read())
    for m in re.finditer(r"(?:[Đđ]o tới|\(mốc) (\d{1,2}/\d{1,2}/20\d\d)", t):
        if m.group(1) != d_full: warn.append(f"{f}: còn ngày đo {m.group(1)} (kỳ chính đo tới {d_full})")
    for m in re.finditer(r"(?:[Gg]iá rao|Index) tháng (\d{1,2}/20\d\d)", t):
        if m.group(1) != ky: warn.append(f"{f}: còn 'tháng {m.group(1)}' gắn với giá rao (kỳ chính {ky})")

f = "en/land-prices-nam-ban.html"
if os.path.exists(f):
    t = norm(open(f, encoding="utf-8").read())
    for m in re.finditer(r"(?:measured to|[Ll]ast measured) (\d{1,2} [A-Z][a-z]+ 20\d\d)", t):
        if m.group(1) != en_date: warn.append(f"{f}: còn '{m.group(0)}' (kỳ chính đo tới {en_date}) — sửa tay số + đoạn kể tháng")
    for m in re.finditer(r"Asking prices, ([A-Z][a-z]+ 20\d\d)", t):
        if m.group(1) != en_ky: warn.append(f"{f}: còn kỳ '{m.group(1)}' (kỳ chính {en_ky})")

L = open("llms.txt", encoding="utf-8").read().split("\n") if os.path.exists("llms.txt") else []
urls = ["https://nambanpanorama.com/" + x[:-5] for x in LIVE] + ["https://nambanpanorama.com/en/land-prices-nam-ban"]
for line in L:
    if not any(u + " " in line or u + ")" in line for u in urls): continue
    for m in re.finditer(r"đo tới (\d{1,2}/\d{1,2}/20\d\d)", line):
        if m.group(1) != d_full: warn.append(f"llms.txt: dòng {line[:70]}… còn 'đo tới {m.group(1)}'")

for w in dict.fromkeys(warn): print(f"::warning::Index lệch kỳ — {w}")
print(f"check-idx-stale: kỳ {ky}, đo tới {d_full}; {len(set(warn))} chỗ lệch")
