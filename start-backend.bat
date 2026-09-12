@echo off
chcp 65001 >nul
title xwzx-news - 后端服务 (FastAPI)

echo ============================================
echo   xwzx-news 后端启动
echo ============================================
echo.

cd /d "%~dp0backend"

if not exist ".env" (
    echo [!] 没有找到 .env，正在从 .env.example 创建...
    copy ".env.example" ".env" >nul
    echo [!] 请打开 backend\.env 填入真实的数据库密码，然后重新运行本脚本
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [!] 没有找到虚拟环境，正在创建...
    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)

echo [OK] 依赖就绪
echo.
echo [*] 服务地址  http://127.0.0.1:8000
echo [*] 接口文档  http://127.0.0.1:8000/docs
echo.
echo [*] 按 Ctrl+C 停止服务
echo.

.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

echo.
echo [*] 服务已停止
pause
