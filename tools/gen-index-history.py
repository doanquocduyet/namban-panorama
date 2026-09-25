#!/usr/bin/env python3
"""Sinh mục 02 (Diễn biến — lịch sử giá theo tháng) và mục 06 (Tin rao đang được quan sát) của
namban-index.html từ data/index/monthly.json. Chạy lại mỗi khi monthly.json đổi:
    python3 tools/gen-index-history.py
Chỉ thay phần giữa hai cặp marker IDX-HIST / IDX-OBS; cập nhật Dataset JSON-LD + dateModified.
Không đăng danh sách tin, không URL tin, không tựa, không SĐT — chỉ số tổng hợp."""
import json, re, html, datetime as dt

P = "namban-index.html"
D = json.load(open("data/index/monthly.json", encoding="utf-8"))
MIN_N = D["meta"].get("min_n", 10)
NOW = dt.datetime.now(dt.timezone(dt.timedelta(hours=7)))

def tr(v):
    """VND/m² -> 'x,yz' triệu"""
    return f"{v/1e6:.2f}".replace(".", ",") if v else "—"
def month_vi(m):
    y, mo = m.split("-"); return f"{int(mo)}/{y}"
def cell(g, unit=True):
    if g["median_vnd_m2"] is None:
        return f'<td class="num low">ít dữ liệu <small>({g["n"]} tin)</small></td>'
    rng = f'<small>{tr(g["p10_vnd_m2"])} – {tr(g["p90_vnd_m2"])}</small>' if g.get("p10_vnd_m2") else ""
    return f'<td class="num"><b>{tr(g["median_vnd_m2"])}</b> <small>({g["n"]} tin)</small>{rng}</td>'

base = D["baseline"]; months = D["monthly"]; last = months[-1]
bg = base["groups"]; lg = last["posted"]["groups"]
first_m = month_vi(months[0]["month"]); last_m = month_vi(last["month"])
m_on = dt.date.fromisoformat(base["measured_on"]).strftime("%-d/%-m/%Y")

# ---- câu trả lời trực tiếp (AI trích được) ----
enough = [m for m in months if m["posted"]["groups"]["dat_duoi_2000"]["median_vnd_m2"] is not None]
thin = [m for m in months if m["posted"]["groups"]["dat_duoi_2000"]["median_vnd_m2"] is None]
ans = []
if len(enough) < 2:
    ans.append(f"Tính tới {m_on}, <strong>chưa đủ dữ liệu để nói giá đất Nam&nbsp;Ban tăng hay giảm</strong> theo tháng: "
               f"{'các tháng ' + ', '.join(month_vi(m['month']).split('/')[0] for m in thin) + '/2026' if thin else ''} chỉ còn "
               f"{min(m['posted']['n'] for m in thin)}–{max(m['posted']['n'] for m in thin)} tin có ngày đăng, dưới ngưỡng {MIN_N} tin một nhóm.")
for m in enough:
    g = m["posted"]["groups"]["dat_duoi_2000"]
    ans.append(f"Tháng {month_vi(m['month'])} có {m['posted']['n']} tin đăng mới, trung vị giá rao đất dưới 2.000&nbsp;m² là <strong>{tr(g['median_vnd_m2'])} triệu/m²</strong> ({g['n']} tin).")
ans.append(f"Mốc nền {m_on}: <strong>{base['n']} tin đang treo</strong> sau khử trùng, trung vị đất dưới 2.000&nbsp;m² <strong>{tr(bg['dat_duoi_2000']['median_vnd_m2'])} triệu/m²</strong>, "
           f"đất từ 2.000&nbsp;m² <strong>{tr(bg['nong_nghiep_tu_2000']['median_vnd_m2'])}</strong>, tin có view <strong>{tr(bg['view']['median_vnd_m2'])}</strong>. "
           f"Đây là giá rao, chưa phải giá đã&nbsp;chốt.")
answer = " ".join(ans)

