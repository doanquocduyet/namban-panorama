@echo off
chcp 65001 >nul
title Chanh Dien LIVE
cd /d "%~dp0"

where node >nul 2>nul
if errorlevel 1 (
  echo.
  echo  [!] May chua cai Node.js.
  echo      Mo trang https://nodejs.org , bam nut LTS de tai, cai xong thi bam lai file nay.
  echo.
  start "" "https://nodejs.org/en/download"
  pause
  exit /b 1
)

if not exist "live\node_modules" (
  echo  Lan dau chay: dang cai thu vien, cho 1-2 phut...
  pushd live
  call npm install --no-audit --no-fund
  if errorlevel 1 (
    echo  [!] Cai thu vien loi. Kiem tra mang Internet roi bam lai file nay.
    popd
    pause
    exit /b 1
  )
  popd
)

echo.
echo  Dang mo bang dieu khien va cua so live 9:16... (DUNG TAT cua so den nay trong luc live)
start "" /min "%~dp0live\mo-man-hinh.bat"
cd live
node server.mjs
pause
