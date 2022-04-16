# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 23:26
# @Author : Levitan
# @File : faithlearning.py
# @Software : PyCharm

import package.learn.config
from package.learn import learn_helper
from package.learn import exception
from package.learn.mydriver import MyDriver
from package.learn import globalvar as gl
from package.learn.display import Display, MyFormat
from package.learn.userinterface import login_of_acc_and_pwd, login_of_QRCoed, login_of_history, add_new_user, change_user_data, delete_historical, system_settings
from package.learn import color


def boot():
    try:
        gl.init_global()
        gl.is_init = True
    except exception.InitializationException:
        print("程序初始化异常")


def start_learn():
    print("选择模式：")

    Display.printTable(["开始学习", "用户设置", "系统设置"], MyFormat([20, 20, 20], displayNumber=True))
    key = input("\n输入序号：")
    Display.separate()
    if key == "1":
        print("选择登陆方式：")
        Display.printTable(["账号密码登陆", "二维码登陆", "历史登陆"], MyFormat([20, 20, 20], displayNumber=True))
        key = input("\n输入序号：")
        Display.separate()
        if key == "1":
            driver = login_of_acc_and_pwd()
        elif key == "2":
            driver = login_of_QRCoed()
        elif key == "3":
            driver = login_of_history()
        else:
            raise Exception("序号输入错误")
        Display.separate()
        learn_helper.automatic_learning(driver)

    elif key == "2":
        print("选择设置：")
        Display.printTable(["创建新用户", "修改用户信息", "删除所有历史登陆信息"], MyFormat([20, 20, 20], displayNumber=True))
        key = input("\n输入序号：")
        Display.separate()
        if key == "1":
            add_new_user()
        elif key == "2":
            change_user_data()
        elif key == "3":
            delete_historical()
        else:
            raise Exception("序号输入错误")
    elif key == "3":
        system_settings()
    input("暂停")


if __name__ == '__main__':
    information = """
============================================================
·作者：Levitan
·本项目已在GitHub上开源
·GitHub地址：https://github.com/Levitans/XueXiTongAutoFlush
============================================================
"""
    print(color.magenta(information))
    print(color.green("                  LEARNING IS A BELIEF"))
    print()
    boot()
    start_learn()
