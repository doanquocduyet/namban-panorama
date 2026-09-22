#!/usr/bin/env python3
"""Đăng Instagram và Threads từ cùng hàng đợi `data/fb-queue.json`.

Chạy trên GitHub Actions, KHÔNG chạy từ phiên Claude — `graph.facebook.com`
và `graph.threads.net` đều bị chặn ở đó.

**Dùng chung hàng đợi với Facebook, cố ý.** Một bài viết một lần, ba nơi
cùng lấy. Nuôi ba hàng đợi song song là nuôi ba bản nội dung lệch nhau, và
sẽ lệch — chuyện đã thấy ở tầng dữ liệu mở (Luật 11).

Mỗi nền tảng có cột đánh dấu riêng trong hàng đợi:
    Facebook   -> "posted"
    Instagram  -> "posted_ig"
    Threads    -> "posted_threads"
Nhờ vậy ba nơi chạy độc lập, nơi này hỏng không kéo nơi kia dừng.

TRẦN CAPTION KHÁC NHAU — ĐÂY LÀ CHỖ DỄ HIỂU NHẦM NHẤT:
    Facebook   63.206 ký tự -> đăng NGUYÊN BÀI, không bài nào chạm trần.
    Instagram   2.200 ký tự -> không bài nào lọt, nên IG đăng CÂU MỒI.
    Threads       500 ký tự/bài -> đăng nguyên bài bằng CHUỖI TRẢ LỜI nối
                  nhau (đúng nếp Threads), bài đầu có ảnh, link ở bài chót.

Biến môi trường:
    PLATFORM            — "instagram" hoặc "threads". BẮT BUỘC.
    FB_PAGE_TOKEN       — Page token (Instagram dùng chung token với Trang).
    THREADS_TOKEN       — token riêng của Threads (lấy ở threads.net, khác
                          token Facebook — xem docs/facebook-panorama.md 0-C).
    SOCIAL_DRY_RUN      — "1" để chạy khô.
"""
import datetime
import importlib.util
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mượn thẳng bộ dùng chung của fb-post.py: load/save/check/pick_image/
# caption_for/article_text. Không chép lại — chép là tới lúc sửa luật §2.1
# thì sửa một chỗ, quên chỗ kia.
_spec = importlib.util.spec_from_file_location(
    "fbpost", os.path.join(ROOT, "tools", "fb-post.py"))
fb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fb)

SITE = fb.SITE
GRAPH = fb.GRAPH                                  # graph.facebook.com/v21.0
THREADS = "https://graph.threads.net/v1.0"

EXPECT_IG = "nambanpanorama"       # đối chiếu như EXPECT_PAGE bên Facebook
EXPECT_THREADS = "nambanpanorama"


def same_handle(a, b):
    """So tên tài khoản, bỏ qua dấu chấm và gạch dưới.

    Instagram không cho trùng tên với Trang Facebook nên tên Instagram của
    Panorama là `namban.panorama` — có dấu chấm, khác `nambanpanorama` bên
    Facebook. So nguyên văn thì chốt chặn báo lệch và từ chối đăng, dù đúng
    là tài khoản của mình (bắt được 16/9/2026, trước khi nó chặn thật).

    Bỏ dấu chấm với gạch dưới vẫn giữ nguyên tác dụng canh: tên một Trang
    khác của Chú (villas, greenspacers) vẫn lệch, vẫn bị chặn.
    """
    norm = lambda s: (s or "").lower().replace(".", "").replace("_", "")
    return norm(a) == norm(b)


def req(base, path, params, token, method="POST"):
    body = urllib.parse.urlencode(dict(params, access_token=token))
    if method == "GET":
        url = base + path + "?" + body
        r = urllib.request.Request(url, method="GET")
    else:
        r = urllib.request.Request(base + path, data=body.encode(),
                                   method="POST")
    with urllib.request.urlopen(r, timeout=90) as resp:
        return json.loads(resp.read().decode())


# ---------------------------------------------------------------- Instagram

def ig_target(token):
    """Tìm tài khoản Instagram đang gắn với Trang, rồi đối chiếu username.

    Cùng một chốt chặn với `resolve_page` bên Facebook: Chú quản nhiều tài
    khoản, token cấp nhầm thì bài Panorama rơi lên tường người khác.
    """
    page = fb.get("/me", {"fields": "id,name"}, token)["id"]
    d = req(GRAPH, "/%s" % page, {"fields": "instagram_business_account"},
            token, "GET")
    acc = d.get("instagram_business_account")
    if not acc:
        raise RuntimeError(
            "Trang chưa gắn tài khoản Instagram chuyên nghiệp. Làm theo "
            "docs/facebook-panorama.md mục 0-B rồi chạy lại.")
    ig = acc["id"]
    me = req(GRAPH, "/%s" % ig, {"fields": "username"}, token, "GET")
    uname = (me.get("username") or "").lower()
    if uname and not same_handle(uname, EXPECT_IG):
        raise RuntimeError("Token trỏ tới Instagram %r, không phải %r. "
                           "Không đăng." % (uname, EXPECT_IG))
    return ig, uname or "(chưa rõ username)"


