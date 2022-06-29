# -*- encoding = utf-8 -*-
# @Time : 2022-06-29 23:17
# @Author : Levitan
# @File : boot.py
# @Software : PyCharm
import re
import os
import sys
import traceback

# 判断系统中的 Python 版本是否满足要求
def python_version_detect():
    pattern = re.compile(r"\d+\d*")
    versionStr = sys.version.split(" ")[0].replace(".", "")
    versionNumber = re.search(pattern, versionStr)
    if versionNumber is None:
        print("获取系统 Python 版本时出现异常")
        eixt(233)
    local_version = int(versionNumber.group())
    if local_version < 390:
        print("当前系统中 Python 版本过低")
        print("程序运行依赖 3.9 及以上版本的Python")
        print("可以访问 https://cdn.npmmirror.com/binaries/python/3.9.0/python-3.9.0.exe 下载Python3.9.0安装包")
        print("安装新 Python 后请手动删除，当前文件夹下的 venv 文件夹")
        exit(233)

# 检测依赖是否存在
def isDependencyReady():
    try:
        # 检测依赖是否存在
        import selenium
        import requests
        import colorama
        import fontTools
    except ModuleNotFoundError as e:
        print("依赖导入失败")
        try_install_library()

# 检测配置文件是否正确
def initGlobalVar():
    from package.learn import exception
    from package.learn import globalvar
    from package.learn import color
    try:
        globalvar.init_global()
    except exception.InitializationException as e:
        print(color.read("程序初始化异常"))
        print("异常信息："+str(e)+"\n")
        input("输入回车退出程序...")
        exit(233)

# 自动安装依赖
def try_install_library():
    print("检测到未安装所需要的第三方库")
    haveVenv = os.path.exists("./venv")
    if haveVenv:
        print(r"你可以手动执行命令 “.\venv\Scripts\pip install -r .\package\requirements.txt” 安装第三方库")
    else:
        print(r"你可以手动执行命令 “pip install -r .\package\requirements.txt” 安装第三方库")
    print("下面尝试自动安装第三方库")
    input("如需自动安装按回车键继续（如不需要可现在关闭程序）...\n")
    from pip._internal import main
    main(["install", "-r", "./package/requirements.txt", "-i", "https://mirrors.aliyun.com/pypi/simple/"])
    print("\n第三方库安装成功，请重新运行程序")
    input("按回车键退出程序......")
    exit(0)
