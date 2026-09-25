#!/usr/bin/env python3
"""Sinh các khối số của namban-index.html từ data/index/monthly.json (+ data/prices.json, data/index/editorial.json nếu có).
Chạy: python3 tools/gen-index-history.py  (workflow index-weekly.yml chạy sau mỗi lần đo)

Chỉ thay phần giữa các cặp marker — đừng sửa tay bên trong:
  IDX-LEAD  header: một dòng kỳ (số nằm ngay ở bốn ô mục 01, không nhắc lại)
  IDX-NOW   mục 01: bốn ô giá kỳ này (trung vị + n + khoảng rao nửa đầu năm + ghi chú) + dòng dẫn sang lý do ở mục 04
  IDX-HIST  mục 02: câu kết luận + chiều giá từng loại (%, tháng so) + bảng tháng + chú thích
  IDX-DATA  mục 03: bảng Stats 6 cặp (đơn vị · loại giá · nguồn · ngưỡng · kỳ đo · kỳ tới) + một câu "không đăng lại tin"
  IDX-CITE  mục 07: ô trích dẫn có số của kỳ
  IDX-FAQ   khối FAQ hiển thị + toàn bộ FAQPage JSON-LD (2 câu sinh theo số + 5 câu tĩnh)
  IDX-GEN   CSS của các khối trên (trong <style id="idx-v2">)
Nếp: một bộ phân loại 4 nhóm cho mọi khối · số kèm n và ngày · "—" khi chưa đủ 10 tin · không in % khi mẫu hai kỳ khác hẳn.
Số từ sổ thực địa Panorama (data/index/editorial.json, nếu có) được ghi dấu † — dùng khi tin rao chưa đủ 10."""
import json, re, os, datetime as dt

P = "namban-index.html"
D = json.load(open("data/index/monthly.json", encoding="utf-8"))
PR = json.load(open("data/prices.json", encoding="utf-8"))
ED = json.load(open("data/index/editorial.json", encoding="utf-8")) if os.path.exists("data/index/editorial.json") else {}
MIN_N = D["meta"].get("min_n", 10)
NOW = dt.datetime.now(dt.timezone(dt.timedelta(hours=7)))
GROUPS = [("tach_thua_150_300", "Đất nền tách thửa 150–300&nbsp;m²", "đất nền tách thửa 150–300 m²"),
          ("lo_500_tho_cu", "Lô khoảng 500&nbsp;m² có thổ cư", "lô khoảng 500 m² có thổ cư"),
          ("dat_tren_1000", "Đất trên 1.000&nbsp;m²", "đất trên 1.000 m²"),
          ("view", "Lô có view hồ, đồi, toàn cảnh", "lô có view hồ, đồi, toàn cảnh")]
LABEL = {k: l for k, l, _ in GROUPS}; LOW = {k: lo for k, _, lo in GROUPS}
NOTE = {"tach_thua_150_300": "Nền nhỏ trong khu đã tách, có thổ cư, xây được ngay.",
        "lo_500_tho_cu": "Ngang 10–18&nbsp;m, tách từ thời luật chưa cho tách nhỏ; ít hàng, giao dịch tốt.",
        "dat_tren_1000": "Phần nhiều là nông nghiệp tách ra từ rẫy, chưa đủ điều kiện tách nhỏ.",
        "view": "Nhìn ra hồ, đồi hoặc toàn cảnh thị trấn; hiếm, giá theo tầm nhìn."}
# khoảng rao phổ biến nửa đầu 2026 (quan sát thực địa, data/prices.json) — map id cũ → nhóm
RANGE_MAP = {"nong-nghiep-dien-tich-lon": "dat_tren_1000", "tach-thua-tho-cu": "tach_thua_150_300", "view-doi-view-ho": "view"}
RANGE = {}
for seg in PR["periods"][0]["segments"]:
    k = RANGE_MAP.get(seg["id"])
    if k: RANGE[k] = (seg["price_min_vnd_m2"], seg["price_max_vnd_m2"], seg.get("total_price_note"))
