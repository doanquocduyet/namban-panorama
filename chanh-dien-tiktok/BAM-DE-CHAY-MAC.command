#!/bin/bash
cd "$(dirname "$0")" || exit 1
if ! command -v node >/dev/null 2>&1; then
  echo "May chua cai Node.js. Tai ban LTS o https://nodejs.org roi chay lai file nay."
  open "https://nodejs.org/en/download"; read -r -p "Bam Enter de dong..."; exit 1
fi
if [ ! -d live/node_modules ]; then
  echo "Lan dau chay: dang cai thu vien, cho 1-2 phut..."
  (cd live && npm install --no-audit --no-fund) || { read -r -p "Cai loi. Bam Enter de dong..."; exit 1; }
fi
( sleep 2; open "http://localhost:3000/live/control.html" ) &
cd live && node server.mjs
