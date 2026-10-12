#!/usr/bin/env python3
"""Gộp kết quả lấy tin (survey/out/tin-rao-*.csv) thành data/index/monthly.json:
- cập nhật tháng hiện tại (posted / refreshed_guland), thêm dòng tuần, đặt mốc nền = lần đo mới nhất
- tin mới = URL chưa từng thấy (lưu băm sha1 trong data/index/seen.json, không lưu URL)
- ĐIỀU KIỆN DỪNG: bất thường thì ghi data/index/alert.json và thoát mã 3 — workflow KHÔNG sinh lại trang.
Chỉ số tổng hợp; không tựa, không URL, không SĐT."""
import csv, glob, json, os, re, sys, hashlib, statistics as st, datetime as dt
from collections import defaultdict, Counter

# AGG_TODAY: chạy lại một lượt đo cũ (vd tính lại tuần 41 sau khi sửa bộ lọc 12/10/2026).
TODAY = dt.date.fromisoformat(os.environ["AGG_TODAY"]) if os.environ.get("AGG_TODAY") else dt.date.today()
ISO_WEEK = TODAY.strftime("%G-W%V")
# AGG_REBUILD_MONTHS="2026-09,2026-10": các tháng này được ghi đè dù mẫu mới nhỏ hơn (tháng đã lưu bị lẫn tin).
# AGG_REBUILD_ONLY=1: chỉ tính lại các tháng đó từ dòng thô gộp nhiều lượt; KHÔNG đụng tuần, mốc nền, seen.
REBUILD = {m.strip() for m in os.environ.get("AGG_REBUILD_MONTHS", "").split(",") if m.strip()}
REBUILD_ONLY = os.environ.get("AGG_REBUILD_ONLY") == "1"
NO_STOP = os.environ.get("AGG_NO_STOP") == "1" or REBUILD_ONLY
IN = {"Nam Ban", "Đông Thanh", "Mê Linh", "Gia Lâm"}
MIN_N = 10
MIN_SMALL = 5   # 5–9 tin: vẫn lưu trung vị riêng (median_small_vnd_m2), trang in kèm nhãn "mẫu nhỏ" — Chú chốt 26/9/2026
P = "data/index/monthly.json"; SEEN_P = "data/index/seen.json"
D = json.load(open(P, encoding="utf-8"))
seen = set(json.load(open(SEEN_P)).get("hashes", [])) if glob.glob(SEEN_P) else set()

# Lọc tin NGOÀI VÙNG (sự cố 12/10/2026): trang danh sách "xã Đông Thanh" của guland/thuviennhadat cài kèm tin nổi bật
# nơi khác (nhà phố TP.HCM, Hà Nội, Đà Nẵng…). Tin đó không ghi địa chỉ trong JSON-LD nên bộ quét gán khu theo trang
# danh sách → tháng 9–10 nhóm "Đông Thanh" có 87/104 và 72/75 tin là tin nơi khác, đẩy đất nền lên 9,15 tr/m².
# Hai lớp (đã review đối kháng 12/10/2026, xem CLAUDE.md mục Index):
#  (1) mọi nguồn: đường dẫn có địa danh nơi khác (khớp trọn cụm) mà KHÔNG có dấu riêng của Nam Ban → bỏ;
#  (2) guland/thuviennhadat mang nhãn "Đông Thanh" (đúng nhóm bị lẫn) → đường dẫn phải có dấu địa phương.
# Cố ý KHÔNG đưa vào danh sách nơi khác: tên trùng thôn Nam Ban (long-bien, dong-ha, ba-dinh, tu-liem, thanh-tri, gia-lam,
# me-linh…), chữ thường dễ nhầm (hai-phong = "hai phòng", da-nang = "đã nâng", cu-chi = "thổ cư chỉ", long-an = "Thăng Long
# an ninh", nha-trang = "nhà trắng", can-ho, hue, sai-gon, bao-loc, tan-phu) và Đà Lạt (tin Nam Ban hay ghi "cách TP Đà Lạt
# 9 km", "23 km tới hồ Xuân Hương" — soát bằng diagnose.py tokens 12/10/2026).
def _tok(*names):  # khớp trọn cụm giữa dấu "-" hoặc "/" (tránh "gia-lam-ha-noi" bị đọc thành "lam-ha")
    return re.compile(r"(?:^|[-/])(?:%s)(?=$|[-/])" % "|".join(names))