# lý do của tháng — CHỈ ghi khi Chú xác nhận (ground truth thực địa); tháng không có dòng thì không in
REASON = {"2026-09": "Theo quan sát thực địa của Panorama, giá rao tháng 9/2026 mềm hơn vì mùa mưa bão và kinh tế: nguồn cung mùa này ra nhiều hơn cầu, người bán rao mềm hơn để ra hàng."}

def tr(v): return f"{v/1e6:.2f}".replace(".", ",")
def tr1(v): return (f"{v/1e6:.1f}".rstrip("0").rstrip(".")).replace(".", ",")
def month_vi(m): y, mo = m.split("-"); return f"{int(mo)}/{y}"
def next_month(m):
    y, mo = map(int, m.split("-")); return f"{mo % 12 + 1}/{y + (mo == 12)}"
def val(m, key):
    """(median_vnd, n, nguồn) cho tháng m, nhóm key: tin rao đủ 10 → 'rao'; không thì sổ thực địa nếu có → 'so'; không thì None"""
    g = m["ghi_nhan"]["groups"][key]
    if g["median_vnd_m2"] is not None: return g["median_vnd_m2"], g["n"], "rao"
    e = ED.get(m["month"], {}).get(key)
    if e and e.get("median_vnd_m2"): return e["median_vnd_m2"], e.get("n"), "so"
    return None
def trend(cur, prev):
    d = (cur - prev) / prev * 100
    w = "đi&nbsp;ngang" if abs(d) < 3 else ("nhích&nbsp;lên" if 3 <= d <= 8 else "nhích&nbsp;xuống" if -8 <= d <= -3 else ("tăng" if 8 < d <= 40 else "giảm" if -40 <= d < -8 else "khác&nbsp;hẳn"))
    return d, w
def plain(s): return re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ")

months = D["monthly"]; last = months[-1]; base = D["baseline"]
m_on = dt.date.fromisoformat(base["measured_on"]).strftime("%-d/%-m/%Y"); last_m = month_vi(last["month"]); nxt = next_month(last["month"])

# ---- số của kỳ này, theo nhóm ----
cur = {}   # key -> dict(v, n, src, prev_m, prev_v, d, w)
for key, label, low in GROUPS:
    c = val(last, key)
    if not c: continue
    prev = None
    for m in reversed(months[:-1]):
        v = val(m, key)
        if v: prev = (m["month"], v); break
    row = {"v": c[0], "n": c[1], "src": c[2], "prev": prev}
    if prev: row["d"], row["w"] = trend(c[0], prev[1][0])
    cur[key] = row
def src_txt(r): return f'{r["n"]} tin rao' if r["src"] == "rao" else "sổ thực địa Panorama†"
def cmp_txt(r):
    if not r.get("prev"): return '<span class="cmp-l">chưa có tháng trước</span><span class="cmp-v">để&nbsp;so</span>'
    pm, pv = r["prev"]
    lead = f'<span class="cmp-l">so với tháng {month_vi(pm)} ({tr(pv[0])})</span>'
    if r["w"] == "khác&nbsp;hẳn": return lead + '<span class="cmp-v"><b>không so được</b> <small>(mẫu khác&nbsp;nhau)</small></span>'
    sign = "+" if r["d"] > 0 else "−"
    small = " <small>(mẫu&nbsp;nhỏ)</small>" if (r["src"] == "rao" and r["n"] < 20) or (pv[2] == "rao" and (pv[1] or 0) < 20) else ""
    return lead + f'<span class="cmp-v"><b>{r["w"]}</b>&nbsp;{sign}{abs(r["d"]):.0f}&nbsp;%{small}</span>'
def sent(key, r):
    s = f'{LOW[key].capitalize()} <strong>{tr(r["v"])} triệu/m²</strong> ({src_txt(r)})'
    if not r.get("prev"): return s + "."
    pm, pv = r["prev"]
    if r["w"] == "khác&nbsp;hẳn": return s + f'; tháng {month_vi(pm)} là {tr(pv[0])} nhưng mẫu hai tháng khác hẳn nhau nên không&nbsp;so.'
    sign = "+" if r["d"] > 0 else "−"
    return s + f', so với tháng {month_vi(pm)} là {tr(pv[0])} — <strong>{r["w"]}</strong> ({sign}{abs(r["d"]):.0f}&nbsp;%).'

