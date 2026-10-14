#!/usr/bin/env python3
"""Chặn đổi tựa trang đang khoá hoặc đang có hạng (học từ Villas 13/10/2026).

Danh sách khoá: tools/title-locks.json (không lên web) — mỗi mục {slug, until, reason, title, h1}.
  until = "YYYY-MM-DD" (hết ngày đó thì thôi kiểm) hoặc "none" (khoá tới khi Chú gỡ).

  python3 tools/check-title-locks.py              kiểm; lệch thì in lỗi và thoát mã 1
  python3 tools/check-title-locks.py --update S   Chú đã duyệt đổi tựa trang S: ghi title/H1 mới vào danh sách

So theo chữ người đọc thấy (bỏ thẻ, &nbsp; thành dấu cách, gộp khoảng trắng), nên thêm &nbsp; hay <br>
để chống rớt chữ thì không tính là đổi tựa. Workflow title-lock-check.yml chạy file này mỗi lần main đổi.
"""
import datetime, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCKS = os.path.join(ROOT, "tools", "title-locks.json")


def raw_parts(slug):
    s0 = slug.strip("/")
    path = os.path.join(ROOT, s0 + ".html") if s0 else os.path.join(ROOT, "index.html")
    if s0 and not os.path.exists(path) and os.path.exists(os.path.join(ROOT, s0, "index.html")):
        path = os.path.join(ROOT, s0, "index.html")  # /en → en/index.html
    if not os.path.exists(path):
        return None, None, path
    s = open(path, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    h = re.search(r"<h1\b[^>]*>(.*?)</h1>", s, re.S)
    return (t.group(1) if t else ""), (h.group(1) if h else ""), path


def norm(x):
    x = re.sub(r"<br\s*/?>", " ", x or "")
    x = re.sub(r"<[^>]+>", "", x)
    x = html.unescape(x).replace("\xa0", " ")
    return re.sub(r"\s+", " ", x).strip()


def load():
    return json.load(open(LOCKS, encoding="utf-8"))


def active(lock, today):
    u = lock.get("until", "none")
    return u == "none" or today <= datetime.date.fromisoformat(u)


def main():
    data = load()
    if len(sys.argv) >= 3 and sys.argv[1] == "--update":
        slug = "/" + sys.argv[2].strip("/")
        hit = [l for l in data["locks"] if l["slug"] == slug]
        if not hit:
            sys.exit(f"Không có khoá cho {slug}")
        t, h, _ = raw_parts(slug)
        for l in hit:
            l["title"], l["h1"] = t, h
        json.dump(data, open(LOCKS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        open(LOCKS, "a", encoding="utf-8").write("\n")
        print(f"Đã ghi tựa mới của {slug} vào danh sách khoá.")
        return

    today = datetime.date.today()
    bad, checked = [], 0
    for l in data["locks"]:
        if not active(l, today):
            continue
        checked += 1
        t, h, path = raw_parts(l["slug"])
        rel = os.path.relpath(path, ROOT)
        if t is None:
            bad.append((rel, f"{l['slug']}: file không còn (khoá: {l['reason']})"))
            continue
        if norm(t) != norm(l["title"]):
            bad.append((rel, f"{l['slug']}: <title> đã đổi — khoá tới {l['until']} ({l['reason']}). "
                             f"Đang khoá: «{norm(l['title'])}» · Bây giờ: «{norm(t)}»"))
        if norm(h) != norm(l["h1"]):
            bad.append((rel, f"{l['slug']}: H1 đã đổi — khoá tới {l['until']} ({l['reason']}). "
                             f"Đang khoá: «{norm(l['h1'])}» · Bây giờ: «{norm(h)}»"))
    if bad:
        for rel, msg in bad:
            print(f"::error file={rel},title=Tựa đang khoá::{msg}")
        print(f"{len(bad)} chỗ lệch trên {checked} trang đang khoá. Đổi đúng ý Chú thì chạy "
              f"python3 tools/check-title-locks.py --update <slug>; không thì trả lại tựa cũ.")
        sys.exit(1)
    print(f"OK: {checked} trang đang khoá, title và H1 không đổi.")


if __name__ == "__main__":
    main()
