@echo off
chcp 65001 > nul
title Crawl4AI 网页爬取工具

echo.
echo ================================================
echo    🌐 Crawl4AI 网页爬取工具
echo    正在启动图形界面...
echo ================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 系统中未找到Python
    echo.
    echo 请先安装Python 3.7或更高版本:
    echo    1. 访问 https://www.python.org/downloads/
    echo    2. 下载并安装最新版本的Python
    echo    3. 安装时勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM 运行启动脚本
python start_ui.py

REM 如果程序异常退出，暂停以便查看错误信息
if errorlevel 1 (
    echo.
    echo 程序异常退出，请检查上方的错误信息
    pause
)

exit /b 0 