# ---- IDX-LEAD: dòng kỳ + một câu đáp (hai nhóm mẫu lớn nhất có thể so được) ----
lead = f'''<p class="idx-period">Kỳ tháng {last_m} · đo tới <span class="nw">{m_on}</span> · giá rao, chưa phải giá&nbsp;chốt</p>
'''

# ---- IDX-NOW: mục 01 ----
cells = []; below = []
for key, label, low in GROUPS:
    r = cur.get(key)
    if not r: continue
    rng = RANGE.get(key)
    rng_html = f'<div class="price-band">Khoảng rao nửa đầu 2026: <b>{tr1(rng[0])}–{tr1(rng[1])}&nbsp;tr/m²</b></div>' if rng else '<div class="price-band">Khoảng rao nửa đầu 2026: chờ số thực&nbsp;địa</div>'
    if rng and r["v"] < rng[0]: below.append(low)
    cells.append(f'<div class="price-cell"><div class="price-tier">{label}</div><div class="price-range">{tr(r["v"])} <span class="idx-unit">tr/m²</span></div><div class="price-unit">trung vị của {src_txt(r)}</div>{rng_html}<div class="price-total">{NOTE[key]}</div></div>')
why = ""
if below:
    lst = (", ".join(below[:-1]) + " và " + below[-1]) if len(below) > 1 else below[0]
    why = f'<p class="idx-why">Trung vị tháng {last_m} của {lst} đang thấp hơn khoảng rao nửa đầu năm. Vì sao, <a href="#tin-hieu">xem&nbsp;mục&nbsp;04</a>.</p>'
now = f'''<div class="idx-section-label">01 — Giá kỳ này</div>
<h2 class="idx-section-title">Giá đất Nam Ban tháng {last_m} theo từng loại</h2>
<div class="price-grid idx-now">{"".join(cells)}</div>
{why}'''

# ---- IDX-HIST: mục 02 ----
# câu đáp mục 02: chỉ nói CHIỀU, không nhắc lại số (số đã ở bốn ô mục 01 và bảng ngay dưới)
def dirw(k):
    r = cur[k]
    if not r.get("prev") or r["w"] == "khác&nbsp;hẳn": return None
    return plain(r["w"])
dirs = {k: dirw(k) for k, _, _ in GROUPS if k in cur}
down = [k for k, w in dirs.items() if w == "giảm"]   # chỉ tính lệch rõ (>8 %); "nhích" 3–8 % coi như chưa đổi chiều
up = [k for k, w in dirs.items() if w == "tăng"]
if down and not up: verdict = "Nhìn chung giá rao đang mềm&nbsp;đi."
elif up and not down: verdict = "Nhìn chung giá rao đang&nbsp;tăng."
elif not up and not down: verdict = "Nhìn chung giá rao gần như đứng&nbsp;yên."
else: verdict = "Mỗi loại đi một chiều, chưa có xu hướng&nbsp;chung."
items = []
for k, label, low in GROUPS:
    if k not in dirs: continue
    w = dirs[k]
    r = cur[k]
    if w:
        pm, pv = r["prev"]; sign = "+" if r["d"] > 0 else "−"
        small = " · mẫu nhỏ" if (r["src"] == "rao" and r["n"] < 20) or (pv[2] == "rao" and (pv[1] or 0) < 20) else ""
        items.append(f'<li><span>{label}</span><span class="d"><b>{w}&nbsp;{sign}{abs(r["d"]):.0f}&nbsp;%</b><small>so với {month_vi(pm)}{small}</small></span></li>')
    else:
        items.append(f'<li><span>{label}</span><span class="d"><em>chưa so được</em><small>mẫu hai tháng khác nhau</small></span></li>')
answer = f'{verdict} Tháng {last_m} so với tháng gần nhất có đủ số của từng&nbsp;loại:'
dirs_html = '<ul class="idx-dirs">' + "".join(items) + '</ul>'
rows = []; shown = set(); skipped = {}
chron = months  # cũ → mới
for key, label, low in GROUPS:
    pts = []
    for m in reversed(chron):
        v = val(m, key)
        if not v:
            n_raw = m["ghi_nhan"]["groups"][key]["n"]
            if n_raw: skipped.setdefault(key, []).append((m["month"], n_raw))
            continue
        shown.add(m["month"])
        tag = ' · đang đo' if m["status"] == "partial" else ""
        n_txt = f'{v[1]}&nbsp;tin' if v[2] == "rao" else "sổ thực địa†"
        pts.append(f'<li><span class="idx-m"><time datetime="{m["month"]}">{month_vi(m["month"])}</time></span><b>{tr(v[0])}</b><small>{n_txt}{tag}</small></li>')
    rows.append(f'<tr><th scope="row">{label}</th><td><ol class="idx-series">{"".join(pts)}</ol></td></tr>')
