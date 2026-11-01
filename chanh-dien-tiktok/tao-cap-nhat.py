"""Sinh cap-nhat.txt: danh sách file cho nút CAP-NHAT-WINDOWS.bat. Chạy lại mỗi khi thêm/bớt file rồi commit.
   ghi-de = luôn thay bằng bản mới · giu = chỉ tải khi máy chưa có (ảnh, nhạc, bài giảng chú có thể đã sửa)."""
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {'node_modules', 'tts', 'cong-duc', '.git'}
SKIP_FILES = {'cau-hinh.json', 'cap-nhat.txt', 'tao-cap-nhat.py', 'CAP-NHAT-WINDOWS.bat', '.gitignore', '.gitattributes', '_headers'}
lines = ['# ghi-de: luon thay ban moi · giu: chi tai khi may chua co']
for d, dirs, files in os.walk(ROOT):
    dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
    for f in sorted(files):
        rel = os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')
        if f in SKIP_FILES and '/' not in rel: continue
        mode = 'giu' if rel.startswith(('assets/', 'bai-giang/')) else 'ghi-de'
        lines.append(f'{mode} {rel}')
open(os.path.join(ROOT, 'cap-nhat.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
print(len(lines) - 1, 'file')
