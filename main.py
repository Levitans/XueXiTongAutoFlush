# -*- encoding = utf-8 -*-
# @Time : 2021-10-31 0:04
# @Author : Levitan
# @File : main.py
# @Software : PyCharm


import os
import sys
import json
from package.user import User
from package.ControlWeb.xueXiTong import XueXiTong
from package.display import Display
from package.manageDate import UserData
from package.manageDate import SubjectData
from package.manageDate import BrowserConfiguration
from package.internetTime import InternetTime

starInformation = """
===========================================
作者：Levitan
本项目已在GitHub上开源
GitHub地址：https://github.com/Levitans/-
===========================================
"""
print(starInformation)

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

Display.setFormat(((15, 10, True), (15, 10, True)))
Display.overLengthOfEn = 15

# while True and InternetTime.isExpiration():
while True:
    if browser.getState() == 1:
        print("当前为不显示浏览器运行\n不显示浏览器程序可能会出错")
    browserInf = "关闭显示" if browser.getState() == 1 else "开启显示"
    print("选择模式（{}）".format("当前浏览器模式："+browserInf))
    function = "1、创建新用户，"\
               "2、使用已有用户（当前已有{}个用户），" \
               "3、修改用户信息，"\
               "4、设置浏览器显示，"\
               "5、退出程序\n输入序号：".format(userData.getUserAmount())
    mode = input(function)
    print()

    while not (mode in ("1", "2", "3", "4", "5", "6")):
        print("输入错误，重新选择")
        mode = input(function)
        print()

    if mode == "1":                     # 创建新用户
        userName = input("输入用户名：")
        account = input("输入手机号：")
        password = input("输入密码：")
        userData.addNewUser(userName, account, password)
        userData = UserData(userDataPath)
        print("用户添加成功\n")
    elif mode == "2":                   # 使用已有用户登陆
        for j, i in enumerate(userData.getUsers()):
            print(str(j+1)+"、"+i.getUserName())
        userIndex = int(input("选择用户：")) - 1
        Display.separate()
        user = userData.getUsers()[userIndex]
        xueXiTong = XueXiTong(chromePath, driverPath, user, browser.getState())
        xueXiTong.landing()
        # 获取课程列表
        coursesList = xueXiTong.getCourses()
        # 展示课程
        listLen = len(coursesList) if len(coursesList) % 2 == 0 else len(coursesList) + 1
        for i in range(0, listLen, 2):
            Display.printTable([coursesList[i], coursesList[i+1]])
        courseIndex = int(input("输入课程号：")) - 1

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
    elif mode == "3":                   # 修改用户信息
        for j, i in enumerate(userData.getUsers()):
            print(str(j+1)+"、"+i.getUserName())
        userIndex = int(input("选择需要修改的用户：")) - 1
        print()
        user = userData.getUsers()[userIndex]
        print("1、修改账号\n2、修改密码")
        key = input("选择修改信息：")
        newData = input("输入新数据：")
        if key == "1":
            userData.modifyUserData(user.getUserName(), newData, "account")
        elif key == 2:
            userData.modifyUserData(user.getUserName(), newData)
    elif mode == "4":                   # 设置浏览器显示模式
        key = input("1、关闭浏览器显示，2、开启浏览器显示\n输入序号：")
        if key == "1":
            browser.modifyClassData(1)
            print("已关闭显示浏览器\n")
        elif key == "2":
            browser.modifyClassData(0)
            print("已开启显示浏览器\n")
        else:
            print("输入错误\n")
    elif mode == "5":                   # 爬取题目（暂时隐藏）
        for j, i in enumerate(userData.getUsers()):
            print(str(j + 1) + "、" + i.getUserName())
        userIndex = int(input("选择用户：")) - 1
        Display.separate()
        user = userData.getUsers()[userIndex]
        xueXiTong = XueXiTong(chromePath, driverPath, user, browser.getState())
        xueXiTong.landing()
        # 获取课程列表
        coursesList = xueXiTong.getCourses()
        # 展示课程
        listLen = len(coursesList) if len(coursesList) % 2 == 0 else len(coursesList) + 1
        for i in range(0, listLen, 2):
            Display.printTable([coursesList[i], coursesList[i+1]])
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

