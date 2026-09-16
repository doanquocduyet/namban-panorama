#!/usr/bin/env python3
"""Đăng bài Facebook từ hàng đợi `data/fb-queue.json`.

Chạy trên GitHub Actions, KHÔNG chạy từ phiên Claude — `graph.facebook.com`
bị chặn ở đó (đã thử: mã trả về 000). Runner của GitHub thì gọi được.

Cách chạy: mỗi lần chạy lấy **một** bài đến hạn, đăng **ảnh + caption** lên
Trang, rồi đăng link bài web vào **comment đầu tiên** (kỹ thuật ở
`docs/facebook-panorama.md` mục 1.2 — link ngoài đặt trong caption làm tụt
tiếp cận). Caption KHÔNG chứa link; link chỉ nằm ở comment.

Ảnh lấy theo thứ tự: trường `image` của bài trong hàng đợi → `og:image` đọc
thẳng từ `<slug>.html`. Nhờ vậy không phải khai ảnh cho từng bài — bài nào
cũng đã có og:image chuẩn 1200×630 (§3 CLAUDE.md). Không tìm ra ảnh thì
đăng chữ, không dừng.

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
import re
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

# Trần caption từng nền tảng. Facebook 63.206 ký tự — bài dài nhất của site
# chưa tới 9.000 nên đăng nguyên bài thoải mái. Instagram 2.200, không bài
# nào lọt, nên Instagram luôn rơi về câu mồi (xem `caption_for`).
FB_LIMIT = 63000
IG_LIMIT = 2200
THREADS_LIMIT = 500

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


def check(post, caption=None, comment=""):
    """Chặn bài phạm luật TRƯỚC khi gọi API. Đăng rồi mới phát hiện thì
    đã nằm trên tường Trang, sửa cũng còn dấu.

    Kiểm trên **caption thật sắp đăng**, không kiểm trên trường `message`.
    Từ 16/9/2026 caption có thể là nguyên bài bóc từ web, nên kiểm `message`
    là kiểm một chuỗi không ai đọc — đúng họ Luật 12 (file tồn tại không
    chứng minh nội dung đúng).
    """
    errs = []
    if caption is None:
        caption = post.get("message", "")
    text = (caption + " " + comment).lower()
    for b in BANNED:
        if b in text:
            errs.append("chuỗi cấm §2.1: %r" % b)
    if not caption.strip():
        errs.append("caption rỗng")
    # Chú chốt 16/9/2026: KHÔNG để link trong caption. Vừa là ý Chú, vừa
    # đúng mục 1.2 — link ngoài trong caption làm Facebook bóp tiếp cận.
    # Link chỉ nằm ở comment đầu tiên.
    if re.search(r"https?://|nambanpanorama\.com", caption):
        errs.append("caption có link — link phải để ở comment, không để trên bài")
    slug = post.get("slug")
    if slug and not os.path.exists(os.path.join(ROOT, slug + ".html")):
        errs.append("slug không tồn tại: /%s" % slug)
    return errs


def pick_image(post):
    """Tìm ảnh cho bài. Trả về (url tuyệt đối, đường dẫn tương đối) hoặc (None, lý do).

    Chú chốt 16/9/2026: đăng **bài + ảnh**, link để dưới comment. Ảnh không
    khai tay cho từng bài — mọi bài đã có `og:image` cắt chuẩn 1200×630, đó
    đúng là tấm dành cho mặt chia sẻ. Đọc thẳng từ HTML nên không phải nuôi
    thêm một danh sách dễ lệch.

    Kiểm file có thật trong repo trước khi đưa cho Facebook: Graph tải ảnh
    bằng cách tự đi lấy URL đó, đưa nhầm đường dẫn thì nó báo lỗi mơ hồ,
    khó dò hơn nhiều so với bắt ngay ở đây.
    """
    rel = (post.get("image") or "").strip()
    if not rel:
        slug = post.get("slug")
        if not slug:
            return None, "bài không có slug, cũng không khai ảnh"
        path = os.path.join(ROOT, slug + ".html")
        try:
            with open(path, encoding="utf-8") as fh:
                html = fh.read()
        except OSError as e:
            return None, "không đọc được %s.html (%s)" % (slug, e)
        m = re.search(
            r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html)
        if not m:
            return None, "/%s không có thẻ og:image" % slug
        rel = m.group(1)

    rel = rel.replace(SITE, "")
    if not rel.startswith("/"):
        rel = "/" + rel
    local = os.path.join(ROOT, rel.lstrip("/"))
    if not os.path.exists(local):
        return None, "ảnh không có trong repo: %s" % rel
    return SITE + rel, rel


def _grab_module():
    """Nạp `scripts/gen_audio_edge.py` làm module rời, không chạy phần main."""
    path = os.path.join(ROOT, "scripts", "gen_audio_edge.py")
    src = open(path, encoding="utf-8").read().split("\nif __name__")[0]
    g = {"__file__": path, "__name__": "gen_audio_edge"}
    exec(compile(src, path, "exec"), g)
    return g


def article_blocks(slug):
    """Bóc lời bài kèm **vai của từng khối** — h2, h3, p, li.

    Dùng lại nguyên bộ bóc của audio (`Grab` trong `gen_audio_edge.py`) thay
    vì viết bộ thứ hai: bộ đó đã chạy thật cho toàn bộ audio của site, đã
    biết bỏ `<figure>`, khối Nguồn, khối liên hệ, nút Nghe bài và mục "Đọc
    gì tiếp". Nuôi hai bộ bóc song song là nuôi hai cách hiểu "thân bài"
    khác nhau — đúng cái bẫy Luật 13b/13c.

    Chỉ kế thừa thêm một việc: nhớ lại thẻ của mỗi khối. Bản audio không cần
    biết đâu là tiêu đề vì giọng đọc tuần tự; bản Facebook thì cần, không
    thì mọi dòng bằng nhau và bài đọc ra như máy nhả chữ (Chú bắt 16/9/2026).
    """
    g = _grab_module()

    class Tagged(g["Grab"]):
        def __init__(self):
            super().__init__()
            self.tagged = []

        def handle_endtag(self, tag):
            cap, n = self.cap, len(self.parts)
            super().handle_endtag(tag)
            if cap and len(self.parts) > n:
                self.tagged.append((cap, self.parts[-1]))

    fp = os.path.join(ROOT, slug + ".html")
    raw = open(fp, encoding="utf-8").read()
    t = Tagged()
    t.feed(raw)
    blocks = t.tagged

    m = (re.search(r'<div class="art-header">.*?<h1>(.*?)</h1>', raw, re.S)
         or re.search(r"<h1>(.*?)</h1>", raw, re.S))
    h1 = ""
    if m:
        import html as _h
        h1 = re.sub(r"<[^>]+>", "", _h.unescape(m.group(1))).strip()
    if h1:
        blocks = [("h1", h1)] + [b for b in blocks if b[1] != h1]
    return blocks


# Vạch ngăn mục: ba gạch ngang đứng riêng một dòng — đúng lối vạch mảnh của
# trang (§2.3 "im lặng mà sang"). Facebook không có chữ đậm nên đây là cách
# tách mục mà không phải dùng emoji hay CHỮ HOA.
# Cố ý dùng em-dash chứ không dùng ký tự vạch dài lạ: em-dash có trong mọi
# bộ chữ, không sợ ra ô vuông trên máy Android đời cũ.
RULE = "———"


def article_text(slug):
    """Dựng lời bài thành một bài Facebook có nhịp, không phải một khối chữ.

    Bốn quy ước, rút từ chỗ Chú chê 16/9/2026 ("suông từ trên xuống"):
      • **Tựa** đứng riêng trên cùng.
      • **Mỗi mục H2** mở bằng một dòng vạch `⸻` rồi tới tên mục — mắt có
        chỗ nghỉ, biết bài đang sang phần khác.
      • **Câu hỏi FAQ (H3) dính liền câu trả lời** — cách nhau một lần xuống
        dòng thôi, còn giữa hai cặp mới là dòng trống. Hỏi và đáp đứng thành
        cặp thì đọc ra cặp; cách đều nhau thì đọc ra danh sách.
      • **Gạch đầu dòng** cho `<li>`, để danh sách ra danh sách.
    """
    out, i = [], 0
    blocks = article_blocks(slug)
    while i < len(blocks):
        tag, text = blocks[i]
        if tag == "h1":
            out.append(text)
        elif tag == "h2":
            out.append(RULE + "\n\n" + text)
        elif tag == "h3":
            # Gộp câu hỏi với câu trả lời ngay sau nó thành một khối.
            block = text
            while i + 1 < len(blocks) and blocks[i + 1][0] in ("p", "li"):
                nxt = blocks[i + 1][1]
                block += "\n" + ("· " + nxt if blocks[i + 1][0] == "li" else nxt)
                i += 1
            out.append(block)
        elif tag == "li":
            out.append("· " + text)
        else:
            out.append(text)
        i += 1
    return "\n\n".join(b for b in out if b.strip())


def caption_for(post, limit=None):
    """Caption cuối cùng cho một bài, kèm lý do đã chọn cái gì.

    Chú chốt 16/9/2026: đăng **100% nội dung như bài trên web**. Nên mặc
    định là nguyên bài; `"full": false` trong hàng đợi thì quay về câu mồi
    viết tay ở trường `message`.

    `limit` dành cho Instagram (2.200 ký tự). Bài đủ luôn dài hơn, nên khi
    vượt trần thì lùi về câu mồi thay vì cắt ngang giữa câu — cắt ngang là
    đăng một bài cụt, tệ hơn hẳn một câu mồi viết tử tế.
    """
    hook = post.get("message", "").strip()
    if not post.get("full", True) or not post.get("slug"):
        return hook, "câu mồi viết tay"
    try:
        body = article_text(post["slug"])
    except Exception as e:
        return hook, "không bóc được lời bài (%s) — dùng câu mồi" % e
    if not body.strip():
        return hook, "bóc ra rỗng — dùng câu mồi"
    # Hashtag chỉ nằm ở câu mồi viết tay, thân bài web không có. Đăng nguyên
    # bài mà bỏ luôn hashtag là mất một đường người ta tìm ra bài — nên nhặt
    # lại dòng hashtag cuối câu mồi, đắp xuống chân bài.
    tags = [ln.strip() for ln in hook.splitlines()
            if ln.strip().startswith("#")]
    tail = post.get("tail", "").strip()
    for extra in (tail, " ".join(tags)):
        if extra and extra not in body:
            body = body + "\n\n" + extra
    if limit and len(body) > limit:
        return hook, ("nguyên bài %d ký tự, quá trần %d — dùng câu mồi"
                      % (len(body), limit))
    return body, "nguyên bài, %d ký tự" % len(body)


def api(path, params, token):
    data = urllib.parse.urlencode(dict(params, access_token=token)).encode()
    req = urllib.request.Request(GRAPH + path, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def get(path, params, token):
    qs = urllib.parse.urlencode(dict(params, access_token=token))
    with urllib.request.urlopen(GRAPH + path + "?" + qs, timeout=60) as r:
        return json.loads(r.read().decode())


def token_info(token):
    """In hạn dùng của token ngay đầu log.

    Câu Chú hỏi 16/9/2026: "làm sao biết mã vĩnh viễn hay có hạn 2–3 tháng".
    Không ai nhớ đi kiểm Debugger định kỳ, nên script tự kiểm mỗi lần chạy.
    `expires_at = 0` nghĩa là không hết hạn — đó là thứ cần thấy.
    Token người dùng dài hạn sống 60 ngày; lấy nhầm một bậc là đúng hai
    tháng sau hệ thống chết mà không ai biết.
    """
    try:
        d = get("/debug_token", {"input_token": token}, token).get("data", {})
    except Exception as e:                      # không chặn việc đăng
        print("Không kiểm được hạn token (%s) — vẫn đăng tiếp." % e)
        return
    exp = d.get("expires_at", -1)
    typ = d.get("type", "?")
    if exp == 0:
        han = "KHÔNG HẾT HẠN"
    elif exp and exp > 0:
        left = (datetime.datetime.fromtimestamp(exp, datetime.timezone.utc)
                - datetime.datetime.now(datetime.timezone.utc)).days
        han = ("CÒN %d NGÀY (hết hạn %s) — token này sẽ chết, xem "
               "docs/facebook-panorama.md mục 0-A bước 3"
               % (left, datetime.date.fromtimestamp(exp).isoformat()))
    else:
        han = "không rõ"
    print("Token: loại %s · %s" % (typ, han))
    if typ != "PAGE":
        print("CẢNH BÁO: token KHÔNG phải loại PAGE. Token người dùng không "
              "đăng được lên Trang — lấy lại theo mục 0-A bước 2.")


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

    link = "%s/%s" % (SITE, post["slug"]) if post.get("slug") else ""
    comment = post.get("comment", "").strip()
    if link and link not in comment:
        comment = (comment + "\n" + link).strip()

    caption, why = caption_for(post, limit=FB_LIMIT)
    print("Caption:", why)

    errs = check(post, caption, comment)
    if errs:
        print("DỪNG — bài %r không qua kiểm:" % post.get("slug"))
        for e in errs:
            print("   -", e)
        return 1

    img, note = pick_image(post)

    if dry:
        print("=== CHẠY KHÔ — KHÔNG ĐĂNG GÌ ===")
        if token:
            print("(có token, nhưng ô \"Chạy khô\" đang để true)")
        else:
            print("(chưa có FB_PAGE_TOKEN)")
        print("Trang:", "facebook.com/" + EXPECT_PAGE)
        print("ngày :", post.get("date"))
        print("bài  :", link or "(không có link)")
        print("ảnh  :", img or "KHÔNG CÓ — sẽ đăng chữ (%s)" % note)
        print("---- caption (%s) ----" % why)
        print(caption)
        print("---- comment 1 ----")
        print(comment)
        print("=== hết. Chưa đăng gì lên Facebook. ===")
        return 0

    token_info(token)

    if not page:
        page, who = resolve_page(token)
        print("Đăng lên Trang:", who, "· id", page)

    if img:
        # /photos trả về `id` của ảnh và `post_id` của bài trên tường.
        # Comment phải gắn vào `post_id` thì mới nằm dưới bài.
        res = api("/%s/photos" % page,
                  {"url": img, "caption": caption, "published": "true"},
                  token)
        pid = res.get("post_id") or res["id"]
        print("Đã đăng ảnh + caption:", pid, "· ảnh", img)
    else:
        print("Không có ảnh (%s) — đăng chữ." % note)
        res = api("/%s/feed" % page, {"message": caption}, token)
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
