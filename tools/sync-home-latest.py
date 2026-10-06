#!/usr/bin/env python3
"""Khối "Mới cập nhật" trên trang chủ — 6 bài tiếng Việt đăng gần nhất (theo datePublished trong JSON-LD).

Ghi HTML tĩnh giữa <!-- HOME-LATEST:START --> và <!-- HOME-LATEST:END --> trong index.html (không JS — Googlebot và
bot AI đọc được ngay), rồi bump <lastmod> của trang chủ trong sitemap.xml khi danh sách đổi.
Lý do (6/10/2026): 24 URL "đã phát hiện / chưa biết URL" trong Search Console đều là bài mới, trung vị 2–4 trang link
vào (trang đã index: 6), và trang chủ — trang Google ghé nhiều nhất — không link tới bài nào trong số đó.
Chạy: python3 tools/sync-home-latest.py   (workflow home-latest.yml tự chạy khi có trang .html đổi trên main)
Không đổi gì thì không ghi file.
"""
import glob, html, json, os, re, datetime as dt

N = 6
SKIP = {"index", "nam-ban", "dat", "dau-tu", "hoi-nhanh", "trao-doi", "doc-lo-dat", "brief", "nam-ban-co-gi-moi",
        "namban-index", "404", "ve-panorama", "doc-nhanh"}
ARTICLE = {"Article", "NewsArticle", "BlogPosting", "Report", "AnalysisNewsArticle"}

def types(o):
    t = o.get("@type") if isinstance(o, dict) else None
    return set(t) if isinstance(t, list) else ({t} if t else set())

rows = []
for f in sorted(glob.glob("*.html")):
    slug = f[:-5]
    if slug in SKIP or slug.startswith(("_", "demo")):
        continue
    s = open(f, encoding="utf-8").read()
    if 'lang="vi"' not in s[:400] or re.search(r'<meta name="robots" content="[^"]*noindex', s):
        continue
    pub = None
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(j)
        except Exception:
            continue
        for o in (d.get("@graph", [d]) if isinstance(d, dict) else d):
            if isinstance(o, dict) and types(o) & ARTICLE and o.get("datePublished"):
                pub = str(o["datePublished"])
                break
        if pub:
            break
    if not pub:
        continue
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    if not h1:
        continue
    title = " ".join(html.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).replace("\xa0", " ").split())
    rows.append((pub, slug, title))

rows.sort(key=lambda r: (r[0], r[1]), reverse=True)
top = rows[:N]

def d_vi(p):
    y, m, d = p[:10].split("-")
    return f"{int(d)}/{int(m)}/{y}"

def nb(t):  # hai chữ cuối dính nhau, chống rớt chữ; cặp số "500–700" không bị bẻ ở dấu gạch
    i = t.rfind(" ")
    out = html.escape(t) if i < 0 else html.escape(t[:i]) + "&nbsp;" + html.escape(t[i + 1:])
    return re.sub(r"(\d[\d.,]*–\d[\d.,]*)", r'<span style="white-space:nowrap">\1</span>', out)

items = "\n".join(
    f'      <a href="/{slug}"><span><span class="kb-t">{nb(title)}</span><br>'
    f'<span class="kb-s"><time datetime="{pub[:10]}">Đăng {d_vi(pub)}</time></span></span><span class="kb-n">→</span></a>'
    for pub, slug, title in top)
block = f"""<!-- HOME-LATEST:START (sinh bởi tools/sync-home-latest.py — đừng sửa tay) -->
<section class="reveal home-latest" id="moi-cap-nhat">
  <div class="wrap">
    <div class="sechead"><span class="idx">04</span><h2 class="kicker" style="margin:0;">Mới cập nhật</h2></div>
    <div class="kb">
{items}
    </div>
  </div>
</section>
<!-- HOME-LATEST:END -->"""

p = "index.html"
s = open(p, encoding="utf-8").read()
a = s.index("<!-- HOME-LATEST:START")
b = s.index("<!-- HOME-LATEST:END -->") + len("<!-- HOME-LATEST:END -->")
if s[a:b] == block:
    print("Khối Mới cập nhật đã khớp, không ghi.")
    raise SystemExit(0)
open(p, "w", encoding="utf-8").write(s[:a] + block + s[b:])
today = dt.datetime.now(dt.timezone(dt.timedelta(hours=7))).strftime("%Y-%m-%d")
sm = open("sitemap.xml", encoding="utf-8").read()
sm2 = re.sub(r"(<loc>https://nambanpanorama.com/</loc><lastmod>)[^<]*", r"\g<1>" + today, sm, count=1)
if sm2 != sm:
    open("sitemap.xml", "w", encoding="utf-8").write(sm2)
print("Đã ghi khối Mới cập nhật:", " · ".join(f"{d_vi(p_)} {s_}" for p_, s_, _ in top))
