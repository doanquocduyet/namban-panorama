#!/usr/bin/env python3
"""Đính chính một bài ĐÃ ĐĂNG trên Facebook / Instagram / Threads.

Chạy trên GitHub Actions (workflow `social-fix.yml`), KHÔNG chạy từ phiên
Claude: token chỉ nằm trong secrets của repo.

Vì sao có file này — ca thật 10/10/2026: mục "xã gặp doanh nghiệp, nhà đầu
tư" đã đăng đủ ba nơi với số thu ngân sách cũ, sau đó xã sửa bản tin. Luật
là KHÔNG xoá bài, KHÔNG đăng lại bài mới (đăng lặp). Cách đính chính:
  - Facebook: sửa thẳng nội dung bài (thay đúng một câu). Không đọc được hay
    không sửa được thì trả lời ngay dưới bài.
  - Instagram, Threads: API không cho sửa chữ bài đã đăng, nên trả lời dưới bài.

Biến môi trường:
  FIX_KEY         key của mục trong data/fb-queue.json (bắt buộc)
  FIX_FB_FIND     câu cũ trong bài Facebook (để trống = không sửa, chỉ trả lời)
  FIX_FB_REPLACE  câu mới thay vào
  FIX_REPLY       câu trả lời dưới bài (bắt buộc)
  FIX_DRY_RUN=1   chỉ đọc và in, không ghi gì lên mạng xã hội
  FB_PAGE_TOKEN   token Trang (Facebook + Instagram)
  THREADS_TOKEN   token Threads

Chống trả lời trùng, hai lớp (review 10/10/2026 bắt được ca Re-run dùng lại
ảnh chụp kho cũ, chưa có dấu của lần trước):
  1. Dấu trong hàng đợi: mục đã có `fix_fb` / `fix_ig` / `fix_threads` thì bỏ
     qua kênh đó. Workflow kéo `origin/main` MỚI NHẤT trước khi chạy script.
  2. Đọc các trả lời đang có dưới bài: đã có đúng câu trả lời này thì không
     đăng nữa, chỉ ghi dấu.
Kết quả ghi vào phiếu `data/.pending-fix.json` sau MỖI kênh xong (kênh sau
hỏng thì kênh trước vẫn được ghi). Workflow dán phiếu lên `origin/main` mới
nhất bằng `python3 tools/social-fix.py --apply <phiếu>`.

Kết quả từng kênh in dạng `::notice::` để đọc được qua API check-runs
(log thô của Actions không đọc được từ phiên Claude).
"""
import datetime
import importlib.util
import json
import os
import sys
import time
import unicodedata
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "fb-queue.json")
PENDING = os.path.join(ROOT, "data", ".pending-fix.json")

_spec = importlib.util.spec_from_file_location(
    "social_post", os.path.join(ROOT, "tools", "social-post.py"))
sp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sp)
fb = sp.fb


def notice(title, msg, level="notice"):
    msg = str(msg).replace("%", "%25").replace("\r", " ").replace("\n", " ")
    print("::%s title=%s::%s" % (level, title, msg[:900]))


def http_err(e):
    try:
        return "%s %s" % (e.code, e.read().decode()[:500])
    except Exception:
        return repr(e)


def norm(s):
    return " ".join(unicodedata.normalize("NFC", s or "").replace("\xa0", " ").split())


def load_queue():
    with open(QUEUE, encoding="utf-8") as fh:
        return json.load(fh)


def find_item(q, key):
    hits = [x for x in q if x.get("key") == key]
    if len(hits) != 1:
        raise SystemExit("DỪNG — key %r khớp %d mục trong hàng đợi." % (key, len(hits)))
    return hits[0]


def write_pending(key, results):
    with open(PENDING, "w", encoding="utf-8") as fh:
        json.dump({"key": key, "results": results}, fh, ensure_ascii=False, indent=2)


