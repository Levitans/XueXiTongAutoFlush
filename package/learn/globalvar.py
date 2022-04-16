# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 18:52
# @Author : Levitan
# @File : globalvar.py.py
# @Software : PyCharm

from package.learn.datamanger import UserManger, CookiesManger
from package.learn.config import cfg_get

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
    # <--------------------加载浏览器配置------------------------->
    if cfg_get("browser_config", "no_head") == "True":
        no_head = True
    if cfg_get("browser_config", "mute_audion") == "True":
        mute = True
    if cfg_get("browser_config", "no_img") == "True":
        no_img = True
    browser_path = cfg_get("browser_config", "browser_path")
    driver_path = cfg_get("browser_config", "driver_path")

    # <------------------------加载数据管理器----------------------->
    user_manager = UserManger(cfg_get("user_config", "user_path"))
    cookie_manager = CookiesManger(cfg_get("user_config", "cookie_path"))
