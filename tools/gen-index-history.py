#!/usr/bin/env python3
"""Sinh mục 02 (Giá đất Nam Ban đang tăng hay giảm?) và mục 06 của namban-index.html từ data/index/monthly.json,
thêm dòng "trung vị tin rao" vào 3 ô mục 01. Chạy: python3 tools/gen-index-history.py
Chỉ thay phần giữa các cặp marker IDX-HIST / IDX-OBS; cập nhật Dataset JSON-LD + dateModified.
Người đọc chỉ cần: loại đất nào · giá trung bình bao nhiêu · tăng hay giảm. Không báo cáo tin đăng.
Số từ sổ thực địa Panorama (data/index/editorial.json, nếu có) được ghi dấu † — dùng khi tin rao chưa đủ 10."""
import json, re, os, datetime as dt

P = "namban-index.html"
D = json.load(open("data/index/monthly.json", encoding="utf-8"))
ED = json.load(open("data/index/editorial.json", encoding="utf-8")) if os.path.exists("data/index/editorial.json") else {}
MIN_N = D["meta"].get("min_n", 10)
NOW = dt.datetime.now(dt.timezone(dt.timedelta(hours=7)))
GROUPS = [("tho_cu_duoi_2000", "Đất thổ cư dưới 2.000&nbsp;m²", "đất thổ cư dưới 2.000 m²"),
          ("nong_nghiep_tu_2000", "Đất nông nghiệp từ 2.000&nbsp;m²", "đất nông nghiệp từ 2.000 m²"),
          ("view", "Lô có view hồ, đồi, toàn cảnh", "lô có view")]

def tr(v): return f"{v/1e6:.2f}".replace(".", ",")
def month_vi(m): y, mo = m.split("-"); return f"{int(mo)}/{y}"
def val(m, key):
    """(median_vnd, n, nguồn) cho tháng m, nhóm key: tin rao đủ 10 → 'rao'; không thì sổ thực địa nếu có → 'so'; không thì None"""
    g = m["ghi_nhan"]["groups"][key]
    if g["median_vnd_m2"] is not None: return g["median_vnd_m2"], g["n"], "rao"
    e = ED.get(m["month"], {}).get(key)
    if e and e.get("median_vnd_m2"): return e["median_vnd_m2"], e.get("n"), "so"
    return None
def trend(cur, prev):
    d = (cur - prev) / prev * 100
    w = "đi ngang" if abs(d) < 3 else ("nhích lên" if 3 <= d <= 8 else "nhích xuống" if -8 <= d <= -3 else ("tăng" if d > 8 else "giảm"))
    return d, w

months = D["monthly"]; last = months[-1]; base = D["baseline"]
m_on = dt.date.fromisoformat(base["measured_on"]).strftime("%-d/%-m/%Y"); last_m = month_vi(last["month"])

# ---- ba ô + câu trả lời ----
cells = []; ans = []; live = {}
for key, label, low in GROUPS:
    cur = val(last, key)
    if not cur: continue
    prev = None
    for m in reversed(months[:-1]):
        v = val(m, key)
        if v: prev = (m["month"], v); break
    big = f'<div class="price-range">{tr(cur[0])} <span class="idx-unit">tr/m²</span></div>'
    src = f'{cur[1]} tin rao' if cur[2] == "rao" else 'sổ thực địa Panorama†'
    if prev:
        d, w = trend(cur[0], prev[1][0]); sign = "+" if d > 0 else "−"
        small = " <small>(mẫu nhỏ)</small>" if (cur[2] == "rao" and cur[1] < 20) or (prev[1][2] == "rao" and (prev[1][1] or 0) < 20) else ""
        cmp = f'So với tháng {month_vi(prev[0])} ({tr(prev[1][0])}): <b>{w}</b>&nbsp;{sign}{abs(d):.0f}&nbsp;%{small}'
        ans.append(f"{low.capitalize()} <strong>{tr(cur[0])} triệu/m²</strong> ({src}), so với tháng {month_vi(prev[0])} là {tr(prev[1][0])} — <strong>{w}</strong> ({sign}{abs(d):.0f}&nbsp;%).")
    else:
        cmp = "Chưa có tháng trước để so"
        ans.append(f"{low.capitalize()} <strong>{tr(cur[0])} triệu/m²</strong> ({src}).")
    cells.append(f'<div class="price-cell"><div class="price-tier">{label}</div>{big}<div class="price-unit">Tháng {last_m} · {src}</div><div class="price-desc">{cmp}</div></div>')
    live[key] = f'Trung vị tin rao {last_m}: <b>{tr(cur[0])} tr/m²</b> ({src})'
