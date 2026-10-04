#!/usr/bin/env bash
# Mã hoá thư mục báo cáo từ khoá GSC (Panorama + Villas) trước khi commit vào repo công khai.
# Dùng trong .github/workflows/gsc-report.yml. Khoá công khai: scripts/gsc-public.pem.
# Khoá mở (riêng tư) nằm trong Google Drive của Chú — xem tools/gsc-decrypt.sh.
# Cách mã: khoá AES-256 ngẫu nhiên cho gói tar.gz, khoá AES được bọc bằng RSA-OAEP (SHA-256).
set -euo pipefail
IN="${1:-gsc-out}"
DEST="docs/gsc-private"
if [ ! -d "$IN" ] || [ -z "$(ls -A "$IN" 2>/dev/null)" ]; then
  echo "Không có báo cáo từ khoá để mã hoá."; exit 0
fi
mkdir -p "$DEST"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
tar -czf "$tmp/b.tgz" -C "$IN" .
openssl rand -hex 32 > "$tmp/k"
openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt -in "$tmp/b.tgz" -out "$DEST/latest.tgz.enc" -pass "file:$tmp/k"
openssl pkeyutl -encrypt -pubin -inkey scripts/gsc-public.pem \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -in "$tmp/k" -out "$DEST/latest.key.enc"
d="$(date -u +%F)"
cp "$DEST/latest.tgz.enc" "$DEST/$d.tgz.enc"; cp "$DEST/latest.key.enc" "$DEST/$d.key.enc"
rm -rf "$IN"
echo "Đã mã hoá → $DEST/latest.* và $DEST/$d.*"
