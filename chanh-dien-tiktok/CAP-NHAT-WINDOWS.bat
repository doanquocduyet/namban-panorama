@echo off
chcp 65001 >nul
title Cap nhat Chanh Dien LIVE
cd /d "%~dp0"
echo.
echo  TAT cua so den "Chanh Dien LIVE" (neu dang chay) truoc khi cap nhat.
pause
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0cap-nhat.ps1"
if errorlevel 1 (
  echo.
  echo  [!] Cap nhat loi. Kiem tra mang Internet roi bam lai file nay.
  pause
  exit /b 1
)
if exist "live\node_modules" (
  pushd live
  call npm install --no-audit --no-fund
  popd
)
echo.
echo  Da cap nhat. Bam dup BAM-DE-CHAY-WINDOWS.bat de chay lai.
pause