def ig_post(token, caption, img, comment, dry):
    if not img:
        print("DỪNG — Instagram bắt buộc phải có ảnh, bài này không tìm ra ảnh.")
        return None
    ig, uname = ig_target(token) if not dry else ("(chạy khô)", EXPECT_IG)
    print("Instagram: @%s · id %s" % (uname, ig))
    if dry:
        return "(chạy khô)"
    c = req(GRAPH, "/%s/media" % ig, {"image_url": img, "caption": caption},
            token)["id"]
    # Facebook phải đi tải ảnh về trước khi publish được. Publish ngay thì
    # thỉnh thoảng dính lỗi "Media ID is not available" — chờ một nhịp.
    time.sleep(8)
    mid = req(GRAPH, "/%s/media_publish" % ig, {"creation_id": c}, token)["id"]
    print("Đã đăng Instagram:", mid)
    if comment:
        r = req(GRAPH, "/%s/comments" % mid, {"message": comment}, token)
        print("Đã đăng comment 1:", r["id"])
    return mid


# ------------------------------------------------------------------ Threads

def strip_tags(text):
    """Bỏ hashtag khỏi bản Threads.

    Threads **chỉ nhận một thẻ chủ đề mỗi bài**. Dòng hashtag kiểu Facebook
    (`#NamBan #LamHa #LamDong #HoTron`) ra kết quả xấu: nó lấy cái đầu làm
    thẻ rồi nuốt luôn dấu `#`, ba cái sau nằm trơ làm chữ thô. Thấy thật
    trên bài đăng 17/9/2026 — dòng cuối hiện `NamBan #LamHa #LamDong #HoTron`.

    Bỏ sạch cho gọn. Bản gói một bài (`th_one`) vốn không có hashtag vì nó
    dựng từ H1 + câu dẫn, nên chỉ nhánh câu mồi và nhánh nguyên bài cần lọc.
    """
    lines = [ln for ln in text.splitlines()
             if not re.fullmatch(r"\s*(#\S+\s*)+", ln)]
    out = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", out).strip()


def th_expiry(token):
    """In số ngày còn lại của token Threads ngay đầu log.

    Khác hẳn Facebook: Page token không hết hạn, còn token Threads **chỉ
    sống 60 ngày** và Meta chưa cho loại vĩnh viễn. Không ai nhớ đi kiểm
    định kỳ, nên script tự kiểm mỗi lần chạy và kêu to khi gần chết.
    Cùng họ với `token_info` bên fb-post.py.
    """
    try:
        d = req(THREADS, "/refresh_access_token",
                {"grant_type": "th_refresh_token"}, token, "GET")
    except Exception as e:
        print("Không kiểm được hạn token Threads (%s) — vẫn đăng tiếp." % e)
        return
    left = int(d.get("expires_in", 0)) // 86400
    print("Token Threads: còn %d ngày." % left)
    if left <= 14:
        print("CẢNH BÁO: token Threads sắp hết hạn. Lấy lại theo "
              "docs/facebook-panorama.md mục 0-C, rồi cập nhật secret "
              "THREADS_TOKEN.")


def th_target(token):
    th_expiry(token)
    me = req(THREADS, "/me", {"fields": "id,username"}, token, "GET")
    uname = (me.get("username") or "").lower()
    if uname and not same_handle(uname, EXPECT_THREADS):
        raise RuntimeError("Token trỏ tới Threads %r, không phải %r. "
                           "Không đăng." % (uname, EXPECT_THREADS))
    return me["id"], uname or "(chưa rõ username)"


def th_publish(token, uid, params):
    c = req(THREADS, "/%s/threads" % uid, params, token)["id"]
    time.sleep(5)
    return req(THREADS, "/%s/threads_publish" % uid,
               {"creation_id": c}, token)["id"]


