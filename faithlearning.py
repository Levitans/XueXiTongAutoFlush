# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 23:26
# @Author : Levitan
# @File : faithlearning.py
# @Software : PyCharm

try:
    import package.learn.config
    from package.learn import color
    from package.learn import learn_helper
    from package.learn import exception
    from package.learn import globalvar as gl
    from package.learn.mydriver import MyDriver
    from package.learn.display import Display, MyFormat
    from package.learn.userinterface import login_of_acc_and_pwd, login_of_QRCoed, login_of_history, add_new_user, \
        change_user_data, delete_historical, system_settings
except ModuleNotFoundError as e:
    print(color.read("依赖导入失败："+str(e)))
    print(color.read("请前往 ”使用说明.md“ 文件中查看所需依赖库"))
    exit(233)


def boot():
    try:
        gl.init_global()
    except exception.InitializationException as e:
        print(color.read("程序初始化异常"))
        print(str(e))
        exit()


boot()


def start_learn():
    if gl.no_head:
        print(color.blue("选择模式") + "（" + "当前浏览器为 " + color.read("关闭显示") + "）：")
    else:
        print(color.blue("选择模式") + "（" + "当前浏览器为 " + color.read("开启显示") + "）：")
    Display.printTable(["开始学习", "用户设置", "系统设置"], MyFormat([20, 20, 20], displayNumber=True))
    key = input("\n输入序号：")
    Display.separate()
    if key == "1":
        print(color.blue("选择登陆方式："))
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
        Display.printTable(["学习", "作业"], MyFormat([20, 20], displayNumber=True))
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
            driver.quit()
            print(color.read("程序运行出现异常"))
            print(color.read(str(e)))

    elif key == "2":
        print(color.blue("选择设置："))
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
