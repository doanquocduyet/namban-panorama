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

# ---- IDX-LEAD: dòng kỳ + dòng ký tên (ai đo, ở đâu, dẫn xuống cách đo) ----
lead = f'''<p class="idx-period">Kỳ tháng {last_m} · đo tới <span class="nw">{m_on}</span> · giá rao, chưa phải giá&nbsp;chốt</p>
<p class="idx-by">Đo và tổng hợp bởi Namban&nbsp;Panorama, <span class="nw">tại Nam Ban · <a href="#du-lieu">cách đo</a></span></p>'''

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
<p class="idx-kicker">Trung vị: xếp các tin rao từ thấp tới cao, lấy giá ở&nbsp;giữa.</p>
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
rows = []; chron = months  # cũ → mới
# cột = tháng có ít nhất một loại đủ số, mới nhất trước; tên tháng ghi MỘT lần ở đầu cột
cols = [m for m in reversed(chron) if any(val(m, k) or m["ghi_nhan"]["groups"][k].get("median_small_vnd_m2") for k, _, _ in GROUPS)]
first_shown = min(m["month"] for m in cols)
for key, label, low in GROUPS:
    tds = []
    for i, m in enumerate(cols):
        v = val(m, key); mv = month_vi(m["month"]) + (" · đang đo" if m["status"] == "partial" else "")
        cls = ' class="cur"' if i == 0 else ""
        if v:
            n_txt = f'{v[1]}&nbsp;tin' if v[2] == "rao" else "sổ thực địa†"
            tds.append(f'<td{cls} data-m="{mv}"><b>{tr(v[0])}</b><small>{n_txt}</small></td>')
        else:
            g = m["ghi_nhan"]["groups"][key]; n_raw = g["n"]
            if g.get("median_small_vnd_m2"):   # 5–9 tin: in số, gắn "mẫu nhỏ" (Chú chốt 26/9/2026 — ô trống nhìn thiếu số liệu)
                tds.append(f'<td class="{"cur " if i == 0 else ""}sm" data-m="{mv}"><b>{tr(g["median_small_vnd_m2"])}</b><small>{n_raw}&nbsp;tin · mẫu&nbsp;nhỏ</small></td>')
            else:
                tds.append(f'<td{cls} data-m="{mv}"><span class="few">{n_raw}&nbsp;tin, chưa đủ để&nbsp;tính</span></td>' if n_raw else f'<td{cls} data-m="{mv}"><span class="few">chưa có&nbsp;tin</span></td>')
    rows.append(f'<tr><th scope="row">{label}</th>{"".join(tds)}</tr>')
CUR = ' class="cur"'
TMP = '<small>đang đo</small>'
thead = "".join(f'<th scope="col"{CUR if i == 0 else ""}><time datetime="{m["month"]}">{month_vi(m["month"])}</time>{TMP if m["status"] == "partial" else ""}</th>' for i, m in enumerate(cols))
span = [m["month"] for m in chron if first_shown <= m["month"] <= last["month"]]
shown_m = {m["month"] for m in cols}
empty_months = [month_vi(m) for m in span if m not in shown_m]
dagger = " † Số từ sổ giao dịch thực địa của Panorama, dùng cho tháng tin rao chưa đủ." if "†" in "".join(rows) + "".join(cells) else ""
gap = (f' Tháng {", ".join(empty_months)} không loại nào có từ 5 tin nên không có&nbsp;cột.' if empty_months else "")
hist = f'''<div class="idx-section-label">02 — Diễn biến</div>
<h2 class="idx-section-title">Giá đất Nam Ban đang tăng hay giảm?</h2>
<p class="idx-answer">{answer}</p>
{dirs_html}
<figure class="idx-fig pm-selectable">
<figcaption>Trung vị giá rao, triệu đồng/m², đo&nbsp;{m_on}. Nguồn và cách tính ở mục&nbsp;03.</figcaption>
<div class="idx-tblwrap"><table class="idx-tbl idx-months" style="--nc:{len(cols)}">
<thead><tr><th scope="col">Loại đất</th>{thead}</tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody></table></div>
</figure>
<p class="idx-note">Ô có từ {MIN_N} tin là trung vị đủ tin cậy, dùng để kết luận tăng hay giảm. Ô ghi "mẫu nhỏ" là trung vị của 5–9 tin: vẫn là số thật, đọc để tham khảo, không dùng để so tăng giảm. Dưới 5 tin thì không tính, vì trung vị lúc đó chỉ là giá của một hai&nbsp;lô.{gap}{dagger}</p>'''

