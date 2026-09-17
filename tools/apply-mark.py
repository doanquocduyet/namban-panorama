#!/usr/bin/env python3
"""Đánh dấu "đã đăng" lên bản hàng đợi MỚI NHẤT, không phải bản đã checkout.

Vì sao cần file này — lỗi thật 17/9/2026:

`actions/checkout` lấy **ảnh chụp kho tại commit lúc bấm nút chạy**, không
phải bản mới nhất. Nên trong một run có hai nhánh (Instagram rồi Threads),
nhánh sau vẫn cầm bản `fb-queue.json` cũ — không có dấu nhánh trước vừa đẩy
lên. Lúc push thì đụng độ, rebase báo CONFLICT, rồi `git rebase --continue`
chết vì runner không có trình soạn thảo:

    CONFLICT (content): Merge conflict in data/fb-queue.json
    error: Terminal is dumb, but EDITOR unset

Hậu quả nặng hơn cái lỗi đỏ: **bài đã đăng thật lên Threads mà hàng đợi
không ghi nhận** — lần chạy sau đăng lại lần nữa, người đọc thấy hai bài
trùng. Đây là kiểu hỏng im lặng, nguy hơn hỏng ồn.

Cách vá: script đăng bài không tự sửa hàng đợi trong repo nữa. Nó ghi một
**phiếu** `data/.pending-mark.json` nhỏ (slug, cột cần đánh dấu, id bài).
Workflow kéo bản `origin/main` mới nhất về, rồi chạy file này để dán phiếu
lên bản mới đó. Không còn hai bản chọi nhau, nên không còn đụng độ.

Chạy lại nhiều lần cũng không sao — đã đánh dấu rồi thì nó báo và thoát 0.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "fb-queue.json")
MARK = os.path.join(ROOT, "data", ".pending-mark.json")


def main():
    if not os.path.exists(MARK):
        print("Không có phiếu đánh dấu — không có gì để ghi.")
        return 0

    with open(MARK, encoding="utf-8") as fh:
        mark = json.load(fh)
    slug, field = mark["slug"], mark["field"]

    with open(QUEUE, encoding="utf-8") as fh:
        queue = json.load(fh)

    for post in queue:
        if post.get("slug") != slug:
            continue
        if post.get(field):
            print("Bài %r đã có dấu %r từ trước — không ghi đè." % (slug, field))
            return 0
        post[field] = True
        if mark.get("id"):
            post[field + "_id"] = mark["id"]
        if mark.get("at"):
            post[field + "_at"] = mark["at"]
        with open(QUEUE, "w", encoding="utf-8") as fh:
            json.dump(queue, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("Đã ghi %s = True cho /%s" % (field, slug))
        return 0

    # Slug biến mất khỏi hàng đợi giữa chừng — báo đỏ, đừng lặng lẽ bỏ qua.
    print("DỪNG — không tìm thấy /%s trong hàng đợi mới. Bài ĐÃ ĐĂNG nhưng "
          "chưa đánh dấu được, kiểm tay." % slug, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
