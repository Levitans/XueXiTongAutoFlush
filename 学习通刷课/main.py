# -*- encoding = utf-8 -*-
# @Time : 2021-10-31 0:04
# @Author : Levitan
# @File : main.py
# @Software : PyCharm

import os
import sys
from package.user import User
from package.ControlWeb.xueXiTong import XueXiTong
from package.disPlay import DisPlay
from package.manageDate import UserData
from package.manageDate import SubjectData

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


driverPath = resource_path(r"driver\chrome\chromedriver.exe")
chromePath = resource_path(r"driver\chrome\chrome.exe")

nowPath = os.getcwd()
userDataPath = "{}\\data\\user_data.json".format(nowPath)
subjectDataPath = "{}\\data\\subject_data.json".format(nowPath)


userData = UserData(userDataPath)

while True:
    print("选择模式：")
    function = "1、创建新用户，2、使用已有用户（当前已有{}个用户）" \
               "，3、修改用户信息，4、退出程序\n输入序号：".format(userData.getUserAmount())
    mode = input(function)
    print()
    while not (mode in ("1", "2", "3", "4", "5", "6")):
        print("输入错误，重新选择")
        mode = input(function)
        print()

    if mode == "1":
        userName = input("输入用户名：")
        account = input("输入手机号：")
        password = input("输入密码：")
        userData.addNewUser(userName, account, password)
        print("用户添加成功\n")
    elif mode == "2":
        for j, i in enumerate(userData.getUsers()):
            print(str(j+1)+"、"+i.getUserName())
        userIndex = int(input("选择用户：")) - 1
        print()
        user = userData.getUsers()[userIndex]
        xueXiTong = XueXiTong(chromePath, driverPath, user)
        xueXiTong.landing()
        # 获取课程列表
        coursesList = xueXiTong.getCourses()
        # 展示课程
        DisPlay.disPlay(coursesList)
        courseIndex = int(input("输入课程号：")) - 1
        # 进入指定课程
        # 返回课程中的章节的列表
        chaptersList = xueXiTong.enterCourse(courseIndex)
        # 实例化subjectData对象
        subjectData = SubjectData(subjectDataPath)
        # 查找本地储存的课程进度
        subjectProgress = subjectData.getSubjectProcess(user.getUserName(), coursesList[courseIndex])
        print("{}本地进度为{}".format(coursesList[courseIndex], subjectProgress))
        xueXiTong.work(chaptersList.index(subjectProgress), subjectData)
    elif mode == "3":
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
    else:
        break
os.system('pause')