# ---- bảng tháng ----
rows = []
for m in reversed(months):
    p = m["posted"]; r = m["refreshed_guland"]
    tag = ' <sup class="idx-tmp" title="tháng đang diễn ra, số tới ngày đo">tạm</sup>' if m["status"] == "partial" else ""
    rcell = cell(r["groups"]["dat_duoi_2000"]) if r["n"] else '<td class="num">—</td>'
    pcell = cell(p["groups"]["dat_duoi_2000"]) if p["n"] else '<td class="num">—</td>'
    rows.append(f'<tr><th scope="row"><time datetime="{m["month"]}">{month_vi(m["month"])}</time>{tag}<small>{p["n"]} đăng · {r["n"]} làm&nbsp;mới</small></th>{pcell}{rcell}</tr>')
rows.append(f'<tr class="base"><th scope="row">Mốc nền {m_on}<small>{base["n"]} tin đang treo</small></th>{cell(bg["dat_duoi_2000"])}<td class="num">—</td></tr>')
table = f'''<figure class="idx-fig pm-selectable">
<figcaption>Trung vị giá rao đất dưới 2.000&nbsp;m² ở xã Nam&nbsp;Ban Lâm&nbsp;Hà theo tháng, triệu đồng/m². Nhóm dưới {MIN_N} tin ghi "ít dữ liệu", không nội suy. Nguồn: Namban&nbsp;Index, đo&nbsp;{m_on}.</figcaption>
<div class="idx-tblwrap"><table class="idx-tbl">
<thead><tr><th scope="col">Tháng</th><th scope="col" class="num">Theo tin đăng<br><small>trung vị · số tin · khoảng 10–90 %</small></th><th scope="col" class="num">Theo tin Guland làm mới<br><small>trung vị · số tin · khoảng 10–90 %</small></th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody></table></div>
</figure>'''

# ---- mốc nền theo nhóm + khu (mục 06) ----
grp_rows = "".join(f'<tr><th scope="row">{g["label"]}</th>{cell(g)}</tr>' for k, g in bg.items())
khu_rows = "".join(f'<tr><th scope="row">{k}</th><td class="num{"" if v["median_vnd_m2"] else " low"}">{("<b>" + tr(v["median_vnd_m2"]) + "</b> ") if v["median_vnd_m2"] else "ít dữ liệu "}<small>({v["n"]} tin)</small></td></tr>' for k, v in base["by_khu"].items() if v["n"])
src_n = len(base["sources"]); villas_pct = round(100 * base["villas_n"] / base["n"])
obs = f'''<p class="idx-answer">Ngày {m_on}, Namban Index đếm được <strong>{base['n']} tin rao đang treo</strong> ở xã Nam&nbsp;Ban Lâm&nbsp;Hà sau khi lọc đúng xã, loại tin thiếu giá hoặc diện tích và gộp tin trùng giữa {src_n} nguồn công khai. Hàng của Nam&nbsp;Ban Villas chiếm khoảng {villas_pct}&nbsp;%; trung vị toàn xã có hay không có nguồn này gần như không&nbsp;đổi.</p>
<figure class="idx-fig pm-selectable">
<figcaption>Mốc nền {m_on}: số tin và trung vị giá rao (triệu đồng/m²) theo nhóm và theo khu. Nhóm dưới {MIN_N} tin ghi "ít&nbsp;dữ&nbsp;liệu".</figcaption>
<div class="idx-tblwrap"><table class="idx-tbl">
<thead><tr><th scope="col">Nhóm</th><th scope="col" class="num">Trung vị<br><small>số tin · khoảng 10–90 %</small></th></tr></thead>
<tbody>{grp_rows}</tbody>
<thead><tr><th scope="col">Khu</th><th scope="col" class="num">Trung vị<br><small>số tin</small></th></tr></thead>
<tbody>{khu_rows}</tbody>
</table></div>
</figure>
<p class="idx-note">Chúng tôi không đăng lại từng tin — chỉ đăng số tổng hợp. Tin rao là giá người bán muốn; muốn biết một lô cụ thể đáng giá bao nhiêu, xem <a href="/dinh-gia-dat-nam-ban">vì sao hai lô cùng diện tích khác giá</a>.</p>'''