# ---- IDX-DATA: mục 03 ----
n_src = 7  # danh sách nguồn quét (meta.method) — không đếm theo tháng có tin
DIGESTS = {"video môi giới + sàn (tổng hợp)", "nambanvillas.vn/tin-rao"}  # nhãn mới + nhãn cũ (run #5)
dg_n = D["meta"].get("digest_n") or 0
dg_m = [m["month"] for m in months if DIGESTS & set(k for k, v in m["ghi_nhan"]["sources"].items() if v)]
dg_src = " + tin rao qua video" if dg_n else ""
dg_p = (f' Bảng diễn biến tháng {month_vi(dg_m[0]).split("/")[0]}–{month_vi(dg_m[-1])} có thêm {dg_n} tin rao qua video môi giới và sàn, mỗi tin có ngày đăng và đã được đối chiếu với nguồn&nbsp;gốc; chúng tôi bỏ tin ngoài xã Nam&nbsp;Ban, gộp trùng với tin tự đo, và không tính chúng vào số tin còn đang&nbsp;rao.' if dg_n and dg_m else "")
data = f'''<dl class="idx-stats">
<div><dt>Đơn vị</dt><dd>Triệu đồng/m², trung vị</dd></div>
<div><dt>Loại giá</dt><dd>Giá rao, chưa phải giá chốt</dd></div>
<div><dt>Nguồn</dt><dd>{n_src} trang rao công khai{dg_src}, gộp trùng</dd></div>
<div><dt>Ngưỡng</dt><dd>Từ {MIN_N} tin mỗi nhóm mỗi tháng</dd></div>
<div><dt>Kỳ đo</dt><dd><time datetime="{base["measured_on"]}">{m_on}</time> · {base["n"]} tin còn đang rao</dd></div>
<div><dt>Kỳ tới</dt><dd>Đầu tháng {nxt}</dd></div>
</dl>
<p class="idx-body-p">Chúng tôi không đăng lại từng tin, không đăng tựa hay số điện thoại người rao, chỉ đăng số tổng&nbsp;hợp.{dg_p}</p>'''

# ---- tổng hợp toàn bộ tin còn đang rao ngày đo (Chú giao 25/9/2026: "làm tổng hợp cho index") ----
# Cố ý chỉ in SỐ TIN + KHOẢNG GIÁ PHỔ BIẾN (p10–p90), không in trung vị: trung vị là việc của mục 01 (theo tháng
# đăng), in thêm một trung vị khác cho cùng loại đất là hai con số tranh nhau. Theo khu chỉ đếm tin, không in
# giá (CLAUDE.md: không có bảng giá theo khu). Bốn nhóm đúng bộ phân loại chung; nhà nêu trong câu ghi chú.
bg = base["groups"]
SLAB = {"tach_thua_150_300": 'Đất nền tách&nbsp;thửa<small>150–300&nbsp;m²</small>',
        "lo_500_tho_cu": 'Lô khoảng 500&nbsp;m²<small>có thổ&nbsp;cư</small>',
        "dat_tren_1000": 'Đất trên 1.000&nbsp;m²<small>phần nhiều là nông&nbsp;nghiệp</small>',
        "view": 'Lô có view<small>hồ, đồi, toàn&nbsp;cảnh</small>'}
stock_rows = "".join(
    f'<tr><th scope="row">{SLAB[k]}</th><td class="num">{bg[k]["n"]}</td><td class="num">'
    + (f'{tr1(bg[k]["p10_vnd_m2"])}–{tr1(bg[k]["p90_vnd_m2"])}' if bg[k].get("p10_vnd_m2") else '<span class="few">dưới 10&nbsp;tin</span>')
    + '</td></tr>' for k, label, _ in GROUPS if k in bg)