def th_chain(text, limit=None):
    """Cắt nguyên bài thành chuỗi bài Threads, mỗi bài dưới trần ký tự.

    Cắt theo **ranh giới đoạn**, không cắt giữa câu. Cố ý KHÔNG dùng
    `chunk()` của `gen_audio_edge.py`: bộ đó cắt cho giọng đọc nên nó gộp
    mọi đoạn bằng một lần xuống dòng, làm mất hết dòng trống. Giọng đọc
    không cần dòng trống, mắt người thì cần — đó đúng là chỗ Chú chê
    16/9/2026 ("suông từ trên xuống").

    Vạch ngăn mục `———` không được đứng cuối một bài trong chuỗi: vạch là
    để mở mục mới, treo ở chân bài trước thì thành dấu cụt.
    """
    limit = limit or fb.THREADS_LIMIT
    out, cur = [], ""
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if cur and len(cur) + 2 + len(para) > limit:
            out.append(cur)
            cur = ""
        while len(para) > limit:        # đoạn đơn dài hơn trần thì đành cắt
            cut = para.rfind(" ", 0, limit) or limit
            out.append(para[:cut].strip())
            para = para[cut:].strip()
        cur = (cur + "\n\n" + para).strip() if cur else para
    if cur:
        out.append(cur)
    # Kéo vạch treo ở chân bài xuống đầu bài kế.
    for i in range(len(out) - 1):
        if out[i].rstrip().endswith(fb.RULE):
            out[i] = out[i].rstrip()[:-len(fb.RULE)].rstrip()
            out[i + 1] = fb.RULE + "\n\n" + out[i + 1]
    return [p for p in out if p.strip()]


def th_one(slug, link, limit=None):
    """Gói bài thành **một** bài Threads dưới trần, kèm link ngay trong bài.

    Chú hỏi 17/9/2026: "một bài ra tới 3 stt, tối ưu sao". Đây là câu trả
    lời — không cắt bài thành chuỗi, mà viết lại cho vừa một bài.

    Cách gói: lấy H1 làm dòng đầu, rồi **thêm từng câu một** của phần dẫn,
    dừng ngay trước câu làm tràn. Chừa sẵn chỗ cho link. Nhờ vậy bài luôn
    dứt ở ranh giới câu, không cụt giữa chừng.

    Hai luật nhỏ rút từ lần đo đầu:
      • **Không dừng ở câu kết thúc bằng dấu hai chấm** — câu đó hứa một
        danh sách phía sau, cắt ngay đó là hứa suông (cùng họ Luật 22).
      • Chỉ lấy tối đa ba đoạn đầu; xa hơn là thân bài, không phải phần dẫn.

    Trả về (text, số câu đã lấy). Không gói nổi thì trả (None, 0).
    """
    limit = limit or fb.THREADS_LIMIT
    blocks = fb.article_blocks(slug)
    h1 = next((t for tag, t in blocks if tag == "h1"), "")
    paras = [t for tag, t in blocks if tag == "p"][:3]
    room = limit - len(link) - 2
    if not h1 or len(h1) > room:
        return None, 0

    out, kept = h1, []
    for para in paras:
        for sent in re.findall(r"[^.!?…]+[.!?…]*", para):
            sent = sent.strip()
            if not sent:
                continue
            sep = "\n\n" if out == h1 else " "
            if len(out) + len(sep) + len(sent) > room:
                para = None
                break
            out += sep + sent
            kept.append(sent)
        if para is None:
            break

    # Câu chót hứa một danh sách ("…dễ bỏ qua:") thì bỏ, đừng hứa suông.
    while kept and kept[-1].rstrip().endswith(":"):
        out = out[:-(len(kept[-1]) + 1)].rstrip()
        kept.pop()

    if not kept:
        return None, 0
    return out + "\n\n" + link, len(kept)


def th_post(token, caption, img, comment, dry, one=None):
    uid, uname = th_target(token) if not dry else ("(chạy khô)", EXPECT_THREADS)
    print("Threads: @%s · id %s" % (uname, uid))
    if one:
        # Một bài duy nhất, link nằm ngay trong bài. Không nối chuỗi.
        posts = [one]
    else:
        posts = th_chain(caption)
        if comment:
            posts.append(comment)
    print("Chuỗi %d bài (trần %d ký tự/bài)" % (len(posts), fb.THREADS_LIMIT))
    if dry:
        for i, p in enumerate(posts, 1):
            print("---- bài %d/%d · %d ký tự ----" % (i, len(posts), len(p)))
            print(p)
        return "(chạy khô)"

    first = {"media_type": "IMAGE", "image_url": img, "text": posts[0]} \
        if img else {"media_type": "TEXT", "text": posts[0]}
    root = th_publish(token, uid, first)
    print("Đã đăng Threads:", root)
    prev = root
    for i, p in enumerate(posts[1:], 2):
        prev = th_publish(token, uid,
                          {"media_type": "TEXT", "text": p, "reply_to_id": prev})
        print("   nối bài %d/%d: %s" % (i, len(posts), prev))
    return root


# --------------------------------------------------------------------- main

