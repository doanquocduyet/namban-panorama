#!/usr/bin/env python3
"""Đính chính một bài ĐÃ ĐĂNG trên Facebook / Instagram / Threads.

Chạy trên GitHub Actions (workflow `social-fix.yml`), KHÔNG chạy từ phiên
Claude: token chỉ nằm trong secrets của repo.

Vì sao có file này — ca thật 10/10/2026: mục "xã gặp doanh nghiệp, nhà đầu
tư" đã đăng đủ ba nơi với số thu ngân sách cũ, sau đó xã sửa bản tin. Luật
§0 là KHÔNG xoá bài, KHÔNG đăng lại bài mới (đăng lặp). Cách đính chính:
  - Facebook: sửa thẳng nội dung bài (thay đúng một câu). Sửa không được thì
    trả lời ngay dưới bài.
  - Instagram, Threads: API không cho sửa chữ bài đã đăng, nên trả lời dưới bài.

Biến môi trường:
  FIX_KEY         key của mục trong data/fb-queue.json (bắt buộc)
  FIX_FB_FIND     câu cũ trong bài Facebook (để trống = không sửa, chỉ trả lời)
  FIX_FB_REPLACE  câu mới thay vào
  FIX_REPLY       câu trả lời dưới bài (bắt buộc)
  FIX_DRY_RUN=1   chỉ đọc và in, không ghi gì lên mạng xã hội
  FB_PAGE_TOKEN   token Trang (Facebook + Instagram)
  THREADS_TOKEN   token Threads

Mỗi kênh chỉ làm MỘT lần: mục trong hàng đợi đã có `fix_fb` / `fix_ig` /
`fix_threads` thì bỏ qua kênh đó, nên bấm chạy lại không sinh trả lời trùng.
Kết quả ghi vào phiếu `data/.pending-fix.json` sau MỖI kênh xong (kênh sau
hỏng thì kênh trước vẫn được ghi). Workflow dán phiếu lên `origin/main` mới
nhất bằng `python3 tools/social-fix.py --apply <phiếu>` — cùng cách
`tools/apply-mark.py` tránh đụng độ khi push.

Kết quả từng kênh in thêm dạng `::notice::` để đọc được qua API check-runs
(log thô của Actions không đọc được từ phiên Claude).
"""
import datetime
import importlib.util
import json
import os
import sys
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "fb-queue.json")
PENDING = os.path.join(ROOT, "data", ".pending-fix.json")

_spec = importlib.util.spec_from_file_location(
    "social_post", os.path.join(ROOT, "tools", "social-post.py"))
sp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sp)
fb = sp.fb


def notice(title, msg):
    msg = str(msg).replace("\n", " ").replace("::", ": ")
    print("::notice title=%s::%s" % (title, msg[:900]))