answer = f"Tháng {last_m} (đo tới {m_on}): " + " ".join(ans) + " Đây là giá rao trung vị, chưa phải giá đã&nbsp;chốt."

# ---- bảng tháng: chỉ tháng có ít nhất một nhóm đủ số ----
rows = []; shown = []
for m in reversed(months):
    vs = [val(m, k) for k, _, _ in GROUPS]
    if not any(vs): continue
    shown.append(m["month"])
    tag = ' <sup class="idx-tmp" title="tháng đang diễn ra, số tới ngày đo">tạm</sup>' if m["status"] == "partial" else ""
    tds = "".join(f'<td class="num"><b>{tr(v[0])}</b><small>{(str(v[1]) + " tin") if v[2] == "rao" else "sổ thực địa†"}</small></td>' if v else '<td class="num dash">—</td>' for v in vs)
    rows.append(f'<tr><th scope="row"><time datetime="{m["month"]}">{month_vi(m["month"])}</time>{tag}</th>{tds}</tr>')
first_shown = min(shown)
table = f'''<figure class="idx-fig pm-selectable">
<figcaption>Trung vị giá rao theo tháng, triệu đồng/m², xã Nam&nbsp;Ban Lâm&nbsp;Hà. Nguồn: Namban&nbsp;Index — tin rao công khai của 7 trang, gộp&nbsp;trùng, đo&nbsp;{m_on}.</figcaption>
<div class="idx-tblwrap"><table class="idx-tbl">
<thead><tr><th scope="col">Tháng</th>{"".join(f'<th scope="col" class="num">{lab}</th>' for _, lab, _ in GROUPS)}</tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody></table></div>
</figure>
<p class="idx-note">"—": tháng đó nhóm chưa đủ {MIN_N} tin rao, không tính. † Số từ sổ giao dịch thực địa của Panorama, dùng cho tháng tin rao chưa đủ. Bảng nối dài về trước khi có số thực địa; từ tháng 10/2026 mỗi tuần thêm một lần&nbsp;đo.</p>
<p class="idx-dl">Dữ liệu mở: <a href="/data/index/monthly.json">monthly.json</a> · <a href="/data/index/monthly.csv">monthly.csv</a> — trích dẫn tự do, ghi nguồn Namban&nbsp;Panorama.</p>'''

hist = f'''<div class="idx-section-label">02 — Diễn biến</div>
<h2 class="idx-section-title">Giá đất Nam Ban đang tăng hay giảm?</h2>
<p class="idx-answer">{answer}</p>
<div class="price-grid idx-now">{"".join(cells)}</div>
{table}'''

obs = f'''<p class="idx-answer">Namban Index theo dõi <strong>{base['n']} tin rao đang treo</strong> ở xã Nam&nbsp;Ban Lâm&nbsp;Hà (đo {m_on}) từ 7 trang công khai, gộp tin trùng, lọc đúng xã. Chúng tôi không đăng lại từng tin, không đăng tựa hay số điện thoại người rao — chỉ đăng số tổng hợp. Muốn biết một lô cụ thể đáng giá bao nhiêu, xem <a href="/dinh-gia-dat-nam-ban">vì sao hai lô cùng diện tích khác&nbsp;giá</a>.</p>'''

s = open(P, encoding="utf-8").read()
def replace_block(s, start_pat, end, body):
    st = re.search(start_pat, s).group(0); a = s.index(st) + len(st); b = s.index(end)
    return s[:a] + "\n" + body + "\n" + s[b:]
s = replace_block(s, r"<!-- IDX-HIST:START[^>]*-->", "<!-- IDX-HIST:END -->", hist)
s = replace_block(s, r"<!-- IDX-OBS:START[^>]*-->", "<!-- IDX-OBS:END -->", obs)

# ---- mục 01: dòng trung vị tin rao dưới "Tổng giá phổ biến" của 3 ô (thứ tự ô: nông nghiệp lớn · tách thửa thổ cư · view) ----
order = ["nong_nghiep_tu_2000", "tho_cu_duoi_2000", "view"]
s = re.sub(r'\n\s*<div class="price-live">.*?</div>', '', s, flags=re.S)
i = [0]
def _add(m):
    key = order[i[0]] if i[0] < len(order) else None; i[0] += 1
    return m.group(0) + (f'\n      <div class="price-live">{live[key]}</div>' if key in live else '')
