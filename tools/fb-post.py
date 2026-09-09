#!/usr/bin/env python3
"""Đăng bài Facebook từ hàng đợi `data/fb-queue.json`.

Chạy trên GitHub Actions, KHÔNG chạy từ phiên Claude — `graph.facebook.com`
bị chặn ở đó (đã thử: mã trả về 000). Runner của GitHub thì gọi được.

Cách chạy: mỗi lần chạy lấy **một** bài đến hạn, đăng lên Trang, rồi đăng
link bài web vào **comment đầu tiên** (kỹ thuật ở `docs/facebook-panorama.md`
mục 1.2 — link ngoài đặt trong caption làm tụt tiếp cận).

Không có secret thì chạy khô (dry-run) và in ra bài sắp đăng. Nhờ vậy bật
workflow trước, cấp token sau, mà không có run nào đỏ.

CHỈ CẦN MỘT SECRET. Page Access Token đã tự gắn với đúng một Trang, nên
`GET /me` trả về chính Trang đó — không phải đi tìm Page ID dạng số. Script
tự hỏi, rồi **đối chiếu username trả về với `EXPECT_PAGE`**; lệch thì dừng,
không đăng. Đây là chốt chặn thật: token cấp nhầm Trang khác (Chú quản nhiều
Trang, bấm nhầm ở bước Get Page Access Token) sẽ bị bắt ngay, thay vì bài
Panorama rơi lên tường của một Trang khác rồi mới phát hiện.

Biến môi trường:
    FB_PAGE_TOKEN  — Page Access Token không hết hạn. BẮT BUỘC.
    FB_PAGE_ID     — tuỳ chọn, ép đăng vào một node cụ thể. Bỏ trống thì
                     script tự resolve từ token (đường đi thường dùng).
    FB_DRY_RUN     — đặt "1" để buộc chạy khô dù đã có token.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "fb-queue.json")
GRAPH = "https://graph.facebook.com/v21.0"
SITE = "https://nambanpanorama.com"

# Trang đích: facebook.com/nambanpanorama. Ghi cứng ở đây làm chốt chặn —
# token phải trỏ đúng Trang này thì mới đăng.
EXPECT_PAGE = "nambanpanorama"

# Chuỗi cấm — cùng danh sách với §2.1 CLAUDE.md. Bài Facebook cũng là mặt
# publication, nên chặn ngay ở đây thay vì trông vào người soạn nhớ.
BANNED = [
    "liên hệ ngay", "mua ngay", "đăng ký nhận giá", "trả lời trong ngày",
    "không cần đăng ký", "inbox ngay", "chốt ngay", "giá tốt nhất",
    "cam kết lời", "chỉ còn", "nhanh tay", "kẻo lỡ",
]


def load():
    with open(QUEUE, encoding="utf-8") as fh:
        return json.load(fh)


def save(q):
    with open(QUEUE, "w", encoding="utf-8") as fh:
        json.dump(q, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def check(post):
    """Chặn bài phạm luật TRƯỚC khi gọi API. Đăng rồi mới phát hiện thì
    đã nằm trên tường Trang, sửa cũng còn dấu."""
    errs = []
    text = (post.get("message", "") + " " + post.get("comment", "")).lower()
    for b in BANNED:
        if b in text:
            errs.append("chuỗi cấm §2.1: %r" % b)
    if not post.get("message", "").strip():
        errs.append("message rỗng")
    slug = post.get("slug")
    if slug and not os.path.exists(os.path.join(ROOT, slug + ".html")):
        errs.append("slug không tồn tại: /%s" % slug)
    return errs


def api(path, params, token):
    data = urllib.parse.urlencode(dict(params, access_token=token)).encode()
    req = urllib.request.Request(GRAPH + path, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def get(path, params, token):
    qs = urllib.parse.urlencode(dict(params, access_token=token))
    with urllib.request.urlopen(GRAPH + path + "?" + qs, timeout=60) as r:
        return json.loads(r.read().decode())


def resolve_page(token):
    """Hỏi token nó thuộc Trang nào, rồi đối chiếu với EXPECT_PAGE.

    Trả về (page_id, mô tả) nếu đúng Trang; ném RuntimeError nếu lệch.
    Không dùng `username` để đăng — Facebook cho Trang đổi username, còn id
    dạng số thì không đổi.
    """
    me = get("/me", {"fields": "id,name,username"}, token)
    uname = (me.get("username") or "").lower()
    if uname and uname != EXPECT_PAGE:
        raise RuntimeError(
            "Token trỏ tới Trang %r (%s), không phải %r. Không đăng."
            % (me.get("name"), uname, EXPECT_PAGE))
    if not uname:
        # Trang chưa đặt username thì không đối chiếu được — báo rõ để
        # người bấm nút tự nhìn tên, đừng lặng lẽ đăng bừa.
        print("CẢNH BÁO: Trang chưa có username. Tên Trang theo token: %r"
              % me.get("name"))
    return me["id"], "%s (%s)" % (me.get("name"), uname or "chưa có username")


def main():
    page = os.environ.get("FB_PAGE_ID", "").strip()
    token = os.environ.get("FB_PAGE_TOKEN", "").strip()
    dry = os.environ.get("FB_DRY_RUN") == "1" or not token

    queue = load()
    today = datetime.date.today().isoformat()
    due = [p for p in queue
           if not p.get("posted") and p.get("date", "9999") <= today]
    if not due:
        print("Không có bài nào đến hạn (hôm nay %s)." % today)
        return 0

    post = due[0]
    errs = check(post)
    if errs:
        print("DỪNG — bài %r không qua kiểm:" % post.get("slug"))
        for e in errs:
            print("   -", e)
        return 1

    link = "%s/%s" % (SITE, post["slug"]) if post.get("slug") else ""
    comment = post.get("comment", "").strip()
    if link and link not in comment:
        comment = (comment + "\n" + link).strip()

    if dry:
        print("=== CHẠY KHÔ (chưa có FB_PAGE_TOKEN) ===")
        print("Trang:", "facebook.com/" + EXPECT_PAGE)
        print("ngày :", post.get("date"))
        print("bài  :", link or "(không có link)")
        print("---- caption ----")
        print(post["message"])
        print("---- comment 1 ----")
        print(comment)
        print("=== hết. Chưa đăng gì lên Facebook. ===")
        return 0

    if not page:
        page, who = resolve_page(token)
        print("Đăng lên Trang:", who, "· id", page)

    res = api("/%s/feed" % page, {"message": post["message"]}, token)
    pid = res["id"]
    print("Đã đăng:", pid)

    if comment:
        c = api("/%s/comments" % pid, {"message": comment}, token)
        print("Đã đăng comment 1:", c["id"])

    post["posted"] = True
    post["post_id"] = pid
    post["posted_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(queue)
    print("Đã đánh dấu trong hàng đợi.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:
        print("DỪNG —", e, file=sys.stderr)
        sys.exit(1)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print("LỖI GRAPH API %s: %s" % (e.code, body), file=sys.stderr)
        sys.exit(1)
