@echo off

:: 用此文件运行时路径中不能中文
set curpath=%~dp0
cd /d %curpath%

python --version >nul 2>nul
if %ERRORLEVEL% == 0 (
    goto start
) else (
    echo 系统中未找到Python
    echo 请安装Python后再运行程序
    echo 注意Python需要安装3.9以上版本
    pause
    exit 0
)

:start
if exist ".\venv" (
    .\venv\Scripts\python.exe faithlearning.py
) else (
    python -m venv .\venv
)