# -*- encoding = utf-8 -*-
# @Time : 2021-10-31 0:04
# @Author : Levitan
# @File : main.py
# @Software : PyCharm


import os
import sys
import json
import time
from package.user import User
from package.display import Display
from package.progress import Progress
from package.manageDate import UserData
from package.manageDate import SubjectData
from package.manageDate import BrowserConfiguration
from package.internetTime import InternetTime
from package.ControlWeb.xueXiTong import XueXiTong
from colorama import Fore, Back, init
init(autoreset=True)        # 设置颜色自动恢复

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


# 地址初始化
nowPath = os.getcwd()
driverPath = "{}\\driver\\chrome\\chromedriver.exe".format(nowPath)
chromePath = "{}\\driver\\chrome\\chrome.exe".format(nowPath)
userDataPath = "{}\\data\\user_data.json".format(nowPath)
subjectDataPath = "{}\\data\\subject_data.json".format(nowPath)
browserConfigurationPath = "{}\\data\\browser_configuration.json".format(nowPath)

userData = UserData(userDataPath)
browser = BrowserConfiguration(browserConfigurationPath)

Display.setFormat(((15, 25), (15, 25)))
Display.overLengthOfEn = 15

# while True and InternetTime.isExpiration():
while True:
    if browser.getState() == 1:
        Display.printWarning("当前为不显示浏览器运行\n不显示浏览器程序可能会出错")
    browserInf = "关闭显示" if browser.getState() == 1 else "开启显示"
    print("选择模式（{}".format(Fore.YELLOW+"当前浏览器模式：" + browserInf), end="）\n")
    function = "1、创建新用户，" \
               "2、使用已有用户（当前已有{}个用户），" \
               "3、修改用户信息，" \
               "4、设置浏览器显示，" \
               "5、退出程序\n输入序号：".format(userData.getUserAmount())
    mode = input(function)
    Display.separate()

    def star():
        """
        作用：选择登陆用户，进入学习通展示所有课程
        :return:
            user: 选择的登陆用户数据的user对象
            XueXiTong: XueXiTong对象
            coursesList: 课程名称列表
        """
        userData.displayUserName()
        index = int(input("选择用户：")) - 1
        Display.separate()
        userdata = userData.getUsers()[index]

        progress = Progress()
        progress.start()

        xueXiTong = XueXiTong(chromePath, driverPath, userdata, browser.getState())
        xueXiTong.landing()
        # 获取课程列表
        try:
            coursesList = xueXiTong.getCourses()
        except Exception as e:
            progress.key = False  # 关闭进度条
            progress.join()  # 等待进度条关闭
            print("Login failure")
            Display.separate()
            Display.printWarning(e.__str__())
            sys.exit()

        progress.key = False        # 关闭进度条
        progress.join()             # 等待进度条关闭

        print("Login success")
        Display.separate()
        time.sleep(1)

        # 展示课程
        if len(coursesList) % 2 == 0:
            listLen = len(coursesList)
        else:
            listLen = len(coursesList) + 1
            coursesList.append("")
        for i in range(0, listLen, 2):
            Display.printTable([coursesList[i], coursesList[i + 1]], numberKey=True)
        return userdata, xueXiTong, coursesList


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
        user, xueXiTong, coursesList = star()
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
        xueXiTong.automaticLearning(chapterIndex, subjectData)
    elif mode == "3":  # 修改用户信息
        userData.displayUserName()
        userIndex = int(input("选择需要修改的用户：")) - 1
        Display.separate()
        user = userData.getUsers()[userIndex]
        print("{}的数据：".format(user.getUserName()))
        print("\t账号："+str(user.getUserAccount()))
        print("\t密码："+str(user.getUserPassword())+"\n")
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
            browser.modifyClassData(1)
            print(Fore.RED+"已关闭显示浏览器")
        elif key == "2":
            browser.modifyClassData(0)
            print(Fore.RED+"已开启显示浏览器")
        else:
            print("输入错误\n")
        Display.separate()
    elif mode == "5":  # 爬取题目（暂时隐藏）
        user, xueXiTong, coursesList = star()
        courseIndex = int(input("输入课程号：")) - 1
        # 进入指定课程
        # 返回课程中的章节的列表
        chaptersList = xueXiTong.enterCourse(courseIndex)
        xueXiTong.crawlData()
    else:
        break
if not InternetTime.isExpiration():
    Display.printWarning("程序以过期")
os.system('pause')
