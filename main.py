# -*- encoding = utf-8 -*-
# @Time : 2021-10-31 0:04
# @Author : Levitan
# @File : main.py
# @Software : PyCharm

import os
import sys
import json
import time
import configparser

from package.user import User
from package.display import Display, Format
from package.progressbar import ProgressBar, ProgressBar2
from package.dataManger import UserDataManger, BrowserShow, BrowserConfiguration
from package.internetTime import InternetTime
from package.ControlWeb.xueXiTong import XueXiTong
from package.ControlWeb.Spider.spider import Spider
from colorama import Fore, Back, init
from package.exception import AtOrPdException, BrowseOrDriverPathException

init(autoreset=True)  # 设置颜色自动恢复

starInformation = """
============================================================
·作者：Levitan
·本项目已在GitHub上开源
·GitHub地址：https://github.com/Levitans/XueXiTongBrushClass
============================================================
"""

print(Fore.MAGENTA + starInformation)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


browserPath = ""
driverPath = ""
browserName = ""
userDataPath = ""
spiderDataPath = ""
browserShow: BrowserShow = None
userManger: UserDataManger = None

# 运行前准备
def initialization():
    global browserPath, driverPath, browserName, userDataPath, spiderDataPath, browserShow, userManger
    # 地址初始化
    nowPath = os.getcwd()
    confPath = nowPath + "\\" + "config.ini"
    conf = configparser.ConfigParser()
    conf.read(confPath, encoding="utf-8")

    # 读取浏览器地址
    try:
        browserConfiguration = BrowserConfiguration(conf)
        browserPath = browserConfiguration.getBrowserPath()  # 浏览器位置
        driverPath = browserConfiguration.getDriverPath()  # 驱动位置
        browserName = browserConfiguration.gerBrowserName()  # 浏览器名称
    except Exception as e:
        Display.printWarning(e.__str__())
        os.system('pause')
        sys.exit()

    # 读取用户数数据地址
    userDataPath = "{}".format(nowPath) + conf.get("data_path", "user_data_path")
    spiderDataPath = "{}".format(nowPath) + conf.get("data_path", "spider_data_path")

    # 初始化浏浏览器显示和用户数据管理
    browserShow = BrowserShow(conf, confPath)
    userManger = UserDataManger(userDataPath)