first_shown = min(shown)
span = [m["month"] for m in chron if first_shown <= m["month"] <= last["month"]]
empty_months = [month_vi(m) for m in span if m not in shown]
dagger = " † Số từ sổ giao dịch thực địa của Panorama, dùng cho tháng tin rao chưa đủ." if "†" in "".join(rows) + "".join(cells) else ""
gap = (f' Tháng {", ".join(empty_months)} không loại nào đủ {MIN_N} tin nên không có trong bảng.' if empty_months else "")
hist = f'''<div class="idx-section-label">02 — Diễn biến</div>
<h2 class="idx-section-title">Giá đất Nam Ban đang tăng hay giảm?</h2>
<p class="idx-answer">{answer}</p>
{dirs_html}
<figure class="idx-fig pm-selectable">
<figcaption>Trung vị giá rao, triệu đồng/m², đo&nbsp;{m_on}. Nguồn và cách tính ở mục&nbsp;03.</figcaption>
<div class="idx-tblwrap"><table class="idx-tbl idx-bygroup">
<thead><tr><th scope="col">Loại đất</th><th scope="col">Các tháng đủ số, mới nhất trước</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody></table></div>
</figure>
<p class="idx-note">Mỗi loại chỉ hiện tháng có từ {MIN_N} tin rao trở lên; tháng ít tin hơn thì bỏ, không điền số ước.{gap}{dagger} Từ tháng 10/2026 đo mỗi tuần nên sẽ ít tháng hụt&nbsp;hơn.</p>'''

# ---- IDX-DATA: mục 03 ----
n_src = 7  # danh sách nguồn quét (meta.method) — không đếm theo tháng có tin
data = f'''<dl class="idx-stats">
<div><dt>Đơn vị</dt><dd>Triệu đồng/m², trung vị</dd></div>
<div><dt>Loại giá</dt><dd>Giá rao, chưa phải giá chốt</dd></div>
<div><dt>Nguồn</dt><dd>{n_src} trang rao công khai, gộp trùng</dd></div>
<div><dt>Ngưỡng</dt><dd>Từ {MIN_N} tin mỗi nhóm mỗi tháng</dd></div>
<div><dt>Kỳ đo</dt><dd><time datetime="{base["measured_on"]}">{m_on}</time> · {base["n"]} tin đang treo</dd></div>
<div><dt>Kỳ tới</dt><dd>Đầu tháng {nxt}</dd></div>
</dl>
<p class="idx-body-p">Chúng tôi không đăng lại từng tin, không đăng tựa hay số điện thoại người rao, chỉ đăng số tổng&nbsp;hợp.</p>'''

# ---- IDX-CITE ----
cite_nums = "; ".join(f'{LOW[k]} {tr(cur[k]["v"])}' for k, _, _ in GROUPS if k in cur)
cite = f'''<div class="idx-cite pm-selectable">
<p id="citeText">Tháng {last_m}, giá rao đất ở xã Nam Ban Lâm Hà, <span class="nw">Lâm Đồng</span> — trung vị theo Namban Index, triệu đồng/m²: {cite_nums}. Giá rao, chưa phải giá chốt; đo tới {m_on}.</p>
<p class="src" id="citeSrc">Nguồn: Namban Panorama, Namban Index, kỳ tháng {last_m}. https://nambanpanorama.com/namban-index</p>
<div class="idx-cite-actions"><button class="idx-act" type="button" id="copyCite"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="1.5"/><path d="M15 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h3"/></svg><span>Chép trích dẫn</span></button><button class="idx-act" type="button" id="copyLink"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1.2 1.2"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1.2-1.2"/></svg><span>Chép link</span></button></div>
</div>'''

