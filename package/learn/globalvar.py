# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 18:52
# @Author : Levitan
# @File : globalvar.py.py
# @Software : PyCharm

from package.learn import color
from package.learn.exception import InitializationException
from package.learn.datamanger import UserManger, CookiesManger
from package.learn.config import cfg_get
from package.learn import file

# 全局变量是否初始化
is_init = False

# 用户配置
user_manager: UserManger
cookie_manager: CookiesManger

# 浏览器配置
no_head = False
mute = False
no_img = False
browser_path = ""
driver_path = ""

def init_global():
    global is_init, no_head, mute, no_img, browser_path, driver_path, user_manager, cookie_manager
    try:
        # <--------------------加载浏览器配置------------------------->
        if cfg_get("browser_config", "no_head") == "True":
            no_head = True
        if cfg_get("browser_config", "mute_audion") == "True":
            mute = True
        if cfg_get("browser_config", "no_img") == "True":
            no_img = True
        browser_path = file.is_file_exists(cfg_get("browser_config", "browser_path"))
        if browser_path == "":
            raise Exception("浏览器路径错误，请检查路径 "+color.read(cfg_get("browser_config", "browser_path"))+" 的正确性")
        driver_path = file.is_file_exists(cfg_get("browser_config", "driver_path"))
        if driver_path == "":
            raise Exception("驱动路径错误，请检查路径 "+color.read(cfg_get("browser_config", "driver_path"))+" 的正确性")

        # <------------------------加载数据管理器----------------------->
        user_manager = UserManger(cfg_get("user_config", "user_path"))
        cookie_manager = CookiesManger(cfg_get("user_config", "cookie_path"))
    except Exception as e:
        raise InitializationException(str(e))
