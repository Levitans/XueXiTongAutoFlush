chcp 65001
@echo off
set filename="newData.zip"
echo 正在下载程序

set curpath=%~dp0
cd /d %curpath%

C:\Windows\System32\WindowsPowerShell\v1.0\powershell curl -o %filename% "https://github.com/Levitans/XueXiTongAutoFlush/archive/refs/heads/master.zip"

package\bin\unzip newData.zip
copy /Y .\XueXiTongAutoFlush-master\package\learn .\package\learn
copy /Y .\XueXiTongAutoFlush-master\package\version.json .\package
copy /Y .\XueXiTongAutoFlush-master\faithlearning.py .\

rmdir /S/Q XueXiTongAutoFlush-master
del /Q %filename%

echo 程序更新成功
pause