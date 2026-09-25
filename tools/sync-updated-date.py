#!/usr/bin/env python3
"""Ghi sẵn dòng "Cập nhật d/m/yyyy" vào HTML gốc của bài (thẻ <time id="pm-updated">), lấy từ dateModified
trong JSON-LD Article — đúng như panorama-utils.js vẫn chèn bằng JS. Lý do (25/9/2026): phần lớn bot AI
(GPTBot, PerplexityBot, ClaudeBot…) không chạy JavaScript nên trước đây chỉ thấy "Cập nhật tháng 9, 2026",
không thấy ngày chính xác. Giao diện không đổi: cùng chỗ, cùng chữ, cùng kiểu.

Luật giống JS: chỉ hiện khi dateModified > datePublished. Chạy lại bao nhiêu lần cũng được (tự thay bản cũ).
Chạy sau mỗi lần sửa bài (đổi dateModified):  python3 tools/sync-updated-date.py
Bỏ qua namban-index (header riêng, bộ sinh riêng) và trang không có Article."""
import re, glob, json, sys

SPAN = ('<time id="pm-updated" datetime="{iso}" style="font-size:11px;letter-spacing:2px;text-transform:uppercase;'
        'color:var(--muted,#6e6759);margin-left:14px;">{label}</time>')
DIV = ('<div id="pm-updated" style="font-size:12px;letter-spacing:1px;text-transform:uppercase;'
       'color:var(--muted,#6e6759);margin-top:8px;"><time datetime="{iso}">{label}</time></div>')
OLD = re.compile(r'(?<!<span class="issue-date">)<time id="pm-updated"[^>]*>[^<]*</time>|<div id="pm-updated"[^>]*><time[^>]*>[^<]*</time></div>')
SKIP = {"namban-index.html", "_mau-bai-viet.html"}

def dates(s):
    pub = mod = None
    for b in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', s):
        try: j = json.loads(b)
        except Exception: continue
        for o in (j.get("@graph", [j]) if isinstance(j, dict) else j):
            if isinstance(o, dict) and o.get("@type") in ("Article", "NewsArticle", "BlogPosting"):
                pub = str(o.get("datePublished") or "")[:10] or pub
                mod = str(o.get("dateModified") or "")[:10] or mod
    return pub, mod

changed = added = removed = 0
for p in sorted(glob.glob("*.html") + glob.glob("*/*.html")):
    if p in SKIP or p.startswith(("tools/", "docs/", "scripts/")): continue
    s = open(p, encoding="utf-8").read()
    pub, mod = dates(s)
    t = OLD.sub("", s)
    if mod and re.fullmatch(r"\d{4}-\d{2}-\d{2}", mod) and not (pub and mod <= pub):
        y, m, d = mod.split("-")
        lab = ("Cập nhật " if 'lang="vi"' in s[:600] else "Updated ") + f"{int(d)}/{int(m)}/{y}"
        # ô ngày vốn ghi "CẬP NHẬT THÁNG 9, 2026" → thay bằng ngày chính xác ngay trong ô (khỏi hai dòng "cập nhật")
        u = re.search(r'<span class="issue-date">(?:\s*[Cc](?:ẬP NHẬT|ập nhật)[^<]*|<time id="pm-updated" datetime="[^"]*">[^<]*</time>)</span>', t)
        i = re.search(r'<span class="issue-date">[^<]*</span>', t)
        if u:
            t = t[:u.start()] + f'<span class="issue-date"><time id="pm-updated" datetime="{mod}">{lab}</time></span>' + t[u.end():]
        elif i:
            t = t[:i.end()] + SPAN.format(iso=mod, label=lab) + t[i.end():]
        else:
            h = re.search(r'<div class="art-header">[\s\S]*?</h1>', t)
            if not h:
                if t != s: open(p, "w", encoding="utf-8").write(t); removed += 1
                continue
            t = t[:h.end()] + DIV.format(iso=mod, label=lab) + t[h.end():]
    if t != s:
        open(p, "w", encoding="utf-8").write(t); changed += 1
        added += t.count('id="pm-updated"')
print(f"OK: {changed} file đổi · {added} dòng ngày tĩnh · {removed} file gỡ dòng cũ")
