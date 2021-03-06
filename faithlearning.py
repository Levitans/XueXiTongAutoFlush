# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 23:26
# @Author : Levitan
# @File : faithlearning.py
# @Software : PyCharm
import shutil
import sys
import traceback

"""
运行前自检
检测依赖是否存在和全局变量是否正确读入
"""
from package.learn import boot
try:
    boot.python_version_detect()
    boot.isDependencyReady()
    boot.initGlobalVar()
except Exception as e:
    print("自检时出现异常：")
    err_info = traceback.format_exc()
    print("异常详细信息：\n"+err_info)


from package.learn import color
from package.learn import globalvar as gl
from package.learn import learn_helper
from package.learn.display import Display, MyFormat
from package.learn.userinterface import login_of_acc_and_pwd, login_of_QRCoed, login_of_history, add_new_user, \
    change_user_data, delete_historical, system_settings, find_answers

def start_learn():
    if gl.no_head:
        print(color.blue("选择模式") + "（" + "当前浏览器为 " + color.read("关闭显示") + "）：")
    else:
        print(color.blue("选择模式") + "（" + "当前浏览器为 " + color.read("开启显示") + "）：")
    Display.printTable(["开始学习", "查找答案", "用户设置", "系统设置"], MyFormat([17, 17, 17, 17], displayNumber=True))
    key = input("\n输入序号：")
    Display.separate()
    if key == "1":
        print(color.blue("选择登陆方式："))
        Display.printTable(["账号密码登陆", "二维码登陆", "历史登陆"], MyFormat([17, 17, 17], displayNumber=True))
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
        Display.printTable(["学习", "作业（还未完善，暂时不要使用）"], MyFormat([17, 17], displayNumber=True))
        key = input("\n输入序号：")
        Display.separate()
        try:
            if key == "1":
                learn_helper.automatic_learning(driver)
            elif key == "2":
                learn_helper.do_homework(driver)
            else:
                raise Exception("序号输入错误")
        except Exception as e:
            # input("出现异常程序已经暂停"+traceback.format_exc())
            driver.quit()
            print(color.read("程序运行出现异常"))
            print(color.read(str(e)))
            err_info = traceback.format_exc()
            gl.exception_log_manger.writeLog(err_info)
    elif key == "2":
        find_answers()
    elif key == "3":
        print(color.blue("选择设置："))
        Display.printTable(["创建新用户", "修改用户信息", "删除所有历史登陆信息"], MyFormat([17, 17, 17], displayNumber=True))
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
    elif key == "4":
        system_settings()


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
    start_learn()