STRONG_LOCAL = _tok(r"lam-ha(?!-noi)", "nam-ban", "namban", r"dt-?725", r"tl-?725", "tinh-lo-725", "duong-725",
                    "thac-voi", "linh-an", "bai-cong", "tong-doi")
LOCAL = re.compile(STRONG_LOCAL.pattern + "|" + _tok("dong-thanh", "me-linh", "gia-lam(?!-ha-noi)", "buon-chuoi").pattern)
FOREIGN = _tok("ho-chi-minh", "tphcm", "tp-hcm", "ha-noi", "hanoi", "tp-da-nang", "thanh-pho-da-nang", "quan-[a-z-]*-da-nang",
               "tp-hai-phong", "thanh-pho-hai-phong", "can-tho", "tien-giang", "my-tho", "binh-duong", "dong-nai", "tinh-long-an",
               "vung-tau", "ba-ria", "khanh-hoa", "tp-nha-trang", "thanh-pho-nha-trang", "thu-duc", "go-vap", "binh-thanh", "tan-binh", "phu-nhuan",
               "binh-tan", "cam-le", "hoc-mon", "huyen-cu-chi", "thanh-xuan", "cau-giay", "hoang-mai", "ha-dong", "kim-giang",
               "tan-dinh", "ben-thanh", "khanh-hoi", r"quan-\d+", r"phuong-\d+", "chung-cu", "can-ho-chung-cu", "thanh-hoa",
               "quang-tri", "nghe-an", "ha-tinh", "thai-binh", "nam-dinh", "ninh-binh", "bac-ninh", "quang-ninh", "thua-thien-hue",
               "quang-nam", "quang-ngai", "binh-dinh", "phu-yen", "gia-lai", "dak-lak", "kon-tum", "dak-nong", "binh-thuan",
               "ninh-thuan", "tay-ninh", "binh-phuoc", "ben-tre", "vinh-long", "tinh-an-giang", "kien-giang", "phu-quoc", "ca-mau",
               "bac-lieu", "soc-trang", "tra-vinh", "dong-thap", "hau-giang")
NEED_LOCAL = {"guland.vn", "thuviennhadat.vn"}
def foreign(r):
    """Trả lý do bỏ ('token' / 'need_local') hoặc None."""
    u = r["url"].lower().split("?")[0].split("/", 3)[-1]
    if FOREIGN.search(u) and not STRONG_LOCAL.search(u): return "token"
    if r["nguon"] in NEED_LOCAL and r.get("khu") == "Đông Thanh" and not LOCAL.search(u): return "need_local"
    return None

def slugkhu(r):
    # bộ quét kết luận "ngoài xã" thì đường dẫn không được ghi đè; "nhiều địa danh" thì chỉ đường dẫn có dấu riêng
    # của Nam Ban (và không có địa danh nơi khác) mới được gỡ
    u = r["url"].lower().split("/", 3)[-1]
    if r["khu"].startswith("ngoài xã"): return r["khu"]
    if r["khu"].startswith("mơ hồ (nhiều") and not (STRONG_LOCAL.search(u) and not FOREIGN.search(u)): return r["khu"]
    for k, n in (("dong-thanh", "Đông Thanh"), ("me-linh", "Mê Linh"), ("buon-chuoi", "Mê Linh"), ("xa-gia-lam", "Gia Lâm")):
        if k in u: return n
    if r["khu"] == "mơ hồ (không nêu khu)" and r["nguon"] == "guland.vn": return "chưa rõ khu"
    return r["khu"]
