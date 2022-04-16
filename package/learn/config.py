# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 19:51
# @Author : Levitan
# @File : config.py
# @Software : PyCharm

from package.learn import file
from package.learn.exception import InitializationException

config_file_path = r".\config.ini"

config = file.get_config_file(config_file_path)


def cfg_get(section, option, default_value=None):
    try:
        return config.get(section, option)
    except Exception as e:
        print("配置文件路径："+config_file_path)
        print("读取配置失败：section="+section+", option="+option+", "+str(e))
        raise InitializationException

def change_cfg_data(section, option, value):
    config.set(section, option, value)
    config.write(open(config_file_path, "w", encoding="utf-8"))