# ---- IDX-FAQ: 2 câu sinh theo số + 5 câu tĩnh ----
q1 = f"Theo Namban Index, tháng {last_m} trung vị giá rao ở xã Nam Ban Lâm Hà, triệu đồng/m²: {cite_nums}. "
if RANGE: q1 += "Khoảng rao phổ biến nửa đầu 2026 theo quan sát thực địa: " + "; ".join(f'{LOW[k]} {tr1(RANGE[k][0])}–{tr1(RANGE[k][1])}' for k, _, _ in GROUPS if k in RANGE) + ". "
q1 += "Đây là giá rao, chưa phải giá chốt; mỗi lô khác nhau tùy vị trí, pháp lý, thương lượng."
q2 = plain(verdict) + f" Tháng {last_m} so với tháng gần nhất có đủ số: " + "; ".join(
    f'{LOW[k]} {plain(cur[k]["w"]) if cur[k]["w"] != "khác&nbsp;hẳn" else "không so được vì mẫu hai tháng khác hẳn"}' if cur[k].get("prev") else f'{LOW[k]} chưa có tháng trước để so'
    for k, _, _ in GROUPS if k in cur) + ". "
q2 += (REASON.get(last["month"], "") + " " if REASON.get(last["month"]) else "") + "Đây là giá rao; chưa đủ để kết luận xu hướng dài hạn."
FAQ = [("Giá đất Nam Ban hiện nay bao nhiêu một mét?", q1),
       ("Giá đất Nam Ban đang tăng hay giảm?", q2),
       ("Giá đất Nam Ban có còn rẻ không?", "So với Đà Lạt và Bảo Lộc, mặt bằng giá Nam Ban vẫn dễ tiếp cận hơn. Nhưng đó là so theo giá rao; giá chốt của từng lô vẫn phải kiểm tại thực địa"),
       ("Đất Nam Ban 500 triệu mua được gì?", "Tầm 500 triệu tới 1,2 tỷ thường rơi vào khu tách thửa nhỏ có thổ cư, diện tích 150–300 m², hạ tầng điện nước đã có hoặc đang hoàn thiện — hợp xây nhỏ hoặc nhà vườn cuối tuần."),
       ("Phân khúc đất Nam Ban nào dễ bán lại nhất?", "Theo quan sát thị trường, lô có view hồ hoặc view toàn cảnh thường dễ bán lại hơn — người mua tìm view thật hiếm khi hối tiếc. Khoảng rao phổ biến nửa đầu 2026 của nhóm này là 4–6 triệu/m², tổng giá phổ biến 1,2–1,8 tỷ một lô; trung vị tin rao từng tháng xem ở mục 01."),
       ("Vì sao giá rao và giá bán thật ở Nam Ban chênh nhau?", "Giá rao là giá người bán muốn, không phải giá giao dịch được. Ở một số khu hai con số này chênh nhau đáng kể, nên con số \"rẻ\" cần kiểm chứng tại thực địa thay vì tin theo tin rao."),
       ("Mua đất nông nghiệp diện tích lớn ở Nam Ban tầm bao nhiêu?", "Đất nông nghiệp trên 1.000 m², chưa tách thửa, có khoảng rao phổ biến nửa đầu 2026 là 1,7–2,8 triệu/m² — tổng giá phổ biến 4,5–15 tỷ tùy diện tích; trung vị tin rao từng tháng xem ở mục 01. Hợp làm vườn canh tác hoặc giữ dài hạn; cần kiểm kỹ lộ giới và khả năng chuyển đổi.")]
H3 = 'style="font-family:\'Fraunces\',serif;font-weight:500;font-size:19px;line-height:1.35;margin:26px 0 8px;color:var(--ink);"'
PP = 'style="font-size:16px;line-height:1.72;color:var(--muted);margin:0;font-weight:300;"'
faq_html = "\n".join(f'<h3 {H3}>{q}</h3><p {PP}>{a}</p>' for q, a in FAQ)
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}, ensure_ascii=False, indent=2)

# ---- ghép vào trang ----
s = open(P, encoding="utf-8").read()
def replace_block(s, tag, body):
    st = re.search(rf"<!-- {tag}:START[^>]*-->", s).group(0); a = s.index(st) + len(st); end = f"<!-- {tag}:END -->"; b = s.index(end)
    return s[:a] + "\n" + body + "\n" + s[b:]