def http_err(e):
    try:
        return "%s %s" % (e.code, e.read().decode()[:500])
    except Exception:
        return str(e)


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
    changed = False
    for k, v in mark["results"].items():
        if not k.startswith("fix_"):
            continue
        if item.get(k):
            print("Đã có %s từ trước — giữ nguyên." % k)
            continue
        item[k] = v
        changed = True
    if changed:
        with open(QUEUE, "w", encoding="utf-8") as fh:
            json.dump(q, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("Đã ghi:", ", ".join(k for k in mark["results"] if k.startswith("fix_")))
    return 0


def main():
    key = os.environ.get("FIX_KEY", "").strip()
    find = os.environ.get("FIX_FB_FIND", "").strip()
    repl = os.environ.get("FIX_FB_REPLACE", "").strip()
    reply = os.environ.get("FIX_REPLY", "").strip()
    dry = os.environ.get("FIX_DRY_RUN") == "1"
    fbtok = os.environ.get("FB_PAGE_TOKEN", "").strip()
    thtok = os.environ.get("THREADS_TOKEN", "").strip()
    if not key or not reply:
        raise SystemExit("DỪNG — thiếu FIX_KEY hoặc FIX_REPLY.")
    if bool(find) != bool(repl):
        raise SystemExit("DỪNG — FIX_FB_FIND và FIX_FB_REPLACE phải đi cùng nhau.")
    item = find_item(load_queue(), key)
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    results = {}
    failed = []
    print("Mục:", key, "· chạy khô" if dry else "· CHẠY THẬT")

    # ---------------------------------------------------------------- Facebook
    pid = item.get("posted_id")
    if item.get("fix_fb"):
        notice("Facebook", "đã đính chính từ trước (%s) — bỏ qua" % item["fix_fb"])
    elif not pid or not fbtok:
        notice("Facebook", "bỏ qua — thiếu id bài hoặc FB_PAGE_TOKEN")
    else:
        try:
            cur = fb.get("/%s" % pid, {"fields": "message"}, fbtok).get("message", "")
            n_old, n_new = (cur.count(find), cur.count(repl)) if find else (0, 0)
            notice("Facebook đọc", "bài %s · %d ký tự · câu cũ %d lần · câu mới %d lần"
                   % (pid, len(cur), n_old, n_new))
            done = None
            if find and n_old == 0 and n_new >= 1:
                done = "sửa bài (đã có câu mới từ trước) " + stamp
            elif not dry and find and n_old == 1:
                try:
                    fb.api("/%s" % pid, {"message": cur.replace(find, repl)}, fbtok)
                    after = fb.get("/%s" % pid, {"fields": "message"}, fbtok).get("message", "")
                    if repl in after and find not in after:
                        done = "sửa bài " + stamp
                    else:
                        notice("Facebook sửa", "API trả về nhưng nội dung chưa đổi — chuyển sang trả lời")
                except urllib.error.HTTPError as e:
                    notice("Facebook sửa lỗi", http_err(e) + " — chuyển sang trả lời")
            if dry:
                notice("Facebook (chạy khô)", "sẽ %s" % (
                    "sửa thẳng nội dung" if n_old == 1 else "trả lời dưới bài"))
            elif not done:
                c = fb.api("/%s/comments" % pid, {"message": reply}, fbtok)
                done = "trả lời %s %s" % (c["id"], stamp)
            if done and not dry:
                results["fix_fb"] = done
                notice("Facebook xong", done)
                write_pending(key, results)
        except urllib.error.HTTPError as e:
            failed.append("facebook")
            notice("Facebook lỗi", http_err(e))
        except Exception as e:
            failed.append("facebook")
            notice("Facebook lỗi", repr(e))

    # --------------------------------------------------------------- Instagram
    mid = item.get("posted_ig_id")
    if item.get("fix_ig"):
        notice("Instagram", "đã đính chính từ trước (%s) — bỏ qua" % item["fix_ig"])
    elif not mid or not fbtok:
        notice("Instagram", "bỏ qua — thiếu id bài hoặc FB_PAGE_TOKEN")
    else:
        try:
            ig, uname = sp.ig_target(fbtok)
            notice("Instagram đọc", "@%s · bài %s" % (uname, mid))
            if dry:
                notice("Instagram (chạy khô)", "sẽ trả lời dưới bài")
            else:
                r = sp.req(sp.GRAPH, "/%s/comments" % mid, {"message": reply}, fbtok)
                results["fix_ig"] = "trả lời %s %s" % (r["id"], stamp)
                notice("Instagram xong", results["fix_ig"])
                write_pending(key, results)
        except urllib.error.HTTPError as e:
            failed.append("instagram")
            notice("Instagram lỗi", http_err(e))
        except Exception as e:
            failed.append("instagram")
            notice("Instagram lỗi", repr(e))

    # ----------------------------------------------------------------- Threads
    tid = item.get("posted_threads_id")
    if item.get("fix_threads"):
        notice("Threads", "đã đính chính từ trước (%s) — bỏ qua" % item["fix_threads"])
    elif not tid or not thtok:
        notice("Threads", "bỏ qua — thiếu id bài hoặc THREADS_TOKEN")
    else:
        try:
            uid, uname = sp.th_target(thtok)
            notice("Threads đọc", "@%s · bài %s · câu trả lời %d ký tự" % (uname, tid, len(reply)))
            if dry:
                notice("Threads (chạy khô)", "sẽ trả lời dưới bài")
            else:
                rid = sp.th_publish(thtok, uid, {"media_type": "TEXT", "text": reply,
                                                 "reply_to_id": tid})
                results["fix_threads"] = "trả lời %s %s" % (rid, stamp)
                notice("Threads xong", results["fix_threads"])
                write_pending(key, results)
        except urllib.error.HTTPError as e:
            failed.append("threads")
            notice("Threads lỗi", http_err(e))
        except Exception as e:
            failed.append("threads")
            notice("Threads lỗi", repr(e))

    if failed:
        print("Kênh lỗi:", ", ".join(failed), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--apply":
        sys.exit(apply(sys.argv[2]))
    sys.exit(main())
