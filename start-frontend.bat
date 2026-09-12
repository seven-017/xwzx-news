@echo off
chcp 65001 >nul
title xwzx-news - 前端服务 (Vite)

echo ============================================
echo   xwzx-news 前端启动
echo ============================================
echo.

cd /d "%~dp0frontend"

if not exist ".env" (
    echo [!] 没有找到 .env，正在从 .env.example 创建...
    copy ".env.example" ".env" >nul
    echo [!] 请打开 frontend\.env 填入自己的 AI API Key
    echo.
)

if not exist "node_modules" (
    echo [*] 没有找到 node_modules，正在安装依赖...
    npm install
)

echo [OK] 依赖就绪
echo.
echo [*] 前端地址  http://127.0.0.1:5173
echo [*] 提醒：页面要能正常显示，后端必须同时在运行
echo.
echo [*] 按 Ctrl+C 停止服务
echo.

npm run dev

echo.
echo [*] 服务已停止
pause