while True:
    initialization()

    if browserShow.getState() == "1":
        Display.printWarning("若程序运行出错可尝试切换浏览器模式")
        print()
    browserInf = "关闭显示" if browserShow.getState() == "1" else "开启显示"
    print("选择模式（{}".format(Fore.YELLOW + "当前浏览器模式：" + browserInf), end="）\n")
    function = ["创建新用户",
                "使用已有用户（当前已有{}个用户）".format(userManger.getUserAmount()),
                "修改用户信息",
                "设置浏览器显示",
                "程序更新",
                "退出程序"]
    Display.printTable(function, Format([20, 20], displayNumber=True))
    mode = input("\n输入序号：")
    Display.separate()

    while not (mode in ("1", "2", "3", "4", "5", "6", "7")):
        print("输入错误，重新选择")
        mode = input(function)
        Display.separate()

    if mode == "1":  # 创建新用户
        userName = input("输入用户名：")
        if userName in userManger.getUserNameList():
            print("用户名已存在！")
        else:
            account = input("输入手机号：")
            password = input("输入密码：")
            userManger.addNewUser(userName, account, password)
            userManger = UserDataManger(userDataPath)
            print("用户添加成功")
        Display.separate()
    elif mode == "2":  # 使用已有用户登陆
        # 选择登录用户
        Display.printTable(userManger.getUserNameList(), Format([20], displayNumber=True))
        print()
        index = int(input("选择用户：")) - 1
        Display.separate()
        user = userManger.getUser(index)

        try:
            xueXiTong = XueXiTong(browserPath, driverPath, browserName, user, browserShow.getState())
        except BrowseOrDriverPathException as e:    # 捕获浏览器地址配置错误
            Display.printWarning(e.__str__())
            sys.exit()

        # 登陆学习通
        progress = ProgressBar()
        progress.start()
        try:
            xueXiTong.logging()
        except AtOrPdException as e:    # 捕获账号密码错误
            progress.join()  # 等待进度条关闭
            print("loging failure")
            Display.separate()
            Display.printWarning(e.__str__())
            xueXiTong.closeDriver()
            sys.exit()
        finally:
            progress.key = False  # 关闭进度条
            progress.join()  # 等待进度条关闭
        print("Login success")
        Display.separate()
        time.sleep(1)

        # 获取页面所有课程并展示
        coursesList = xueXiTong.getCourses()
        coursesNameList = [i.name for i in coursesList]
        Display.printTable(coursesNameList, Format([50, 50], displayNumber=True))

        # 选择课程
        courseIndex = int(input("输入课程号：")) - 1
        Display.separate()

        # 进入指定课程
        print("正在进入课程")
        try:
            chaptersList = xueXiTong.enterCourse(coursesList[courseIndex])
        except Exception as e:
            Display.printWarning(e.__str__())
            xueXiTong.closeDriver()
            sys.exit()
        print("进入课程成功")
        Display.separate()
        time.sleep(0.5)
        xueXiTong.work()
        Display.separate()
    elif mode == "3":  # 修改用户信息
        Display.printTable(userManger.getUserNameList(), Format([20], displayNumber=True))
        index = int(input("选择需要修改的用户：")) - 1
        Display.separate()
        user = userManger.getUser(index)
        print("{}的数据：".format(user.getName()))
        print("\t账号：" + str(user.getAccount()))
        print("\t密码：" + str(user.getPassword()) + "\n")
        print("1、修改账号\n2、修改密码\n3、删除账号")
        key = input("选择修改信息：")
        if key == "1":
            newAccount = input("输入新数据：")
            userManger.modifyUserData(user.getName(), newAccount, "account")
        elif key == "2":
            newPassword = input("输入新数据：")
            userManger.modifyUserData(user.getName(), newPassword)
        elif key == "3":
            userManger.deleteUser(user)
        else:
            Display.printWarning("输入信息有误")
        Display.separate()
    elif mode == "4":  # 设置浏览器显示模式
        key = input("1、关闭浏览器显示，2、开启浏览器显示\n输入序号：")
        if key == "1":
            browserShow.modifyClassData("1")
            print(Fore.RED + "已关闭显示浏览器")
        elif key == "2":
            browserShow.modifyClassData("0")
            print(Fore.RED + "已开启显示浏览器")
        else:
            print("输入错误\n")
        Display.separate()
    elif mode == "5":
        os.system("start powershell.exe cmd /k 'bin\\updata.exe'")
        sys.exit()
    elif mode == "6":  # 爬取题目（暂时隐藏）
        if not os.path.exists(spiderDataPath):  # 判断spiderData文件夹是否存在
            os.mkdir(spiderDataPath)
        userManger.displayUserName()
        index = int(input("选择用户：")) - 1
        Display.separate()
        userdata = userManger.getUserNameList()[index]

        progress = ProgressBar()
        progress.start()

        spider = Spider(browserPath, driverPath, browserName, userdata, browserShow.getState(), spiderDataPath)
        try:
            spider.logging()
        except package.exception.atOrPdException.AtOrPdException as e:
            progress.key = False  # 关闭进度条
            progress.join()  # 等待进度条关闭
            print("Login failure")
            Display.separate()
            Display.printWarning(e.__str__())
            spider.closeDriver()
            sys.exit()
        # 获取课程列表

        coursesList = spider.getCourses()
        progress.key = False  # 关闭进度条
        progress.join()  # 等待进度条关闭

        print("Login success")
        Display.separate()
        time.sleep(1)

        # 展示课程
        Display.printTable(coursesList, Format([50, 50], displayNumber=True))
        courseIndex = int(input("输入课程号：")) - 1
        Display.separate()
        # 进入指定课程
        # 返回课程中的章节的列表
        chaptersList = spider.enterCourse(courseIndex)
        spider.work()
        print("题目爬取完成")
    else:
        break
if not InternetTime.isExpiration():
    Display.printWarning("程序以过期")
os.system('pause')
sys.exit()
