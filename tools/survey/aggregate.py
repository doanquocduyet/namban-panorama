#!/usr/bin/env python3
"""Gộp kết quả lấy tin (survey/out/tin-rao-*.csv) thành data/index/monthly.json:
- cập nhật tháng hiện tại (posted / refreshed_guland), thêm dòng tuần, đặt mốc nền = lần đo mới nhất
- tin mới = URL chưa từng thấy (lưu băm sha1 trong data/index/seen.json, không lưu URL)
- ĐIỀU KIỆN DỪNG: bất thường thì ghi data/index/alert.json và thoát mã 3 — workflow KHÔNG sinh lại trang.
Chỉ số tổng hợp; không tựa, không URL, không SĐT."""
import csv, glob, json, sys, hashlib, statistics as st, datetime as dt
from collections import defaultdict, Counter

TODAY = dt.date.today(); ISO_WEEK = TODAY.strftime("%G-W%V")
IN = {"Nam Ban", "Đông Thanh", "Mê Linh", "Gia Lâm"}
MIN_N = 10
P = "data/index/monthly.json"; SEEN_P = "data/index/seen.json"
D = json.load(open(P, encoding="utf-8"))
seen = set(json.load(open(SEEN_P)).get("hashes", [])) if glob.glob(SEEN_P) else set()

def slugkhu(r):
    u = r["url"].lower().split("/", 3)[-1]
    for k, n in (("dong-thanh", "Đông Thanh"), ("me-linh", "Mê Linh"), ("buon-chuoi", "Mê Linh"), ("xa-gia-lam", "Gia Lâm")):
        if k in u: return n
    if r["khu"] == "mơ hồ (không nêu khu)" and r["nguon"] == "guland.vn": return "chưa rõ khu"
    return r["khu"]
rows = []
for f in glob.glob("survey/out/tin-rao-*.csv"): rows += list(csv.DictReader(open(f, encoding="utf-8")))
raw_by_src = Counter(r["nguon"] for r in rows)
good = []
for r in rows:
    if not (r.get("dien_tich_m2") and r.get("gia_ca_lo_vnd")): continue
    a = float(r["dien_tich_m2"]); t = float(r["gia_ca_lo_vnd"]); m2 = t / a
    if not (1e5 <= m2 <= 1e8 and 5e7 <= t <= 2e11): continue
    r["_m2"] = m2; r["_a"] = a; r["_t"] = t; r["_khu"] = slugkhu(r)
    if r["_khu"] not in IN | {"chưa rõ khu"}: continue
    if r["ngay_dang"] and r["ngay_dang"] < "2026-01-01": continue
    r["_h"] = hashlib.sha1(r["url"].split("?")[0].encode()).hexdigest()[:16]
    good.append(r)
# Tin rao Villas tổng hợp (video môi giới + sàn, có ngày đăng, không link gốc) — CHỈ bổ sung bảng tháng:
# không vào mốc nền/tuần (không biết tin còn treo), không tính "tin mới"; gộp trùng với tin tự đo KHÔNG xét khu
# (sàn ghi khu khác nhau cho cùng một lô), tin tự đo được giữ trước vì có URL gốc.
DIGEST = "nambanvillas.vn/tin-rao"
good.sort(key=lambda r: (r["nguon"] == DIGEST, r["ngay_dang"] or "9999", r["nguon"]))
kept = []
def dup(k, r): return abs(k["_a"] - r["_a"]) <= .02 * k["_a"] and abs(k["_t"] - r["_t"]) <= .03 * k["_t"]
for r in good:
    if r["nguon"] == DIGEST:
        if any(dup(k, r) for k in kept): continue
    elif any(k["_khu"] == r["_khu"] and dup(k, r) for k in kept): continue
    kept.append(r)
live = [r for r in kept if r["nguon"] != DIGEST]; n_digest = len(kept) - len(live)
def q(xs, p):
    xs = sorted(xs); k = (len(xs) - 1) * p; lo = int(k); hi = min(lo + 1, len(xs) - 1); return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)
G = [("tach_thua_150_300", "Đất nền tách thửa 150–300 m²", lambda r: 150 <= r["_a"] <= 300 and r["loai"] != "nhà / biệt thự"),
     ("lo_500_tho_cu", "Lô khoảng 500 m² có thổ cư", lambda r: 350 <= r["_a"] <= 700 and r["loai"] != "nhà / biệt thự"),
     ("dat_tren_1000", "Đất trên 1.000 m²", lambda r: r["_a"] > 1000 and r["loai"] != "nhà / biệt thự"),
     ("view", "Lô có view hồ, đồi, toàn cảnh", lambda r: r["view"] == "view"),
     ("nha", "Nhà / biệt thự (m² đất)", lambda r: r["loai"] == "nhà / biệt thự")]
def grp(rs):
    out = {"n": len(rs), "groups": {}}
    for key, label, f in G:
        xs = [r["_m2"] for r in rs if f(r)]
        ok = len(xs) >= MIN_N
        out["groups"][key] = {"label": label, "n": len(xs), "median_vnd_m2": int(st.median(xs)) if ok else None, "p10_vnd_m2": int(q(xs, .1)) if ok else None, "p90_vnd_m2": int(q(xs, .9)) if ok else None}
    out["by_khu"] = {k: {"n": len([r for r in rs if r["_khu"] == k]), "median_vnd_m2": (int(st.median([r["_m2"] for r in rs if r["_khu"] == k])) if len([r for r in rs if r["_khu"] == k]) >= MIN_N else None)} for k in ["Nam Ban", "Đông Thanh", "Mê Linh", "Gia Lâm", "chưa rõ khu"]}
    out["villas_n"] = len([r for r in rs if r["nguon"] == "nambanvillas.vn"]); out["sources"] = dict(Counter(r["nguon"] for r in rs))
    return out