def apply(path):
    """Dán phiếu lên bản hàng đợi hiện có trên đĩa (workflow đã reset về main)."""
    with open(path, encoding="utf-8") as fh:
        mark = json.load(fh)
    q = load_queue()
    item = find_item(q, mark["key"])
    changed = []
    for k, v in mark["results"].items():
        if not k.startswith("fix_"):
            continue
        if item.get(k):
            print("Đã có %s từ trước — giữ nguyên." % k)
            continue
        item[k] = v
        changed.append(k)
    if changed:
        with open(QUEUE, "w", encoding="utf-8") as fh:
            json.dump(q, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("Đã ghi:", ", ".join(changed))
    return 0


def already_replied(texts, reply):
    r = norm(reply)
    return any(norm(t) == r for t in texts)


def fb_comments(pid, tok):
    d = fb.get("/%s/comments" % pid, {"fields": "message", "limit": "100"}, tok)
    return [c.get("message", "") for c in d.get("data", [])]


def ig_comments(mid, tok):
    d = sp.req(sp.GRAPH, "/%s/comments" % mid, {"fields": "text", "limit": "100"}, tok, "GET")
    return [c.get("text", "") for c in d.get("data", [])]


def th_replies(tid, tok):
    d = sp.req(sp.THREADS, "/%s/replies" % tid, {"fields": "text"}, tok, "GET")
    return [c.get("text", "") for c in d.get("data", [])]


def main():
    key = os.environ.get("FIX_KEY", "").strip()
    find = norm(os.environ.get("FIX_FB_FIND", ""))
    repl = norm(os.environ.get("FIX_FB_REPLACE", ""))
    reply = norm(os.environ.get("FIX_REPLY", ""))
    dry = os.environ.get("FIX_DRY_RUN") == "1"
    fbtok = os.environ.get("FB_PAGE_TOKEN", "").strip()
    thtok = os.environ.get("THREADS_TOKEN", "").strip()
    if not key or not reply:
        raise SystemExit("DỪNG — thiếu FIX_KEY hoặc FIX_REPLY.")
    if bool(find) != bool(repl):
        raise SystemExit("DỪNG — FIX_FB_FIND và FIX_FB_REPLACE phải đi cùng nhau.")
    if len(reply) > 480:
        raise SystemExit("DỪNG — câu trả lời %d ký tự, Threads chỉ nhận tới 500." % len(reply))
    item = find_item(load_queue(), key)
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    results = {}
    failed = []
    print("Mục:", key, "· chạy khô" if dry else "· CHẠY THẬT")

    def done(field, value, title):
        notice(title, value)
        if not dry:
            results[field] = value
            write_pending(key, results)

    # ---------------------------------------------------------------- Facebook
    pid = item.get("posted_id")
    if item.get("fix_fb"):
        notice("Facebook", "đã đính chính từ trước (%s) — bỏ qua" % item["fix_fb"])
    elif not pid or not fbtok:
        notice("Facebook", "bỏ qua — thiếu id bài hoặc FB_PAGE_TOKEN")
    else:
        try:
            page, who = fb.resolve_page(fbtok)
            if not pid.startswith(page + "_"):
                raise RuntimeError("bài %s không thuộc Trang %s (%s)" % (pid, page, who))
            cur = None
            try:
                raw = fb.get("/%s" % pid, {"fields": "message"}, fbtok).get("message", "")
                cur = unicodedata.normalize("NFC", raw).replace("\xa0", " ")
            except urllib.error.HTTPError as e:
                notice("Facebook đọc lỗi", http_err(e) + " — chuyển sang trả lời")
            n_old = cur.count(find) if (cur is not None and find) else 0
            n_new = cur.count(repl) if (cur is not None and find) else 0
            if cur is not None:
                notice("Facebook đọc", "Trang %s · bài %s · %d ký tự · câu cũ %d lần · câu mới %d lần"
                       % (who, pid, len(cur), n_old, n_new))
            if find and cur is not None and n_old == 0 and n_new >= 1:
                done("fix_fb", "sửa bài (đã có câu mới từ trước) " + stamp, "Facebook xong")
            elif dry:
                notice("Facebook (chạy khô)", "sẽ sửa thẳng nội dung" if n_old == 1
                       else "sẽ trả lời dưới bài (nếu chưa có câu trả lời y hệt)")
            else:
                edited = False
                if find and n_old == 1:
                    try:
                        res = fb.api("/%s" % pid, {"message": cur.replace(find, repl)}, fbtok)
                        notice("Facebook sửa", "API trả về %s" % json.dumps(res, ensure_ascii=False))
                        for wait in (0, 6):
                            time.sleep(wait)
                            try:
                                after = fb.get("/%s" % pid, {"fields": "message"}, fbtok).get("message", "")
                            except urllib.error.HTTPError as e:
                                notice("Facebook đọc lại lỗi", http_err(e))
                                after = ""
                            after = unicodedata.normalize("NFC", after).replace("\xa0", " ")
                            if repl in after and find not in after:
                                edited = True
                                break
                        if not edited and res.get("success") is True:
                            # API báo thành công: tin API, KHÔNG trả lời thêm (tránh
                            # đính chính hai lần). Ghi rõ là chưa đọc lại được.
                            edited = True
                            notice("Facebook sửa", "API báo success nhưng đọc lại chưa thấy câu mới — coi như đã sửa, không trả lời thêm")
                    except urllib.error.HTTPError as e:
                        notice("Facebook sửa lỗi", http_err(e) + " — chuyển sang trả lời")
                if edited:
                    done("fix_fb", "sửa bài " + stamp, "Facebook xong")
                else:
                    try:
                        existing = fb_comments(pid, fbtok)
                    except urllib.error.HTTPError as e:
                        existing = []
                        notice("Facebook đọc bình luận lỗi", http_err(e) + " — chỉ dựa vào dấu trong hàng đợi")
                    if already_replied(existing, reply):
                        done("fix_fb", "đã có trả lời y hệt từ trước " + stamp, "Facebook xong")
                    else:
                        c = fb.api("/%s/comments" % pid, {"message": reply}, fbtok)
                        done("fix_fb", "trả lời %s %s" % (c["id"], stamp), "Facebook xong")
        except urllib.error.HTTPError as e:
            failed.append("facebook")
            notice("Facebook lỗi", http_err(e), "error")
        except Exception as e:
            failed.append("facebook")
            notice("Facebook lỗi", repr(e), "error")

    # --------------------------------------------------------------- Instagram
    mid = item.get("posted_ig_id")
    if item.get("fix_ig"):
        notice("Instagram", "đã đính chính từ trước (%s) — bỏ qua" % item["fix_ig"])
    elif not mid or not fbtok:
        notice("Instagram", "bỏ qua — thiếu id bài hoặc FB_PAGE_TOKEN")
    else:
        try:
            ig, uname = sp.ig_target(fbtok)
            try:
                existing = ig_comments(mid, fbtok)
            except urllib.error.HTTPError as e:
                existing = []
                notice("Instagram đọc bình luận lỗi", http_err(e) + " — chỉ dựa vào dấu trong hàng đợi")
            notice("Instagram đọc", "@%s · bài %s · %d bình luận" % (uname, mid, len(existing)))
            if already_replied(existing, reply):
                done("fix_ig", "đã có trả lời y hệt từ trước " + stamp, "Instagram xong")
            elif dry:
                notice("Instagram (chạy khô)", "sẽ trả lời dưới bài")
            else:
                r = sp.req(sp.GRAPH, "/%s/comments" % mid, {"message": reply}, fbtok)
                done("fix_ig", "trả lời %s %s" % (r["id"], stamp), "Instagram xong")
        except urllib.error.HTTPError as e:
            failed.append("instagram")
            notice("Instagram lỗi", http_err(e), "error")
        except Exception as e:
            failed.append("instagram")
            notice("Instagram lỗi", repr(e), "error")

    # ----------------------------------------------------------------- Threads
    tid = item.get("posted_threads_id")
    if item.get("fix_threads"):
        notice("Threads", "đã đính chính từ trước (%s) — bỏ qua" % item["fix_threads"])
    elif not tid or not thtok:
        notice("Threads", "bỏ qua — thiếu id bài hoặc THREADS_TOKEN")
    else:
        try:
            if dry:
                # Chạy khô chỉ đọc: không gọi th_target (nó gia hạn token).
                me = sp.req(sp.THREADS, "/me", {"fields": "id,username"}, thtok, "GET")
                uid, uname = me["id"], (me.get("username") or "")
                if uname and not sp.same_handle(uname.lower(), sp.EXPECT_THREADS):
                    raise RuntimeError("Token trỏ tới Threads %r" % uname)
            else:
                uid, uname = sp.th_target(thtok)
            existing = None
            try:
                existing = th_replies(tid, thtok)
            except urllib.error.HTTPError as e:
                notice("Threads đọc trả lời lỗi", http_err(e) + " — chỉ dựa vào dấu trong hàng đợi")
            notice("Threads đọc", "@%s · bài %s · câu trả lời %d ký tự · %s"
                   % (uname, tid, len(reply),
                      "chưa đọc được trả lời" if existing is None else "%d trả lời" % len(existing)))
            if existing is not None and already_replied(existing, reply):
                done("fix_threads", "đã có trả lời y hệt từ trước " + stamp, "Threads xong")
            elif dry:
                notice("Threads (chạy khô)", "sẽ trả lời dưới bài")
            else:
                rid = sp.th_publish(thtok, uid, {"media_type": "TEXT", "text": reply,
                                                 "reply_to_id": tid})
                done("fix_threads", "trả lời %s %s" % (rid, stamp), "Threads xong")
        except urllib.error.HTTPError as e:
            failed.append("threads")
            notice("Threads lỗi", http_err(e), "error")
        except Exception as e:
            failed.append("threads")
            notice("Threads lỗi", repr(e), "error")

    if failed:
        print("Kênh lỗi:", ", ".join(failed), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--apply":
        sys.exit(apply(sys.argv[2]))
    sys.exit(main())
