# -*- encoding = utf-8 -*-
# @Time : 2021-10-31 0:04
# @Author : Levitan
# @File : main.py
# @Software : PyCharm


import os
import sys
import json
import time
import ctypes
from package.user import User
from package.display import Display
from package.progress import Progress
from package.manageDate import UserData, SubjectData, BrowserShow, BrowserConfiguration
from package.internetTime import InternetTime
from package.ControlWeb.xueXiTong import XueXiTong
from package.ControlWeb.Spider.spider import Spider
from colorama import Fore, Back, init

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


# 禁用快速编辑
def disableQuickEdit():
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)


# 地址初始化
nowPath = os.getcwd()
userDataPath = "{}\\data\\user_data.json".format(nowPath)
subjectDataPath = "{}\\data\\subject_data.json".format(nowPath)
browserShowPath = "{}\\data\\browser_show.json".format(nowPath)
browserConfigurationPath = "{}\\data\\browser_configuration.json".format(nowPath)
spiderDataPath = "{}\\spiderData".format(nowPath)

browserPath = ""
driverPath = ""
# 获取浏览器和浏览器驱动的地址
try:
    browserConfiguration = BrowserConfiguration(browserConfigurationPath)
    browserPath = browserConfiguration.getBrowserPath()  # 浏览器位置
    driverPath = browserConfiguration.getDriverPath()  # 驱动位置
except Exception as e:
    Display.printWarning(e.__str__())
    os.system('pause')


userData = UserData(userDataPath)
browserShow = BrowserShow(browserShowPath)

Display.setFormat(50, 50)
Display.overLengthOfEn = 15

# while True and InternetTime.isExpiration():
while True:
    if browserShow.getState() == 1:
        Display.printWarning("当前为不显示浏览器运行\n不显示浏览器程序可能会出错")
    browserInf = "关闭显示" if browserShow.getState() == 1 else "开启显示"
    print("选择模式（{}".format(Fore.YELLOW + "当前浏览器模式：" + browserInf), end="）\n")
    function = "1、创建新用户，" \
               "2、使用已有用户（当前已有{}个用户），" \
               "3、修改用户信息，" \
               "4、设置浏览器显示，" \
               "5、退出程序\n输入序号：".format(userData.getUserAmount())
    mode = input(function)
    Display.separate()

    while not (mode in ("1", "2", "3", "4", "5", "6")):
        print("输入错误，重新选择")
        mode = input(function)
        Display.separate()

    if mode == "1":  # 创建新用户
        userName = input("输入用户名：")
        account = input("输入手机号：")
        password = input("输入密码：")
        userData.addNewUser(userName, account, password)
        userData = UserData(userDataPath)
        print("用户添加成功\n")
        Display.separate()
    elif mode == "2":  # 使用已有用户登陆
        # 选择登录用户
        userData.displayUserName()
        index = int(input("选择用户：")) - 1
        Display.separate()
        user = userData.getUsers()[index]

        # 显示进度条
        progress = Progress()
        progress.start()

        xueXiTong = XueXiTong(browserPath, driverPath, user, browserShow.getState())
        try:
            xueXiTong.logging()
        except Exception as e:
            progress.key = False  # 关闭进度条
            progress.join()  # 等待进度条关闭
            print("Login failure")
            Display.separate()
            Display.printWarning(e.__str__())
            xueXiTong.closeDriver()
            sys.exit()
        # 获取课程列表
        coursesList = xueXiTong.getCourses()
        progress.key = False  # 关闭进度条
        progress.join()  # 等待进度条关闭

        print("Login success")
        Display.separate()
        time.sleep(1)

        # 展示课程
        Display.printTable(coursesList, displayNumber=True)
        courseIndex = int(input("输入课程号：")) - 1
        Display.separate()
        # 进入指定课程
        # 返回课程中的章节的列表
        chaptersList = xueXiTong.enterCourse(courseIndex)
        # 实例化subjectData对象
        subjectData = SubjectData(subjectDataPath)
        # 查找本地储存的课程进度
        subjectProgress = subjectData.getSubjectProcess(user.getUserName(), coursesList[courseIndex])
        print("{}本地进度为{}".format(coursesList[courseIndex], subjectProgress))
        chapterIndex = 0
        try:
            chapterIndex = chaptersList.index(subjectProgress)
        except ValueError as e:
            Display.separate()
            print("当前课程没有{}章节。".format(subjectProgress))
            print("可以到{}\\data\\subject_data.json中修改课程进度。".format(nowPath))
            Display.separate()
            break
        xueXiTong.work(chapterIndex, subjectData)
    elif mode == "3":  # 修改用户信息
        userData.displayUserName()
        userIndex = int(input("选择需要修改的用户：")) - 1
        Display.separate()
        user = userData.getUsers()[userIndex]
        print("{}的数据：".format(user.getUserName()))
        print("\t账号：" + str(user.getUserAccount()))
        print("\t密码：" + str(user.getUserPassword()) + "\n")
        print("1、修改账号\n2、修改密码")
        key = input("选择修改信息：")
        if key == "1":
            newAccount = input("输入新数据：")
            userData.modifyUserData(user.getUserName(), newAccount, "account")
        elif key == "2":
            newPassword = input("输入新数据：")
            userData.modifyUserData(user.getUserName(), newPassword)
        else:
            Display.printWarning("输入信息有误")
        Display.separate()
    elif mode == "4":  # 设置浏览器显示模式
        key = input("1、关闭浏览器显示，2、开启浏览器显示\n输入序号：")
        if key == "1":
            browserShow.modifyClassData(1)
            print(Fore.RED + "已关闭显示浏览器")
        elif key == "2":
            browserShow.modifyClassData(0)
            print(Fore.RED + "已开启显示浏览器")
        else:
            print("输入错误\n")
        Display.separate()
    elif mode == "5":  # 爬取题目（暂时隐藏）
        if not os.path.exists(spiderDataPath):  # 判断spiderData文件夹是否存在
            os.mkdir(spiderDataPath)
        userData.displayUserName()
        index = int(input("选择用户：")) - 1
        Display.separate()
        userdata = userData.getUsers()[index]

        progress = Progress()
        progress.start()

        spider = Spider(browserPath, driverPath, userdata, browserShow.getState(), spiderDataPath)
        spider.logging()
        # 获取课程列表
        try:
            coursesList = spider.getCourses()
        except Exception as e:
            progress.key = False  # 关闭进度条
            progress.join()  # 等待进度条关闭
            print("Login failure")
            Display.separate()
            Display.printWarning(e.__str__())
            spider.closeDriver()
            sys.exit()

        progress.key = False  # 关闭进度条
        progress.join()  # 等待进度条关闭

        print("Login success")
        Display.separate()
        time.sleep(1)

        # 展示课程
        Display.printTable(coursesList, displayNumber=True)
        courseIndex = int(input("输入课程号：")) - 1
        Display.separate()
        # 进入指定课程
        # 返回课程中的章节的列表
        chaptersList = spider.enterCourse(courseIndex)
        spider.work(None, None)
        print("题目爬取完成")

    else:
        break
if not InternetTime.isExpiration():
    Display.printWarning("程序以过期")
os.system('pause')