s = re.sub(r'<div class="price-total">[^<]*</div>', _add, s, count=3)

CSS = """.idx-answer{font-size:16.5px;line-height:1.7;margin:0 0 14px;text-wrap:pretty}
.idx-now .price-cell{padding:22px 20px 18px}
.idx-now .price-range{font-size:30px}
.idx-unit{font-family:'Be Vietnam Pro',sans-serif;font-size:13px;color:var(--muted);letter-spacing:.2px}
.idx-now .price-desc b{font-weight:500;color:var(--ink)}
.idx-now .price-desc small{font-size:11.5px;color:var(--stone-text,#726a5c)}
.price-live{margin-top:8px;font-size:12.5px;color:var(--muted);line-height:1.45;font-style:normal}
.price-live b{font-weight:500;color:var(--forest)}
.idx-fig{margin:18px 0 10px}
.idx-fig figcaption{font-size:13px;color:var(--muted);line-height:1.5;margin:0 0 8px;text-wrap:pretty}
.idx-tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:3px;background:var(--card)}
.idx-tbl{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
.idx-tbl th,.idx-tbl td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;line-height:1.4}
.idx-tbl thead th{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:500;vertical-align:bottom}
.idx-tbl tbody th{font-weight:500;color:var(--ink);white-space:nowrap}
.idx-tbl .num{text-align:right}
.idx-tbl td b{font-family:'Fraunces',serif;font-weight:500;font-size:17px;color:var(--ink)}
.idx-tbl td small{display:block;font-size:11.5px;color:var(--muted)}
.idx-tbl td.dash{color:var(--stone);font-size:16px}
.idx-tbl tr:last-child th,.idx-tbl tr:last-child td{border-bottom:0}
.idx-tmp{font-size:10.5px;color:var(--muted);margin-left:4px;font-style:italic}
.idx-note{font-size:13.5px;color:var(--muted);line-height:1.6;margin:10px 0 0;text-wrap:pretty}
.idx-note a,.idx-dl a,.idx-answer a{color:var(--forest);text-decoration:none;border-bottom:1px solid var(--line)}
.idx-dl{font-size:13.5px;color:var(--muted);margin:10px 0 4px}
@media(max-width:600px){.idx-tbl{font-size:13px}.idx-tbl th,.idx-tbl td{padding:9px 8px}.idx-tbl td b{font-size:15.5px}.idx-tbl thead th{font-size:10px}.idx-answer{font-size:15.5px}.idx-now .price-range{font-size:27px}}
"""
if ".idx-answer{" in s:
    s = re.sub(r"\.idx-answer\{[\s\S]*?\n(?=</style>)", CSS, s, count=1)
else:
    s = s.replace('<style id="idx-v2">\n', '<style id="idx-v2">\n' + CSS, 1)

# ---- JSON-LD + dateModified ----
s = re.sub(r'"temporalCoverage": "[^"]*"', f'"temporalCoverage": "{first_shown}/{last["month"]}"', s, count=1)
s = re.sub(r'("@type": "Dataset",[\s\S]*?"dateModified": )"[^"]*"', lambda m: m.group(1) + f'"{NOW.date().isoformat()}"', s, count=1)
s = re.sub(r'("@type": "Article",[\s\S]*?"dateModified": )"[^"]*"', lambda m: m.group(1) + f'"{NOW.strftime("%Y-%m-%dT%H:%M:00+07:00")}"', s, count=1)
open(P, "w", encoding="utf-8").write(s)

for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S): json.loads(m.group(1))
for m in re.finditer(r"<style[^>]*>(.*?)</style>", s, re.S): assert m.group(1).count("{") == m.group(1).count("}")
for t in ["div", "figure", "table", "thead", "tbody", "tr", "th", "td", "p", "h2"]:
    o = len(re.findall(rf"<{t}\b[^>]*>", s)); c = len(re.findall(rf"</{t}>", s)); assert o == c, (t, o, c)
print("OK:", len(rows), "tháng trong bảng ·", len(cells), "ô · dateModified", NOW.strftime("%Y-%m-%d %H:%M"))
