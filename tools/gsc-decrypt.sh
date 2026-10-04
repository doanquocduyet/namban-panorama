#!/usr/bin/env bash
# Mở báo cáo từ khoá GSC đã mã hoá (docs/gsc-private/).
#   tools/gsc-decrypt.sh <file-khoá> [latest|YYYY-MM-DD] [thư-mục-ra]
# <file-khoá>: nội dung Google Doc "namban-panorama — khoá mở báo cáo GSC" trong Drive của Chú
# (dán nguyên văn cũng được — script tự lọc phần khoá, kể cả dấu \ mà Google Docs chèn trước "-----").
# Đừng commit khoá, đừng để thư mục ra nằm trong repo.
set -euo pipefail
KEY="$1"; WHICH="${2:-latest}"; OUT="${3:-${TMPDIR:-/tmp}/gsc-report}"
SRC="$(cd "$(dirname "$0")/.." && pwd)/docs/gsc-private"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
{ echo "-----BEGIN PRIVATE KEY-----"
  sed -n '/BEGIN PRIVATE KEY/,/END PRIVATE KEY/p' "$KEY" | grep -v 'PRIVATE KEY' | tr -d ' \r\\' | grep -v '^$'
  echo "-----END PRIVATE KEY-----"; } > "$tmp/p.pem"
openssl pkeyutl -decrypt -inkey "$tmp/p.pem" -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 \
  -in "$SRC/$WHICH.key.enc" -out "$tmp/k"
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in "$SRC/$WHICH.tgz.enc" -out "$tmp/b.tgz" -pass "file:$tmp/k"
mkdir -p "$OUT"; tar -xzf "$tmp/b.tgz" -C "$OUT"
echo "Đã mở → $OUT"; ls "$OUT"
