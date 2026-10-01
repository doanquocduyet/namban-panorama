#!/usr/bin/env python3
"""Gộp lượt đo so sánh vùng (phiếu 2/10/2026) → tools/survey/so-sanh-da-lat-<ngày>.json. KHÔNG đụng data/index.

Cách tính chép đúng aggregate.py của Index (mốc nền = tin còn đang rao tại ngày đo, không chia tháng):
- loại tin thiếu giá hoặc diện tích; giữ 100 nghìn–100 triệu/m² và 50 triệu–200 tỷ cả lô; bỏ tin đăng trước 2026
- gộp trùng trong cùng một vùng: diện tích ±2% và giá ±3%
- 5 nhóm cùng quy tắc; dưới 10 tin: ghi "mẫu nhỏ", không tính trung vị
Nam Ban: dòng của crawl.py (bỏ nhóm video tổng hợp, theo phiếu), lọc khu như aggregate.py.
Vùng khác: dòng của so-sanh-vung.py. Không ghi URL, tựa, SĐT vào file kết quả.
"""
import csv, glob, json, statistics as st, datetime as dt, os, sys
from collections import Counter, defaultdict

TODAY = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=7)).date()  # ngày đo theo giờ VN
MIN_N = 10
DIGEST = "video môi giới + sàn (tổng hợp)"
NB_KHU = {"Nam Ban", "Đông Thanh", "Mê Linh", "Gia Lâm"}
VUNG = ["Nam Ban", "Tà Nung", "Đà Lạt nội thành (ghi rõ phường 1–12)", "Đà Lạt ven khác (Xuân Thọ, Xuân Trường, Trạm Hành)",
        "Đà Lạt (chỉ ghi Đà Lạt, không nêu phường/xã)"]

def slugkhu(r):  # chép aggregate.py
    u = r["url"].lower().split("/", 3)[-1]
    for k, n in (("dong-thanh", "Đông Thanh"), ("me-linh", "Mê Linh"), ("buon-chuoi", "Mê Linh"), ("xa-gia-lam", "Gia Lâm")):
        if k in u: return n
    if r["khu"] == "mơ hồ (không nêu khu)" and r["nguon"] == "guland.vn": return "chưa rõ khu"
    return r["khu"]

def clean(r):
    if not (r.get("dien_tich_m2") and r.get("gia_ca_lo_vnd")): return False
    a = float(r["dien_tich_m2"]); t = float(r["gia_ca_lo_vnd"]); m2 = t / a
    if not (1e5 <= m2 <= 1e8 and 5e7 <= t <= 2e11): return False
    if r["ngay_dang"] and r["ngay_dang"] < "2026-01-01": return False
    r["_a"], r["_t"], r["_m2"] = a, t, m2
    return True

raw_nb = [r for f in glob.glob("survey/out/tin-rao-*.csv") for r in csv.DictReader(open(f, encoding="utf-8")) if r["nguon"] != DIGEST]
raw_v = [r for f in glob.glob("survey/out-vung/tin-rao-*.csv") for r in csv.DictReader(open(f, encoding="utf-8"))]
note_raw = {"Nam Ban (dòng thô crawl.py, đã bỏ nhóm video tổng hợp)": len(raw_nb), "vùng khác (dòng thô)": len(raw_v)}

rows = []
for r in raw_nb:
    if not clean(r): continue
    r["_khu"] = slugkhu(r)
    if r["_khu"] not in NB_KHU | {"chưa rõ khu"}: continue
    r["_vung"] = "Nam Ban"; rows.append(r)
khu_v = Counter(r["khu"] for r in raw_v)
for r in raw_v:
    if not clean(r) or r["khu"] not in VUNG: continue
    r["_khu"] = r["_vung"] = r["khu"]; rows.append(r)

# gộp trùng trong cùng khu (Nam Ban: như Index, theo từng khu con; vùng khác: theo vùng)
rows.sort(key=lambda r: (r["ngay_dang"] or "9999", r["nguon"]))
kept = []
def dup(k, r): return abs(k["_a"] - r["_a"]) <= .02 * k["_a"] and abs(k["_t"] - r["_t"]) <= .03 * k["_t"]
for r in rows:
    if any(k["_khu"] == r["_khu"] and dup(k, r) for k in kept): continue
    kept.append(r)

def q(xs, p):
    xs = sorted(xs); k = (len(xs) - 1) * p; lo = int(k); hi = min(lo + 1, len(xs) - 1); return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)
G = [("tach_thua_150_300", "Đất nền tách thửa 150–300 m²", lambda r: 150 <= r["_a"] <= 300 and r["loai"] != "nhà / biệt thự"),
     ("lo_500_tho_cu", "Lô khoảng 500 m² có thổ cư", lambda r: 350 <= r["_a"] <= 700 and r["loai"] != "nhà / biệt thự"),
     ("dat_tren_1000", "Đất trên 1.000 m²", lambda r: r["_a"] > 1000 and r["loai"] != "nhà / biệt thự"),
     ("view", "Lô có view hồ, đồi, toàn cảnh", lambda r: r["view"] == "view"),
     ("nha", "Nhà / biệt thự (m² đất)", lambda r: r["loai"] == "nhà / biệt thự")]

out = {"ngay_do": TODAY.isoformat(), "phieu": "So sánh giá rao Nam Ban – Tà Nung – Đà Lạt, 2/10/2026",
       "cach_do": "Giống mốc nền Namban Index: tin còn đang rao tại ngày đo, 7 trang tin rao công khai (kiểm robots.txt), "
                  "loại tin thiếu giá/diện tích, gộp trùng diện tích ±2% và giá ±3% trong cùng vùng, bỏ tin đăng trước 2026. "
                  "Giá rao, chưa phải giá chốt. Dưới 10 tin: mẫu nhỏ, không tính trung vị. Đơn vị đồng/m² đất.",
       "vung": {}, "ghi_chu": {"dong_tho": note_raw, "phan_vung_dong_tho_vung_khac": dict(khu_v.most_common())}}
for v in VUNG:
    rs = [r for r in kept if r["_vung"] == v]
    g = {}
    for key, label, f in G:
        xs = [r["_m2"] for r in rs if f(r)]
        ok = len(xs) >= MIN_N
        g[key] = {"label": label, "n": len(xs), "median_vnd_m2": int(st.median(xs)) if ok else None,
                  "p10_vnd_m2": int(q(xs, .1)) if ok else None, "p90_vnd_m2": int(q(xs, .9)) if ok else None,
                  "ghi": None if ok else "mẫu nhỏ"}
    out["vung"][v] = {"n": len(rs), "nguon": dict(Counter(r["nguon"] for r in rs)), "loai_theo_crawl": dict(Counter(r["loai"] for r in rs)), "groups": g}

dst = f"tools/survey/so-sanh-da-lat-{TODAY.isoformat()}.json"
json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Đã ghi", dst)
def f(x): return "" if x is None else f"{x/1e6:.2f}".replace(".", ",")
for v, d in out["vung"].items():
    print(f"\n## {v} — {d['n']} tin · nguồn {d['nguon']}")
    for key, g in d["groups"].items():
        print(f"  {g['label']}: n={g['n']}" + (f" · trung vị {f(g['median_vnd_m2'])} · P10–P90 {f(g['p10_vnd_m2'])}–{f(g['p90_vnd_m2'])} tr/m²" if g["median_vnd_m2"] else " · mẫu nhỏ"))
print("\nPhân vùng dòng thô (vùng khác):", json.dumps(out["ghi_chu"]["phan_vung_dong_tho_vung_khac"], ensure_ascii=False))