def main():
    plat = os.environ.get("PLATFORM", "").strip().lower()
    if plat not in ("instagram", "threads"):
        print("DỪNG — PLATFORM phải là 'instagram' hoặc 'threads'.",
              file=sys.stderr)
        return 1

    token = os.environ.get(
        "THREADS_TOKEN" if plat == "threads" else "FB_PAGE_TOKEN", "").strip()
    dry = os.environ.get("SOCIAL_DRY_RUN") == "1" or not token
    mark = "posted_threads" if plat == "threads" else "posted_ig"

    queue = fb.load()
    today = datetime.date.today().isoformat()
    # Cùng thang ưu tiên với Facebook — xem fb.by_priority.
    due = sorted([p for p in queue
                  if not p.get(mark) and p.get("date", "9999") <= today],
                 key=fb.by_priority)
    if not due:
        print("Không có bài nào đến hạn cho %s (hôm nay %s)." % (plat, today))
        return 0

    post = due[0]
    print("Chọn: /%s (ưu tiên %s, hẹn %s) — còn %d bài đến hạn."
          % (post.get("slug"), post.get("priority", 5), post.get("date"), len(due)))
    link = "%s/%s" % (SITE, post["slug"]) if post.get("slug") else ""
    comment = post.get("comment", "").strip()
    if link and link not in comment:
        comment = (comment + "\n" + link).strip()

    # Instagram không lọt nguyên bài nên `caption_for` tự lùi về câu mồi.
    #
    # Threads cắt được nguyên bài thành chuỗi, nhưng một bài của site ra
    # **12–18 mắt xích** — đổ liên tiếp chừng đó lên một tài khoản mới thì
    # nhìn y như spam (Chú cản đúng lúc 17/9/2026, đã huỷ run đang chạy).
    # Nên mặc định Threads đăng **MỘT bài**, gói bằng `th_one`: H1 + mấy
    # câu dẫn đầu + link ngay trong bài. Đo thật cả 4 bài trong hàng đợi:
    # 324 / 466 / 395 / 489 ký tự — đều lọt.
    # Muốn nguyên bài thành chuỗi thì bật `THREADS_FULL=1` khi chạy tay.
    one = None
    if plat == "instagram":
        limit = fb.IG_LIMIT
    elif os.environ.get("THREADS_FULL") == "1":
        limit = None
    else:
        limit = fb.THREADS_LIMIT
        if post.get("slug"):
            one, nsent = th_one(post["slug"], link)
            if one:
                print("Threads: gói 1 bài · %d ký tự · %d câu dẫn"
                      % (len(one), nsent))
            else:
                print("Threads: không gói nổi 1 bài — lùi về chuỗi câu mồi.")
    caption, why = caption_and_log(post, limit, plat)
    if plat == "threads":
        # Câu mồi viết cho Facebook nên ghi "Bản đầy đủ ở comment". Trên
        # Threads link nằm trong bài hoặc ở bài nối, không phải comment.
        caption = caption.replace("ở comment", "ở dưới")
        caption = strip_tags(caption)

    # Bài một-mảnh CÓ link trong thân, nên miễn luật cấm link của `check`
    # (luật đó viết cho caption Facebook, nơi link làm tụt tiếp cận).
    errs = fb.check(post, one or caption, comment) if not one else [
        e for e in fb.check(post, one, comment) if "caption có link" not in e]
    if errs:
        print("DỪNG — bài %r không qua kiểm:" % post.get("slug"))
        for e in errs:
            print("   -", e)
        return 1

    img, note = fb.pick_image(post)
    print("ảnh:", img or "KHÔNG CÓ (%s)" % note)

    if dry:
        print("=== CHẠY KHÔ — KHÔNG ĐĂNG GÌ (%s) ===" % plat)
        if plat == "instagram":
            print("---- caption ----")
            print(caption)
            print("---- comment 1 ----")
            print(comment)
            print("(Instagram không cho link bấm được trong caption lẫn "
                  "comment — link chỉ để người đọc copy; chỗ bấm được là bio.)")
    if plat == "instagram":
        pid = ig_post(token, caption, img, comment, dry)
    else:
        pid = th_post(token, caption, img, comment, dry, one=one)
    if dry or pid is None:
        print("=== hết. Chưa đăng gì lên %s. ===" % plat)
        return 0 if pid is not None or dry else 1

    fb.mark_posted(post, mark, pid)
    return 0


def caption_and_log(post, limit, plat):
    caption, why = fb.caption_for(post, limit=limit)
    print("Caption %s: %s" % (plat, why))
    return caption, why


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:
        print("DỪNG —", e, file=sys.stderr)
        sys.exit(1)
    except urllib.error.HTTPError as e:
        print("LỖI API %s: %s" % (e.code, e.read().decode(errors="replace")),
              file=sys.stderr)
        sys.exit(1)