hist = f'''<div class="idx-section-label">02 — Diễn biến</div>
<h2 class="idx-section-title">Giá đất Nam Ban tăng hay giảm từ tháng {first_m} đến nay?</h2>
<p class="idx-answer">{answer}</p>
{table}
<p class="idx-note">Hai cách xếp tháng, không trộn: <strong>theo tin đăng</strong> là ngày đăng ghi trên trang nguồn (Batdongsanonline, Thuviennhadat, Muaban, Villas); <strong>theo tin làm mới</strong> là ngày Guland làm mới tin — tin cũ được đẩy lên cũng tính, nên cột này phản ánh <em>hàng đang chào</em> chứ không phải hàng mới ra. Tin đăng những tháng đầu năm phần lớn đã bán hoặc đã gỡ, sàn không giữ lại — vì thế từ tháng {last_m} Index tự ghi mỗi tuần, không trông vào bản lưu của ai.</p>
<p class="idx-dl">Dữ liệu mở: <a href="/data/index/monthly.json">monthly.json</a> · <a href="/data/index/monthly.csv">monthly.csv</a> — trích dẫn tự do, ghi nguồn Namban&nbsp;Panorama.</p>'''

s = open(P, encoding="utf-8").read()
def replace_block(s, start, end, body):
    a = s.index(start) + len(start); b = s.index(end)
    return s[:a] + "\n" + body + "\n" + s[b:]
if "<!-- IDX-HIST:START -->" not in s:
    s = s.replace("  <!-- 02 DIỄN BIẾN -->\n", "  <!-- 02 DIỄN BIẾN -->\n<!-- IDX-HIST:START (sinh bởi tools/gen-index-history.py — đừng sửa tay) -->\n<!-- IDX-HIST:END -->\n", 1)
    # bỏ khối cũ (label + h2 + p chờ) nằm sau marker END tới <hr>
    a = s.index("<!-- IDX-HIST:END -->") + len("<!-- IDX-HIST:END -->"); b = s.index("<hr>", a)
    s = s[:a] + "\n\n  " + s[b:]
if "<!-- IDX-OBS:START -->" not in s:
    s = s.replace("  <!-- 06 TIN RAO -->\n", "  <!-- 06 TIN RAO -->\n<!-- IDX-OBS:START (sinh bởi tools/gen-index-history.py — đừng sửa tay) -->\n<!-- IDX-OBS:END -->\n", 1)
    a = s.index("<!-- IDX-OBS:END -->") + len("<!-- IDX-OBS:END -->"); b = s.index("<hr>", a)
    # giữ label + h2 mục 06, bỏ đoạn chờ
    seg = s[a:b]
    keep = re.search(r'\s*<div class="idx-section-label">06[^<]*</div>\s*<h2[^>]*>[^<]*</h2>', seg).group(0)
    s = s[:a] + keep + "\n\n  " + s[b:]
s = replace_block(s, re.search(r"<!-- IDX-HIST:START[^>]*-->", s).group(0), "<!-- IDX-HIST:END -->", hist)
s = replace_block(s, re.search(r"<!-- IDX-OBS:START[^>]*-->", s).group(0), "<!-- IDX-OBS:END -->", obs)

