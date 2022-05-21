# -*- encoding = utf-8 -*-
# @Time : 2022-04-16 15:49
# @Author : Levitan
# @File : userinterface.py
# @Software : PyCharm

from package.learn import config
from package.learn import color
from package.learn import globalvar as gl
from package.learn.mydriver import MyDriver
from package.learn.display import Display, MyFormat
from package.learn.task.quiz.getanswer import GetAnswer


# --------------------------各种登陆交互----------------------------
def login_of_acc_and_pwd():
    username_list = gl.user_manager.getUsersName()
    print(color.blue("当前系统中的用户有："))
    Display.printTable(username_list, MyFormat([20], displayNumber=True))
    print()
    index = int(input("选择用户：")) - 1
    username = username_list[index]
    Display.separate()

    print("正在登陆...")
    driver = MyDriver()
    cookies = gl.cookie_manager.getCookies(username)
    if len(cookies) == 0:
        driver.login_with_acc_and_pwd(username)
    else:
        driver.login_with_cookies(username)
    return driver


def login_of_QRCoed():
    driver = MyDriver(noHead=False)
    print("正在打开二维码登陆界面，请稍后...")
    username = driver.login_with_QRCode()
    print("登陆成功")
    if gl.no_head:
        print("请稍后")
        driver.quit()
        driver = MyDriver()
        driver.login_with_cookies(username)
    return driver


def login_of_history():
    print(color.yellow("          历史登陆中的信息有存活期限        "))
    print(color.yellow("  若没有你的登陆信息请重新扫码登陆或账号密码登陆"))
    Display.separate()
    name_list = gl.cookie_manager.getNameList()
    Display.printTable(name_list, MyFormat([20], displayNumber=True))
    print()
    index = int(input("选择用户：")) - 1
    name = name_list[index]
    Display.separate()
    driver = MyDriver()
    driver.login_with_cookies(name)
    return driver


# -----------------------答案查找页面---------------------------------
def find_answers():
    print(color.yellow("注意！查找答案的频率不要过高"))
    print(color.yellow("频率过高会被接口判断为爬虫，有被封ip风险"))
    getAnswer = GetAnswer()
    while True:
        q = input("输入题目（q退出）：")
        if q == "q":
            break
        answerList = getAnswer.getAnswer(q)
        if len(answerList) == 0:
            print(color.yellow("没有找到这题的答案"))
        Display.separate(10)


# ---------------------各种用户设置交互--------------------------------
def add_new_user():
    userName = input("输入用户名：")
    if userName in gl.user_manager.getUsersName():
        print("用户名已存在！！")
        return
    else:
        account = input("输入手机号：")
        password = input("输入密码：")
        gl.user_manager.addNewUser(userName, account, password)
        print("用户添加成功")


def change_user_data():
    username_list = gl.user_manager.getUsersName()
    print(color.blue("当前系统中的用户有："))
    Display.printTable(username_list, MyFormat([20], displayNumber=True))
    index = int(input("\n选择需要修改的用户：")) - 1
    Display.separate()
    username = username_list[index]
    userdata = gl.user_manager.getUserData(username)
    print("{}的数据：".format(username))
    print("\t账号：" + userdata["account"])
    print("\t密码：" + userdata["password"] + "\n")
    Display.printTable(["修改账号", "修改密码", "删除账号"], MyFormat([20, 20, 20], displayNumber=True))
    key = input("\n选择修改信息：")
    Display.separate()
    if key == "1":
        newData = input("输入新账号：")
        gl.user_manager.modifyUserData(username, newData, "pwd")
    elif key == "2":
        newData = input("输入新密码：")
        gl.user_manager.modifyUserData(username, newData)
    elif key == "3":
        gl.user_manager.modifyUserData(username, "", "del")
    else:
        raise Exception("输入序号错误！！！")
    print("信息修改成功")


def delete_historical():
    gl.cookie_manager.removeAll()
    print("历史记录删除成功")


# ----------------------------系统设置交互--------------------------------
def system_settings():
    Display.printTable(["浏览器显示", "浏览器声音"], MyFormat([20, 20], displayNumber=True))
    key = input("\n输入序号：")
    Display.separate()
    if key == "1":
        info = color.blue("关") if gl.no_head else color.blue("开")
        print("\t当前浏览器显示为：" + info)
        Display.printTable(["开启显示", "关闭显示"], MyFormat([20, 20], displayNumber=True))
        key = input("\n输入序号：")
        Display.separate()
        if key == "1":
            config.change_cfg_data("browser_config", "no_head", "False")
        elif key == "2":
            config.change_cfg_data("browser_config", "no_head", "True")
        else:
            raise Exception("输入序号错误！！！")

    elif key == "2":
        info = color.blue("关") if gl.mute else color.blue("开")
        print("\t当前浏览器声音为：" + info)
        Display.printTable(["开启声音", "关闭声音"], MyFormat([20, 20], displayNumber=True))
        key = input("\n输入序号：")
        Display.separate()
        if key == "1":
            config.change_cfg_data("browser_config", "mute_audion", "False")
        elif key == "2":
            config.change_cfg_data("browser_config", "mute_audion", "True")
        else:
            raise Exception("输入序号错误！！！")
    else:
        raise Exception("输入序号错误！！！")
    print("设置修改成功")
