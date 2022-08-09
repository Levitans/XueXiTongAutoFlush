# -*- encoding = utf-8 -*-
# @Time : 2022-04-16 15:49
# @Author : Levitan
# @File : userinterface.py
# @Software : PyCharm

from package.learn import globalvar as gl
from package.learn.driver.mydriver import MyDriver
from package.learn.task.quiz.getanswer import GetAnswer

from package.learn.data_management.datamanger import ConfigManger, UserManger, CookiesManger

from package.learn.printer import color
from package.learn.printer.factory import getPrinterBySetter
from package.learn.printer.setter import TableSetter, MsgSetter

mySetter = TableSetter()
mySetter.hasHead = True
mySetter.autoOrdNumber = True
mySetter.headColor = "green"
mySetter.abreastTableNumber = 2
tablePrinter = getPrinterBySetter(mySetter)

user_manager = UserManger(gl.user_file_path)
cookie_manager = CookiesManger(gl.cookie_file_path)

# --------------------------各种登陆交互----------------------------
def select_Login_UI():
    username_list = user_manager.getUsersName()
    print(color.yellow("         当前系统中的用户如下表\n"))
    print(color.blue("选择登陆用户："))
    printList = [["用户名"]]
    printList += [[_] for _ in username_list]
    tablePrinter.print(printList)
    print()
    index = int(input("选择用户：")) - 1
    username = username_list[index]
    gl.spliter.print()

    print("正在登陆...")
    driver = MyDriver(
        gl.browser_path,
        gl.driver_path,
        gl.no_img,
        gl.no_head
    )
    # 查看本地是否储存所选用户的 cookies
    # 如果存在则用 cookies 登陆，如果不存在则用账号密码登陆，登陆成功后保存 cookies
    if cookie_manager.isUserExist(username):
        driver.login_with_cookies(cookie_manager.getCookies(username))
    else:
        userData = user_manager.getUserData(username)
        cookies = driver.login_with_acc_and_pwd(userData["account"], userData["password"])
        cookie_manager.setCookies(username, cookies)
    return driver


def login_of_QRCoed():
    driver = MyDriver(
        gl.browser_path,
        gl.driver_path,
        gl.no_img,
        noHead=False
    )
    print("正在打开二维码登陆界面，请稍后...")
    username, cookies = driver.login_with_QRCode()
    print("请扫描浏览器上的二维码")
    cookie_manager.setCookies(username, cookies)
    print("登陆成功")
    driver.quit()
    if gl.no_head:
        print("请稍后")
        driver = MyDriver(
            gl.browser_path,
            gl.driver_path,
            gl.no_img,
            gl.no_head
        )
        driver.login_with_cookies(cookie_manager.getCookies(username))
    return driver


def login_of_history():
    print(color.yellow("=================================================="))
    print(color.yellow("|          历史登陆中的信息有存活期限            |"))
    print(color.yellow("|         程序会自动删除过期的登陆数据           |"))
    print(color.yellow("| 若没有你的登陆信息请重新扫码登陆或账号密码登陆 |"))
    print(color.yellow("=================================================="))

    print(color.blue("选择登陆用户："))
    name_list = cookie_manager.getNameList()
    printList = [["名称"]]
    printList += [[_] for _ in name_list]
    tablePrinter.print(printList)
    print()
    index = int(input("选择用户：")) - 1
    name = name_list[index]
    gl.spliter.print()
    print("正在登陆...")
    driver = MyDriver(
        gl.browser_path,
        gl.driver_path,
        gl.no_img,
        gl.no_head
    )
    driver.login_with_cookies(cookie_manager.getCookies(name))
    print("登陆成功")
    return driver


# -----------------------答案查找页面---------------------------------
def find_answers():
    msgSetter = MsgSetter()
    msgSetter.color = "yellow"
    msgPrinter = getPrinterBySetter(msgSetter)
    msgPrinter.print("\n     注意！查找答案的频率不要过高\n频率过高会被接口判定为爬虫，有被封ip风险\n")
    print()
    getAnswer = GetAnswer()
    while True:
        q = input(color.blue("输入题目（q退出）："))
        if q == "q" or q == "Q":
            break
        answerList = getAnswer.getAnswer(q)
        if len(answerList) == 0:
            print(color.yellow("没有找到这题的答案"))
        gl.spliter.print()


# ---------------------各种用户设置交互--------------------------------
def add_new_user():
    userName = input("输入用户名：")
    if userName in user_manager.getUsersName():
        print("用户名已存在！！")
        return
    else:
        account = input("输入手机号：")
        password = input("输入密码：")
        user_manager.addNewUser(userName, account, password)
        print("用户添加成功")


def change_user_data():
    username_list = user_manager.getUsersName()
    print(color.blue("当前系统中的用户有："))
    printDataList = [["用户名"]]
    printDataList += [[_] for _ in username_list]
    tablePrinter.print(printDataList)
    index = int(input("\n选择需要修改的用户：")) - 1
    gl.spliter.print()
    username = username_list[index]
    userdata = user_manager.getUserData(username)
    print("{}的数据：".format(username))
    print("\t账号：" + userdata["account"])
    print("\t密码：" + userdata["password"] + "\n")
    tablePrinter.print([["选项"], ["修改账号"], ["修改密码"], ["删除账号"]])
    key = input("\n选择修改信息：")
    gl.spliter.print()
    if key == "1":
        newData = input("输入新账号：")
        user_manager.modifyUserData(username, newData, "pwd")
    elif key == "2":
        newData = input("输入新密码：")
        user_manager.modifyUserData(username, newData)
    elif key == "3":
        user_manager.modifyUserData(username, "", "del")
    else:
        raise Exception("输入序号错误！！！")
    print("信息修改成功")


def delete_historical():
    cookie_manager.removeAll()
    print("历史记录删除成功")


# ----------------------------系统设置交互--------------------------------
def system_settings():
    cfgManger = ConfigManger()
    print(color.blue("选择设置："))
    tablePrinter.print([["选项"], ["浏览器显示"], ["浏览器声音"]])
    key = input("\n输入序号：")
    gl.spliter.print()
    if key == "1":
        info = color.blue("关") if gl.no_head else color.blue("开")
        print("\t当前浏览器显示为：" + info)
        print(color.blue("选择设置选项："))
        tablePrinter.print([["选项"], ["开启显示"], ["关闭显示"]])
        key = input("\n输入序号：")
        gl.spliter.print()
        if key == "1":
            cfgManger.change_cfg("browser_config", "no_head", "False")
        elif key == "2":
            cfgManger.change_cfg("browser_config", "no_head", "True")
        else:
            raise Exception("输入序号错误！！！")

    elif key == "2":
        info = color.blue("关") if gl.mute else color.blue("开")
        print("\t当前浏览器声音为：" + info)
        print(color.blue("选择设置选项："))
        tablePrinter.print([["选项"], ["开启声音"], ["关闭声音"]])
        key = input("\n输入序号：")
        gl.spliter.print()
        if key == "1":
            cfgManger.change_cfg("browser_config", "mute_audion", "False")
        elif key == "2":
            cfgManger.change_cfg("browser_config", "mute_audion", "True")
        else:
            raise Exception("输入序号错误！！！")
    else:
        raise Exception("输入序号错误！！！")
    print("设置修改成功")
