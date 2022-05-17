@echo off

chdir | cd

python --version >nul 2>nul
if %ERRORLEVEL% == 0 (
    goto start
) else (
    echo 系统中未找到 Python
    echo 请确认系统中是否有安装 Python
    echo 若有安装 Python 则可能没有配置 Python 环境变量
    echo 若没有安装 Python 可访问下面地址下载 Python3.9.0 安装包
    echo https://cdn.npmmirror.com/binaries/python/3.9.0/python-3.9.0.exe
    echo 注意 Python 需要安装3.9.0及以上版本
    pause
    exit 0
)

:start
if exist ".\venv" (
    .\venv\Scripts\python.exe .\faithlearning.py
) else (
    echo 当前目录未找到虚拟环境
    echo 正在为你创建虚拟环境
    python -m venv .\venv
    echo 虚拟环境创建成功
    goto start
)
pause
exit 0