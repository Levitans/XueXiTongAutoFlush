# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 18:52
# @Author : Levitan
# @File : globalvar.py.py
# @Software : PyCharm

from package.learn import color
from package.learn.exception import InitializationException
from package.learn.datamanger import UserManger, CookiesManger, ExceptionLogManger
from package.learn.config import cfg_get
from package.learn import file

# 全局变量是否初始化
is_init = False

# 用户配置
user_manager: UserManger
cookie_manager: CookiesManger

# 异常日志管理器
exception_log_manger: ExceptionLogManger

# 浏览器配置
no_head = False
mute = False
no_img = False
browser_path = ""
driver_path = ""

# 任务点配置
ppt_speed_max: int
ppt_speed_min: int
quiz_get_answer_speed_max: int
quiz_get_answer_speed_min: int
quiz_click_speed_max: int
quiz_click_speed_min: int

# 其他配置
version_file_path = ""

def init_global():
    """
    在配置文件中加载配置
    """
    global is_init, no_head, mute, no_img, browser_path, driver_path, user_manager, cookie_manager, \
        ppt_speed_max, ppt_speed_min, quiz_get_answer_speed_max, quiz_get_answer_speed_min, quiz_click_speed_max, quiz_click_speed_min, \
        exception_log_manger, version_file_path

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
        exception_log_manger = ExceptionLogManger(cfg_get("other", "exception_log_file_path"))

        # <------------------------加载任务点配置----------------------->
        ppt_speed_max = int(cfg_get("task_config", "ppt_speed_max"))
        ppt_speed_min = int(cfg_get("task_config", "ppt_speed_min"))
        quiz_get_answer_speed_max = int(cfg_get("task_config", "quiz_get_answer_speed_max"))
        quiz_get_answer_speed_min = int(cfg_get("task_config", "quiz_get_answer_speed_min"))
        quiz_click_speed_max = int(cfg_get("task_config", "quiz_click_speed_max"))
        quiz_click_speed_min = int(cfg_get("task_config", "quiz_click_speed_min"))

        # <------------------------加载其他点配置----------------------->
        version_file_path = cfg_get("other", "version_file_path")

        # 所有配置加载成功
        is_init = True
    except Exception as e:
        raise InitializationException(str(e))