for tag, body in [("IDX-LEAD", lead), ("IDX-NOW", now), ("IDX-HIST", hist), ("IDX-DATA", data), ("IDX-CITE", cite), ("IDX-FAQ", faq_html)]:
    s = replace_block(s, tag, body)
s = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage",[\s\S]*?\}\s*</script>', lambda m: '<script type="application/ld+json">\n' + faq_ld + '\n</script>', s, count=1)

CSS = """.idx-header p.idx-period{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--line);margin:0 0 14px;max-width:none;line-height:1.6}
.idx-period .nw{white-space:nowrap}
.idx-kicker{font-size:13.5px;color:var(--muted);margin:-8px 0 14px}
.idx-answer{font-size:16.5px;line-height:1.7;margin:0 0 14px;text-wrap:pretty}
.idx-why{font-size:15px;line-height:1.7;margin:16px 0 0;text-wrap:pretty;color:var(--ink)}
.idx-why b{font-weight:500}
.idx-dirs{list-style:none;margin:0 0 22px;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:0 28px;border-top:1px solid var(--line)}
.idx-dirs li{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--line);font-size:15px}
.idx-dirs .d{display:flex;flex-direction:column;align-items:flex-end;text-align:right}
.idx-dirs b{font-weight:500;color:var(--ink);white-space:nowrap}
.idx-dirs small{font-size:11.5px;color:var(--muted);white-space:nowrap}
.idx-dirs em{font-style:italic;color:var(--muted);white-space:nowrap;font-size:14px}
@media(max-width:600px){.idx-dirs{grid-template-columns:1fr}}
.idx-now{grid-template-columns:repeat(4,1fr);grid-auto-rows:auto}
.idx-now .price-cell{padding:22px 18px 16px;display:grid;grid-row:span 5;grid-template-rows:subgrid;row-gap:0;align-content:start}
.idx-now .price-tier{margin-bottom:10px;align-self:end}
.idx-now .price-desc{display:flex;flex-direction:column;margin-top:2px}
.idx-now .cmp-l{font-size:12.5px;color:var(--muted)}
.idx-now .cmp-v{font-size:13.5px;color:var(--ink)}
@supports not (grid-template-rows:subgrid){.idx-now .price-cell{display:block}.idx-now .price-tier{min-height:2.9em}}
@media(max-width:900px){.idx-now{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.idx-now{grid-template-columns:1fr}}
.idx-now .price-range{font-size:28px}
.idx-unit{font-family:'Be Vietnam Pro',sans-serif;font-size:13px;color:var(--muted);letter-spacing:.2px}
.idx-now .price-desc{text-wrap:pretty}
.idx-now .price-desc b{font-weight:500;color:var(--ink)}
.idx-now .price-desc small{font-size:11.5px;color:var(--stone-text,#726a5c)}
.price-band{margin-top:10px;font-size:12.5px;color:var(--muted);line-height:1.45;text-wrap:pretty}
.price-band b{font-weight:500;color:var(--forest)}
.idx-fig{margin:18px 0 10px}
.idx-fig figcaption{font-size:13px;color:var(--muted);line-height:1.5;margin:0 0 8px;text-wrap:pretty}
.idx-fig table+figcaption,.idx-fig .idx-tblwrap+figcaption{margin:8px 0 0}
.idx-tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:3px;background:var(--card)}
.idx-tbl{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
.idx-tbl th,.idx-tbl td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;line-height:1.4}
.idx-tbl thead th{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:500;vertical-align:bottom}
.idx-tbl tbody th{font-weight:500;color:var(--ink);white-space:nowrap}
.idx-tbl tbody th a{color:var(--forest);text-decoration:none;border-bottom:1px solid var(--line)}
.idx-tbl .num{text-align:right}
.idx-tbl td b{font-family:'Fraunces',serif;font-weight:500;font-size:17px;color:var(--ink)}
.idx-tbl td small{display:block;font-size:11.5px;color:var(--muted)}
.idx-tbl td.dash{color:var(--stone);font-size:16px}
.idx-tbl tr:last-child th,.idx-tbl tr:last-child td{border-bottom:0}
.idx-tmp{font-size:10.5px;color:var(--muted);margin-left:4px;font-style:italic}
.idx-note{font-size:13.5px;color:var(--muted);line-height:1.6;margin:10px 0 0;text-wrap:pretty}
.idx-note a,.idx-dl a,.idx-answer a{color:var(--forest);text-decoration:none;border-bottom:1px solid var(--line)}
.idx-dl{font-size:13.5px;color:var(--muted);margin:10px 0 4px}
.idx-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border:1px solid var(--line);border-radius:3px;overflow:hidden;margin:0 0 18px}
.idx-stats div{background:var(--card);padding:12px 14px}
.idx-stats dt{font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase;color:var(--stone-text,#726a5c);font-weight:500;margin-bottom:4px}
.idx-stats dd{margin:0;font-size:14px;line-height:1.45;color:var(--ink)}
.idx-bygroup tbody th{width:34%;white-space:normal;font-family:'Fraunces',serif;font-weight:400;font-size:16px;line-height:1.35}
.idx-series{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(86px,1fr));gap:8px 10px}
.idx-series li{display:flex;flex-direction:column;min-width:0}
.idx-series .idx-m{font-size:11.5px;line-height:16px;height:16px;letter-spacing:.04em;color:var(--muted);white-space:nowrap}
.idx-series b{font-family:'Fraunces',serif;font-weight:500;font-size:19px;color:var(--ink);line-height:1.25}
.idx-series small{font-size:11.5px;color:var(--muted)}
.idx-series li:first-child b{color:var(--forest)}
@media(max-width:600px){.idx-stats{grid-template-columns:1fr 1fr}.idx-tbl{font-size:13px}.idx-answer{font-size:15.5px}.idx-now .price-range{font-size:27px}
.idx-bygroup thead{display:none}.idx-bygroup,.idx-bygroup tbody,.idx-bygroup tr,.idx-bygroup th,.idx-bygroup td{display:block;width:auto}
.idx-bygroup tr{padding:12px 14px;border-bottom:1px solid var(--line)}.idx-bygroup tr:last-child{border-bottom:0}
.idx-bygroup tbody th,.idx-bygroup td{padding:0;border:0}.idx-bygroup tbody th{margin-bottom:8px;width:auto}}
"""
if "/* IDX-GEN:START */" in s:
    s = re.sub(r"/\* IDX-GEN:START \*/\n[\s\S]*?/\* IDX-GEN:END \*/", lambda m: "/* IDX-GEN:START */\n" + CSS + "/* IDX-GEN:END */", s, count=1)
