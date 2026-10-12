#!/usr/bin/env python3
"""Chẩn đoán nhóm tin Index bị lẫn (ca 12/10/2026: tháng 10 đất nền 9,15 tr/m², nhóm "Đông Thanh" trung vị 18,7 tr/m²).

Chạy trên GitHub Actions (workflow index-diagnose.yml) — runner tải được dòng thô 30 ngày (artifact tin-rao-*)
và vào được guland.vn. Chỉ IN kết quả dạng ::notice:: (đọc qua API check-runs), KHÔNG ghi gì vào repo.
Không in SĐT; tựa tin chỉ in rút gọn để nhận ra địa danh.
"""
import csv, glob, os, re, sys, statistics as st, importlib.util
from collections import Counter, defaultdict

def notice(title, msg):
    msg = str(msg).replace("%", "%25").replace("\r", " ").replace("\n", " · ")
    print("::notice title=%s::%s" % (title, msg[:3500]))

def slugkhu(r):  # y hệt aggregate.py
    u = r["url"].lower().split("/", 3)[-1]
    for k, n in (("dong-thanh", "Đông Thanh"), ("me-linh", "Mê Linh"), ("buon-chuoi", "Mê Linh"), ("xa-gia-lam", "Gia Lâm")):
        if k in u: return n
    if r["khu"] == "mơ hồ (không nêu khu)" and r["nguon"] == "guland.vn": return "chưa rõ khu"
    return r["khu"]

def part_raw():
    rows, seen = [], set()
    files = sorted(glob.glob("survey/diag/**/tin-rao-*.csv", recursive=True))
    for f in files:
        for r in csv.DictReader(open(f, encoding="utf-8")):
            u = r["url"].split("?")[0]
            if u in seen: continue
            seen.add(u); rows.append(r)
    notice("Dòng thô", "%d file · %d tin khác nhau · nguồn %s" % (len(files), len(rows), dict(Counter(r["nguon"] for r in rows))))
    good = []
    for r in rows:
        try:
            a = float(r["dien_tich_m2"]); t = float(r["gia_ca_lo_vnd"])
        except Exception:
            continue
        r["_m2"] = t / a; r["_k"] = slugkhu(r); good.append(r)
    lamha = re.compile(r"lam-ha|lam-dong|nam-ban")
    for month in ("2026-08", "2026-09", "2026-10"):
        dt = [r for r in good if r["_k"] == "Đông Thanh" and (r["ngay_dang"] or "")[:7] == month]
        if not dt: continue
        ok = [r for r in dt if lamha.search(r["url"].lower())]
        bad = [r for r in dt if not lamha.search(r["url"].lower())]
        med = lambda xs: "%.2f tr" % (st.median([x["_m2"] for x in xs]) / 1e6) if xs else "-"
        notice("Đông Thanh %s" % month,
               "%d tin (trung vị %s/m²) · đường dẫn có lam-ha/lam-dong/nam-ban: %d (trung vị %s) · không có: %d (trung vị %s) · nhãn bộ quét: %s · nguồn: %s"
               % (len(dt), med(dt), len(ok), med(ok), len(bad), med(bad),
                  dict(Counter(r["khu"] for r in dt).most_common(6)), dict(Counter(r["nguon"] for r in dt))))
        ex = sorted(dt, key=lambda r: -r["_m2"])[:10]
        notice("Đông Thanh %s — 10 tin giá cao nhất" % month,
               " | ".join("%s · %.1f tr/m² · %s m² · nhãn %s" % (r["url"].split("/", 3)[-1][:110], r["_m2"] / 1e6, r["dien_tich_m2"], r["khu"]) for r in ex))
    # toàn bộ tin vào bảng: bao nhiêu đường dẫn guland không mang dấu Lâm Hà
    g = [r for r in good if r["nguon"] == "guland.vn"]
    notice("guland toàn bộ", "%d tin · không có lam-ha/lam-dong/nam-ban trong đường dẫn: %d · khu theo slug: %s"
           % (len(g), len([r for r in g if not lamha.search(r["url"].lower())]), dict(Counter(r["_k"] for r in g).most_common(8))))

def part_live():
    spec = importlib.util.spec_from_file_location("crawl", "tools/survey/crawl.py")
    c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
    base = "https://guland.vn/mua-ban-bat-dong-san-xa-dong-thanh-huyen-lam-ha-lam-dong"
    r = c.get("guland.vn", base)
    if r is None:
        notice("guland trực tiếp", "không mở được trang danh sách Đông Thanh"); return
    soup = c.soup_of(r)
    links = c.links_matching(soup, base, r"/post/", "guland.vn")
    notice("guland danh sách Đông Thanh", "HTTP %s · URL cuối %s · tựa %s · %d link /post/ · mẫu: %s"
           % (r.status_code, r.url, c.text_of(soup.find("title"))[:120], len(links),
              " | ".join(u.split("/", 3)[-1][:90] for u in links[:12])))
    out = []
    for u in links[:6]:
        d = c.get("guland.vn", u)
        if d is None: continue
        s = c.soup_of(d)
        date, approx, ptot, pm2, area, addr, attrs = c.generic_detail(s)
        bc = c.text_of(s.select_one(".breadcrumb") or s.select_one("nav[aria-label*=read]") or s.select_one("ol"))[:140]
        out.append("%s · địa chỉ JSON-LD: %s · breadcrumb: %s" % (u.split("/", 3)[-1][:80], (addr or "")[:120], bc))
    notice("guland 6 tin đầu trang Đông Thanh", " | ".join(out))

if __name__ == "__main__":
    part_raw()
    try:
        part_live()
    except Exception as e:
        notice("guland trực tiếp lỗi", repr(e))