rows = []
for f in sorted(glob.glob("survey/out/tin-rao-*.csv")): rows += list(csv.DictReader(open(f, encoding="utf-8")))
raw_by_src = Counter(r["nguon"] for r in rows)
good = []; n_foreign = {"token": Counter(), "need_local": Counter()}; _urls = set()
for r in rows:
    why = foreign(r)
    if why:
        n_foreign[why][r["nguon"]] += 1; continue
    if not (r.get("dien_tich_m2") and r.get("gia_ca_lo_vnd")): continue
    a = float(r["dien_tich_m2"]); t = float(r["gia_ca_lo_vnd"]); m2 = t / a
    if not (1e5 <= m2 <= 1e8 and 5e7 <= t <= 2e11): continue
    r["_m2"] = m2; r["_a"] = a; r["_t"] = t; r["_khu"] = slugkhu(r)
    if r["_khu"] not in IN | {"chưa rõ khu"}: continue
    if r["ngay_dang"] and r["ngay_dang"] < "2026-01-01": continue
    r["_h"] = hashlib.sha1(r["url"].split("?")[0].encode()).hexdigest()[:16]
    if r["_h"] in _urls: continue      # gộp nhiều lượt: giữ dòng HỢP LỆ đầu tiên của mỗi tin
    _urls.add(r["_h"]); good.append(r)
# Tin rao Villas tổng hợp (video môi giới + sàn, có ngày đăng, không link gốc) — CHỈ bổ sung bảng tháng:
# không vào mốc nền/tuần (không biết tin còn treo), không tính "tin mới"; gộp trùng với tin tự đo KHÔNG xét khu
# (sàn ghi khu khác nhau cho cùng một lô), tin tự đo được giữ trước vì có URL gốc.
DIGEST = "video môi giới + sàn (tổng hợp)"  # nhãn công khai trong monthly.json — KHÔNG ghi tên trang tổng hợp (Chú chốt 25/9)
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
        out["groups"][key] = {"label": label, "n": len(xs), "median_vnd_m2": int(st.median(xs)) if ok else None, "p10_vnd_m2": int(q(xs, .1)) if ok else None, "p90_vnd_m2": int(q(xs, .9)) if ok else None, "median_small_vnd_m2": int(st.median(xs)) if MIN_SMALL <= len(xs) < MIN_N else None}
    out["by_khu"] = {k: {"n": len([r for r in rs if r["_khu"] == k]), "median_vnd_m2": (int(st.median([r["_m2"] for r in rs if r["_khu"] == k])) if len([r for r in rs if r["_khu"] == k]) >= MIN_N else None)} for k in ["Nam Ban", "Đông Thanh", "Mê Linh", "Gia Lâm", "chưa rõ khu"]}
    out["villas_n"] = len([r for r in rs if r["nguon"] == "nambanvillas.vn"]); out["sources"] = dict(Counter(r["nguon"] for r in rs))
    return out

