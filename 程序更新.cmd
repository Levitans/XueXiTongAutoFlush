@echo off
set filename="newData.zip"
echo 正在下载新版本

:: 切换脚本的路径
set curpath=%~dp0
cd /d %curpath%

:: 获取github上的压缩包
powershell curl -o %filename% "https://github.com/Levitans/XueXiTongAutoFlush/archive/refs/heads/master.zip"

unzip newData.zip
copy /Y .\XueXiTongAutoFlush-master\package\learn .\package\learn
copy /Y .\XueXiTongAutoFlush-master\package\version.json .\package
copy /Y .\XueXiTongAutoFlush-master\faithlearning.py .\
copy /Y .\XueXiTongAutoFlush-master\README.md .\

:: 删除文件
rmdir /S/Q XueXiTongAutoFlush-master
del /Q %filename%

echo 程序更新成功
pause