KHU = [("Nam Ban", "chỉ ghi “Nam Ban”"), ("Đông Thanh", "Đông Thanh"), ("Mê Linh", "Mê Linh"), ("Gia Lâm", "Gia Lâm"), ("chưa rõ khu", "không ghi khu")]
khu_txt = " · ".join(f'{lab} {base["by_khu"][k]["n"]}' for k, lab in KHU if base.get("by_khu", {}).get(k, {}).get("n"))
n_house = bg.get("nha", {}).get("n", 0)
n_out = base["n"] - n_house - sum(bg[k]["n"] for k in ("tach_thua_150_300", "lo_500_tho_cu", "dat_tren_1000") if k in bg)
data += f'''
<h3 class="idx-sub">Tổng hợp {base["n"]} tin còn đang rao ngày&nbsp;{m_on}</h3>
<figure class="idx-fig pm-selectable">
<div class="idx-tblwrap"><table class="idx-tbl idx-stock">
<thead><tr><th scope="col">Loại đất</th><th scope="col" class="num">Số&nbsp;tin</th><th scope="col" class="num">Giá phổ&nbsp;biến<br><span class="u">triệu/m²</span></th></tr></thead>
<tbody>
{stock_rows}
</tbody></table></div>
<figcaption>Khoảng giá phổ biến: bỏ 10&nbsp;% tin rẻ nhất và 10&nbsp;% tin đắt nhất, lấy khoảng còn lại. Tính trên mọi tin còn đang rao ngày đo, không theo tháng đăng, nên không so thẳng với bốn ô ở mục&nbsp;01.</figcaption>
</figure>
<p class="idx-note">Theo khu: {khu_txt}. {n_house} tin là nhà hoặc biệt thự; {n_out} tin đất có diện tích nằm ngoài ba nhóm diện tích trên (ví dụ dưới 150&nbsp;m², 300–350&nbsp;m², 700–1.000&nbsp;m²) — vẫn được đếm, không vào ô&nbsp;nào.</p>'''

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

CSS = """.idx-tbl.idx-stock tbody th{white-space:normal}
.idx-stock tbody th small{display:block;font-weight:400;font-size:12px;color:var(--muted);margin-top:2px}
.idx-stock td.num{text-align:right;white-space:nowrap}
.idx-stock thead th.num{text-align:right;white-space:nowrap}
.idx-stock thead .u{text-transform:none;letter-spacing:0;font-size:11.5px}
@media(max-width:600px){.idx-stock th,.idx-stock td{padding:9px 8px}.idx-stock tbody th{font-size:13px}}
.idx-stock .few{font-style:italic;font-size:12px;color:var(--muted)}
.idx-header p.idx-period{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--line);margin:0 0 14px;max-width:none;line-height:1.6}
.idx-period .nw{white-space:nowrap}
.idx-header p.idx-by{font-size:13px;color:#c8c0b0;margin:-6px 0 0;max-width:none}
.idx-by .nw{white-space:nowrap}
.idx-header p.idx-by a{color:#e8e1d3;text-decoration:none;border-bottom:1px solid rgba(232,225,211,.35)}
.idx-header p.idx-by a:hover{border-color:#e8e1d3}
.idx-kicker{font-size:13.5px;color:var(--muted);margin:-8px 0 14px}
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
.idx-months{table-layout:fixed}
.idx-months thead th{text-align:right;white-space:nowrap}
.idx-months thead th:first-child{text-align:left;width:40%}
.idx-months thead th time{display:block;font-size:12.5px;letter-spacing:.04em;color:var(--ink);text-transform:none}
.idx-months thead th small{display:block;font-size:10.5px;letter-spacing:.04em;text-transform:none;font-style:italic;color:var(--muted);font-weight:400}
.idx-months tbody th{white-space:normal;font-family:'Fraunces',serif;font-weight:400;font-size:16px;line-height:1.35;vertical-align:middle}
.idx-months td{text-align:right;vertical-align:middle}
.idx-months td b{display:block;font-family:'Fraunces',serif;font-weight:500;font-size:19px;color:var(--ink);line-height:1.2}
.idx-months td small{display:block;font-size:11.5px;color:var(--muted)}
.idx-months td.cur{background:rgba(47,64,52,.045)}
.idx-months td.cur b{color:var(--forest)}
.idx-months thead th.cur{background:rgba(47,64,52,.045)}
.idx-months td.sm b{color:var(--muted);font-weight:400}
.idx-months .few{font-size:11.5px;font-style:italic;color:var(--stone-text,#726a5c)}
@media(max-width:600px){.idx-stats{grid-template-columns:1fr 1fr}.idx-tbl{font-size:13px}.idx-answer{font-size:15.5px}.idx-now .price-range{font-size:27px}
.idx-months,.idx-months thead,.idx-months tbody{display:block}
.idx-months thead tr{display:grid;grid-template-columns:repeat(var(--nc,3),1fr)}.idx-months thead th:first-child{display:none}
.idx-months thead th{padding:10px 12px}
.idx-months tbody tr{display:grid;grid-template-columns:repeat(var(--nc,3),1fr)}
.idx-months tbody th{grid-column:1/-1;padding:12px 12px 4px;border:0}
.idx-months td{padding:6px 12px 12px;border-bottom:1px solid var(--line)}.idx-months tr:last-child td{border-bottom:0}
.idx-months td b{font-size:18px}}
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