# ---- điều kiện dừng ----
new_rows = [r for r in live if r["_h"] not in seen]
alerts = []
prev_weeks = D.get("weekly", [])
# chỉ xét khi lần đo trước cách ≥6 ngày — chạy lại trong cùng tuần (vd thêm nguồn) thì tin mới đương nhiên ít
gap_days = (TODAY - dt.date.fromisoformat(D["meta"].get("measured_on", "2000-01-01"))).days
if seen and gap_days >= 6 and len(new_rows) < 15: alerts.append(f"chỉ {len(new_rows)} tin mới trong tuần (<15)")
if D["meta"].get("digest_n") and raw_by_src.get(DIGEST, 0) == 0: alerts.append(f"nguồn {DIGEST} về 0 tin (lần trước {D['meta']['digest_n']}) — bảng tháng sẽ tụt nếu sinh lại")
base = grp(live)
if prev_weeks:
    # so từng nhóm có ở cả hai tuần (dùng .get: tên nhóm từng đổi 25/9/2026, khóa cũ 'dat_duoi_2000' làm run #4 chết)
    pg = prev_weeks[-1]["snapshot"].get("groups", {})
    for key, cg in base["groups"].items():
        og = pg.get(key) or {}
        pm, cm = og.get("median_vnd_m2"), cg.get("median_vnd_m2")
        if pm and cm and og.get("n", 0) >= 30 and cg.get("n", 0) >= 30 and abs(cm - pm) / pm > .25:
            alerts.append(f"trung vị {cg['label']} lệch {100*(cm-pm)/pm:.0f}% so tuần trước")
    for s_, n in prev_weeks[-1]["snapshot"]["sources"].items():
        if n > 0 and raw_by_src.get(s_, 0) == 0: alerts.append(f"nguồn {s_} về 0 tin (tuần trước {n}) — nghi bị chặn")
if base["n"] and base["villas_n"] / base["n"] > .4: alerts.append(f"Villas chiếm {100*base['villas_n']/base['n']:.0f}% (>40%)")
if base["n"] < 100: alerts.append(f"tổng chỉ {base['n']} tin sau khử trùng (<100)")
if alerts:
    json.dump({"tuan": ISO_WEEK, "ngay": TODAY.isoformat(), "canh_bao": alerts, "tong_tin": base["n"], "tin_moi": len(new_rows)}, open("data/index/alert.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("DỪNG — không sinh lại trang:", alerts); sys.exit(3)

# ---- cập nhật monthly.json ----
real = defaultdict(list); upd = defaultdict(list); allm = defaultdict(list)
for r in kept:
    if not r["ngay_dang"]: continue
    m = r["ngay_dang"][:7]
    if m < "2026-04": continue
    (upd if r["ngay_uoc"] else real)[m].append(r); allm[m].append(r)
cur = TODAY.strftime("%Y-%m")
months = {m["month"]: m for m in D["monthly"]}
for m in sorted(set(allm) | {cur}):
    months[m] = {"month": m, "status": "partial" if m == cur else "closed", "ghi_nhan": grp(allm.get(m, [])), "posted": grp(real.get(m, [])), "refreshed_guland": grp(upd.get(m, []))}
D["monthly"] = [months[k] for k in sorted(months)]
wk = {"week": ISO_WEEK, "measured_on": TODAY.isoformat(), "new_listings": len(new_rows), "snapshot": base}
D["weekly"] = [w for w in prev_weeks if w["week"] != ISO_WEEK] + [wk]
D["baseline"] = {"measured_on": TODAY.isoformat(), "label": f"Mốc nền: toàn bộ tin đang treo ngày {TODAY.strftime('%-d/%-m/%Y')}, sau khử trùng", **base}
D["meta"]["generated_at"] = dt.datetime.now(dt.timezone(dt.timedelta(hours=7))).isoformat(timespec="minutes"); D["meta"]["measured_on"] = TODAY.isoformat()
D["meta"]["digest_n"] = n_digest
json.dump(D, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"hashes": sorted(seen | {r["_h"] for r in kept}), "updated": TODAY.isoformat()}, open(SEEN_P, "w"))
with open("data/index/monthly.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["thang", "co_so", "so_tin", "nhom", "n_nhom", "trung_vi_vnd_m2", "p10_vnd_m2", "p90_vnd_m2"])
    for d in D["monthly"]:
        for basis in ("ghi_nhan", "posted", "refreshed_guland"):
            for key, g in d[basis]["groups"].items(): w.writerow([d["month"], basis, d[basis]["n"], key, g["n"], g["median_vnd_m2"] or "", g["p10_vnd_m2"] or "", g["p90_vnd_m2"] or ""])
    for wq in D["weekly"]:
        for key, g in wq["snapshot"]["groups"].items(): w.writerow([wq["week"], "weekly_snapshot", wq["snapshot"]["n"], key, g["n"], g["median_vnd_m2"] or "", g["p10_vnd_m2"] or "", g["p90_vnd_m2"] or ""])
if glob.glob("data/index/alert.json"):
    import os; os.remove("data/index/alert.json")
print(f"OK tuần {ISO_WEEK}: {base['n']} tin đang treo · {len(new_rows)} tin mới · {n_digest} tin Villas tổng hợp (chỉ bảng tháng) · tháng {cur} posted n={months[cur]['posted']['n']}")
