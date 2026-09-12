@echo off
chcp 65001 >nul
title xwzx-news - 一键启动

echo ============================================
echo   xwzx-news 一键启动（后端 + 前端）
echo ============================================
echo.
echo 即将分别打开两个窗口：
echo   1) 后端  http://127.0.0.1:8000/docs
echo   2) 前端  http://127.0.0.1:5173
echo.

start "xwzx-news 后端" cmd /k "%~dp0start-backend.bat"
timeout /t 3 >nul
start "xwzx-news 前端" cmd /k "%~dp0start-frontend.bat"

echo.
echo [OK] 两个服务已在新窗口启动。
echo [*] 想停止服务，直接关闭对应窗口即可。
echo.
pause