else:
    s = s.replace('<style id="idx-v2">\n', '<style id="idx-v2">\n/* IDX-GEN:START */\n' + CSS + '/* IDX-GEN:END */\n', 1)

# ---- JSON-LD + dateModified ----
s = re.sub(r'"temporalCoverage": "[^"]*"', f'"temporalCoverage": "{first_shown}/{last["month"]}"', s, count=1)
s = re.sub(r'("@type": "Dataset",[\s\S]*?"dateModified": )"[^"]*"', lambda m: m.group(1) + f'"{NOW.date().isoformat()}"', s, count=1)
s = re.sub(r'("@type": "Article",[\s\S]*?"dateModified": )"[^"]*"', lambda m: m.group(1) + f'"{NOW.strftime("%Y-%m-%dT%H:%M:00+07:00")}"', s, count=1)
open(P, "w", encoding="utf-8").write(s)

for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S): json.loads(m.group(1))
for m in re.finditer(r"<style[^>]*>(.*?)</style>", s, re.S): assert m.group(1).count("{") == m.group(1).count("}")
for t in ["div", "figure", "table", "thead", "tbody", "tr", "th", "td", "p", "h2", "h3", "dl", "dt", "dd"]:
    o = len(re.findall(rf"<{t}\b[^>]*>", s)); c = len(re.findall(rf"</{t}>", s)); assert o == c, (t, o, c)
print("OK:", len(rows), "tháng trong bảng ·", len(cells), "ô ·", len(FAQ), "FAQ · dateModified", NOW.strftime("%Y-%m-%d %H:%M"))
