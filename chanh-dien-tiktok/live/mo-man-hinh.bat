@echo off
rem Mo bang dieu khien + cua so overlay 9:16 rieng (Edge, khong bi lam cham khi bi che, tu phat tieng)
timeout /t 3 /nobreak >nul
start "" "http://localhost:3000/live/control.html"
start "" msedge --app="http://localhost:3000/live/overlay.html?auto=1" --window-size=540,960 --user-data-dir="%LOCALAPPDATA%\ChanhDienOverlay" --disable-backgrounding-occluded-windows --disable-renderer-backgrounding --disable-background-timer-throttling --autoplay-policy=no-user-gesture-required
exit
