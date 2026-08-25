#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sinh bản đồ ảnh cho namban-panorama.

Chạy:  python3 tools/gen-image-manifest.py
Kết quả: data/images-manifest.json  (máy đọc) + in tóm tắt ra màn hình.

Mục đích: mỗi phiên KHÔNG phải rà tay lại toàn bộ /images (tốn token + time).
Cứ chạy script này là ra ảnh nào dùng ở đâu, đóng vai gì, tấm nào chưa dùng.
NHỚ chạy lại mỗi khi thêm/xóa/đổi tên ảnh, rồi commit data/images-manifest.json.
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "images")

# quét mọi file văn bản có thể trỏ tới ảnh
TEXT_GLOBS = ["**/*.html", "**/*.css", "**/*.json", "**/*.xml", "**/*.txt", "**/*.js"]

def rel(p): return os.path.relpath(p, ROOT).replace("\\", "/")

def list_images():
    out = []
    for ext in ("webp", "jpg", "jpeg", "png", "svg", "gif", "avif"):
        out += glob.glob(os.path.join(IMG_DIR, f"*.{ext}"))
    return sorted(out, key=lambda p: os.path.basename(p).lower())

def dims(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return list(im.size)
    except Exception:
        return None

def load_texts():
    files = {}
    for g in TEXT_GLOBS:
        for p in glob.glob(os.path.join(ROOT, g), recursive=True):
            # bỏ file rác/tạm và chính manifest
            if "/node_modules/" in p or os.path.basename(p).startswith("_"):
                continue
            try:
                files[rel(p)] = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                pass
    return files

def roles_in(text, fname):
    """Trả về tập vai trò mà ảnh fname đóng trong 1 file văn bản."""
    esc = re.escape(fname)
    roles = set()
    # bắt từng dòng/đoạn ngắn chứa tên ảnh để đoán vai
    for m in re.finditer(r'.{0,80}images/' + esc + r'.{0,20}', text):
        seg = m.group(0)
        low = seg.lower()
        if "og:image" in low:            roles.add("og")
        elif "twitter:image" in low:     roles.add("twitter")
        elif '"image"' in low or '"logo"' in low or '"thumbnailurl"' in low:
            roles.add("schema")
        elif "<img" in low or "src=" in low: roles.add("display")
        elif "url(" in low:              roles.add("css")
        else:                            roles.add("ref")
    return roles

def main():
    texts = load_texts()
    imgs = list_images()
    manifest = {}
    unused = []
    for p in imgs:
        name = os.path.basename(p)
        used_in = {}
        for fpath, text in texts.items():
            if fpath.endswith("images-manifest.json"):
                continue
            if re.search(r'images/' + re.escape(name) + r'\b', text):
                r = roles_in(text, name)
                if r:
                    used_in[fpath] = sorted(r)
        entry = {
            "kb": round(os.path.getsize(p) / 1024),
            "dims": dims(p),
            "used_in": used_in,
        }
        if not used_in:
            entry["status"] = "unused"
            unused.append(name)
        manifest[name] = entry

    # sitemap-only = có trong image-sitemap nhưng không hiện <img>/og ở trang nào
    doc = {
        "_note": "Tự sinh bởi tools/gen-image-manifest.py — ĐỪNG sửa tay. "
                 "Chạy lại script này sau mỗi lần thêm/xóa/đổi ảnh rồi commit.",
        "_roles": {
            "display": "hiện trong <img> ở trang (người đọc thấy)",
            "og": "og:image — thumbnail chia sẻ Facebook/Zalo",
            "twitter": "twitter:image",
            "schema": "JSON-LD image/logo",
            "css": "nền qua url() trong CSS",
            "unused": "chưa trỏ ở đâu — dự trữ trong kho",
        },
        "total_images": len(imgs),
        "unused_count": len(unused),
        "unused": sorted(unused),
        "images": manifest,
    }
    outp = os.path.join(ROOT, "data", "images-manifest.json")
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    with open(outp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"Tổng ảnh: {len(imgs)} · chưa dùng: {len(unused)}")
    if unused:
        print("Chưa dùng:", ", ".join(sorted(unused)))
    print("Đã ghi:", rel(outp))

if __name__ == "__main__":
    main()
