#!/usr/bin/env bash
# Nén video nền trang chủ về dưới 3MB, không tiếng, chuẩn web.
# Dùng:  ./nen-video.sh <file-goc> [so-giay]
set -e
SRC="$1"; SEC="${2:-10}"
[ -f "$SRC" ] || { echo "Không thấy file: $SRC"; exit 1; }
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
mkdir -p video
echo "Gốc: $(du -h "$SRC" | cut -f1)"
for CRF in 30 32 34 36; do
  "$FF" -y -hide_banner -loglevel error -i "$SRC" -t "$SEC" -an \
    -vf "scale='min(1920,iw)':-2:flags=lanczos,fps=25" \
    -c:v libx264 -crf $CRF -preset slow -pix_fmt yuv420p -profile:v high -level 4.0 \
    -movflags +faststart video/hero.mp4
  SZ=$(stat -c%s video/hero.mp4)
  echo "  crf $CRF → $((SZ/1024)) KB"
  [ "$SZ" -lt 3145728 ] && { echo "ĐẠT (<3MB) ở crf $CRF"; break; }
done
"$FF" -y -hide_banner -loglevel error -i video/hero.mp4 -vframes 1 -q:v 3 video/hero-poster.jpg
echo "Xong: video/hero.mp4 + video/hero-poster.jpg"