# ---- CSS (một lần) ----
CSS = """.idx-answer{font-size:16.5px;line-height:1.7;margin:0 0 14px;text-wrap:pretty}
.idx-fig{margin:14px 0 10px}
.idx-fig figcaption{font-size:13px;color:var(--muted);line-height:1.5;margin:0 0 8px;text-wrap:pretty}
.idx-tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:3px;background:var(--card)}
.idx-tbl{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
.idx-tbl th,.idx-tbl td{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;line-height:1.4}
.idx-tbl thead th{font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:500;vertical-align:bottom}
.idx-tbl thead th small{display:block;font-size:10.5px;letter-spacing:0;text-transform:none;font-weight:400;margin-top:2px}
.idx-tbl tbody th{font-weight:500;color:var(--ink);white-space:nowrap}
.idx-tbl tbody th small{display:block;font-size:11.5px;color:var(--muted);font-weight:400;white-space:normal}
.idx-tbl .num{text-align:right;white-space:nowrap}
.idx-tbl td b{font-family:'Fraunces',serif;font-weight:500;font-size:16px;color:var(--ink)}
.idx-tbl td small{display:block;font-size:11.5px;color:var(--muted)}
.idx-tbl td.low{color:var(--muted);font-style:italic;font-size:13px}
.idx-tbl tr.base th,.idx-tbl tr.base td{border-top:2px solid var(--stone);background:rgba(47,64,52,.04)}
.idx-tbl tr:last-child th,.idx-tbl tr:last-child td{border-bottom:0}
.idx-tmp{font-size:10.5px;color:var(--muted);margin-left:4px;font-style:italic}
.idx-note{font-size:14.5px;color:var(--muted);line-height:1.65;margin:10px 0 0;text-wrap:pretty}
.idx-note a,.idx-dl a{color:var(--forest);text-decoration:none;border-bottom:1px solid var(--line)}
.idx-dl{font-size:13.5px;color:var(--muted);margin:10px 0 4px}
@media(max-width:600px){.idx-tbl{font-size:13px}.idx-tbl tbody th{white-space:normal}.idx-tbl td.low{white-space:normal}.idx-tbl tbody th{min-width:96px}.idx-tbl th,.idx-tbl td{padding:8px 7px}.idx-tbl td small{font-size:11px}.idx-tbl thead th{font-size:10.5px;letter-spacing:.05em}.idx-tbl td b{font-size:15px}.idx-answer{font-size:15.5px}}
"""
if ".idx-tblwrap{" not in s:
    s = s.replace("</style>\n", CSS + "</style>\n", 1) if '<style id="idx-v2">' not in s else s.replace('<style id="idx-v2">\n', '<style id="idx-v2">\n' + CSS, 1)

# ---- JSON-LD Dataset + dateModified ----
s = re.sub(r'"temporalCoverage": "[^"]*"', f'"temporalCoverage": "{months[0]["month"]}/{last["month"]}"', s, count=1)
s = re.sub(r'("@type": "Dataset",[\s\S]*?"dateModified": )"[^"]*"', lambda m: m.group(1) + f'"{NOW.date().isoformat()}"', s, count=1)
if "data/index/monthly.json" not in s:
    s = s.replace('''  "distribution": [
    {
      "@type": "DataDownload",
      "encodingFormat": "application/json",
      "contentUrl": "https://nambanpanorama.com/data/prices.json"
    },''', '''  "distribution": [
    {
      "@type": "DataDownload",
      "encodingFormat": "application/json",
      "contentUrl": "https://nambanpanorama.com/data/index/monthly.json",
      "description": "Trung vị giá rao đất xã Nam Ban Lâm Hà theo tháng và mốc nền, kèm số tin và khoảng 10–90 %"
    },
    {
      "@type": "DataDownload",
      "encodingFormat": "text/csv",
      "contentUrl": "https://nambanpanorama.com/data/index/monthly.csv"
    },
    {
      "@type": "DataDownload",
      "encodingFormat": "application/json",
      "contentUrl": "https://nambanpanorama.com/data/prices.json"
    },''', 1)
    s = s.replace('"name": "Namban Index — Giá đất Nam Ban theo phân khúc",', '"name": "Namban Index — Giá đất Nam Ban theo phân khúc và theo tháng",', 1)
s = re.sub(r'("@type": "Article",[\s\S]*?"dateModified": )"[^"]*"', lambda m: m.group(1) + f'"{NOW.strftime("%Y-%m-%dT%H:%M:00+07:00")}"', s, count=1)
open(P, "w", encoding="utf-8").write(s)

# ---- kiểm ----
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S): json.loads(m.group(1))
for m in re.finditer(r"<style[^>]*>(.*?)</style>", s, re.S): assert m.group(1).count("{") == m.group(1).count("}")
for t in ["div", "figure", "table", "thead", "tbody", "tr", "th", "td", "p", "h2"]:
    o = len(re.findall(rf"<{t}\b[^>]*>", s)); c = len(re.findall(rf"</{t}>", s)); assert o == c, (t, o, c)
print("OK: mục 02 + 06 sinh lại ·", len(months), "tháng · mốc nền", base["n"], "tin · dateModified", NOW.strftime("%Y-%m-%d %H:%M"))
