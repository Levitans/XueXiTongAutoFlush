chcp 65001
@echo off
set filename="newData.zip"
echo 正在下载程序

set curpath=%~dp0
cd /d %curpath%

C:\Windows\System32\WindowsPowerShell\v1.0\powershell curl -o %filename% "https://github.com/Levitans/XueXiTongAutoFlush/archive/refs/heads/master.zip"
if %ERRORLEVEL% == 0 (
    echo 程序下载成功
) else (
    echo 与服务器连接超时
    echo 请重试
    pause
    exit 2
)

package\bin\unzip newData.zip
copy /Y .\XueXiTongAutoFlush-master\package .\package
copy /Y .\XueXiTongAutoFlush-master\faithlearning.py .\

rmdir /S/Q XueXiTongAutoFlush-master
del /Q %filename%

echo 程序更新成功
pause