def write_csv(D):
    with open("data/index/monthly.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["thang", "co_so", "so_tin", "nhom", "n_nhom", "trung_vi_vnd_m2", "p10_vnd_m2", "p90_vnd_m2"])
        for d in D["monthly"]:
            for basis in ("ghi_nhan", "posted", "refreshed_guland"):
                for key, g in d[basis]["groups"].items(): w.writerow([d["month"], basis, d[basis]["n"], key, g["n"], g["median_vnd_m2"] or "", g["p10_vnd_m2"] or "", g["p90_vnd_m2"] or ""])
        for wq in D["weekly"]:
            for key, g in wq["snapshot"]["groups"].items(): w.writerow([wq["week"], "weekly_snapshot", wq["snapshot"]["n"], key, g["n"], g["median_vnd_m2"] or "", g["p10_vnd_m2"] or "", g["p90_vnd_m2"] or ""])

# ---- chạy lại lượt cũ: không được đè lên lượt mới hơn ----
if os.environ.get("AGG_TODAY") and not REBUILD_ONLY:
    newer = [w["week"] for w in D.get("weekly", []) if w["week"] > ISO_WEEK]
    if newer or D["meta"].get("measured_on", "") > TODAY.isoformat():
        print("DỪNG — đã có lượt đo mới hơn", newer or D["meta"].get("measured_on")); sys.exit(2)
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
print("Tin ngoài vùng bị loại — địa danh nơi khác:", dict(n_foreign["token"]), "· nhãn Đông Thanh thiếu dấu địa phương:", dict(n_foreign["need_local"]))
if prev_weeks:
    for s_, n in prev_weeks[-1]["snapshot"]["sources"].items():
        if n >= 20 and raw_by_src.get(s_, 0) > 0 and base["sources"].get(s_, 0) == 0:
            alerts.append(f"nguồn {s_} còn dòng thô nhưng về 0 tin SAU lọc (tuần trước {n}) — nghi đổi khuôn đường dẫn")
if REBUILD_ONLY: alerts = []        # tính lại tháng từ dòng thô gộp: không phải một lượt đo, luật dừng tuần không áp
HARD = [a for a in alerts if "về 0" in a or "<100" in a]
if alerts and NO_STOP and not HARD:
    print("CẢNH BÁO (không dừng — AGG_NO_STOP/AGG_REBUILD_ONLY):", alerts); alerts = []
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
# Tin cũ bị sàn gỡ sau 2–3 tháng (kinh nghiệm Villas 25/9/2026) → tháng đã qua CHỈ được ghi đè khi mẫu mới
# không nhỏ hơn mẫu đã lưu; nếu không, tháng 6 sẽ tụt dần về "dưới 10 tin" khi tin của nó biến mất khỏi mạng.
for m in sorted(set(allm) | {cur}):
    new = {"month": m, "status": "partial" if m == cur else "closed", "ghi_nhan": grp(allm.get(m, [])), "posted": grp(real.get(m, [])), "refreshed_guland": grp(upd.get(m, []))}
    old = months.get(m)
    if REBUILD_ONLY and m not in REBUILD: continue
    if m != cur and old and new["ghi_nhan"]["n"] < old["ghi_nhan"]["n"] and m not in REBUILD:
        old["status"] = "closed"; continue
    months[m] = new
D["monthly"] = [months[k] for k in sorted(months)]
if REBUILD_ONLY:
    D["meta"]["rebuilt"] = {"months": sorted(REBUILD), "at": dt.datetime.now(dt.timezone(dt.timedelta(hours=7))).isoformat(timespec="minutes"),
                            "note": "tính lại sau khi lọc tin ngoài vùng (sự cố 12/10/2026)"}
    json.dump(D, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    write_csv(D)
    print("REBUILD xong:", {m: months[m]["ghi_nhan"]["n"] for m in sorted(REBUILD) if m in months}); sys.exit(0)
wk = {"week": ISO_WEEK, "measured_on": TODAY.isoformat(), "new_listings": len(new_rows), "snapshot": base}
D["weekly"] = [w for w in prev_weeks if w["week"] != ISO_WEEK] + [wk]
D["baseline"] = {"measured_on": TODAY.isoformat(), "label": f"Mốc nền: toàn bộ tin đang treo ngày {TODAY.strftime('%-d/%-m/%Y')}, sau khử trùng", **base}
D["meta"]["generated_at"] = dt.datetime.now(dt.timezone(dt.timedelta(hours=7))).isoformat(timespec="minutes"); D["meta"]["measured_on"] = TODAY.isoformat()
D["meta"]["digest_n"] = n_digest
json.dump(D, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"hashes": sorted(seen | {r["_h"] for r in kept}), "updated": TODAY.isoformat()}, open(SEEN_P, "w"))
write_csv(D)
if glob.glob("data/index/alert.json"):
    import os; os.remove("data/index/alert.json")
print(f"OK tuần {ISO_WEEK}: {base['n']} tin đang treo · {len(new_rows)} tin mới · {n_digest} tin Villas tổng hợp (chỉ bảng tháng) · tháng {cur} posted n={months[cur]['posted']['n']}")
