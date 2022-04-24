# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 19:53
# @Author : Levitan
# @File : file.py
# @Software : PyCharm
import os
import configparser
import json
from package.learn import color


def get_config_file(filename) -> configparser.ConfigParser:
    conf_obj = configparser.ConfigParser()
    try:
        conf_obj.read(filename, encoding="utf-8")
    except Exception as e:
        print(color.read(filename+"解析错误："+str(e)))
        print(color.yellow("请检查"+filename+"中的信息"))
        exit()
    return conf_obj


def get_json_data(filename) -> dict:
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            try:
                json_data = json.load(f)
            except Exception as e:
                err_info = color.read("文件 "+filename + " 解析错误：" + str(e))+"\n"+\
                           color.yellow("请检查 " + filename + " 中的信息")
                raise Exception(err_info)
        return json_data
    except FileNotFoundError:
        raise Exception(color.read("文件 "+filename+" 未找到"))


def save_json_data(filename, dictData):
    with open(filename, "w", encoding="utf-8") as f:
        data = json.dumps(dictData, indent=4, ensure_ascii=False)
        f.write(data)


def save_text_file(filename, text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def append_text_file(filename, text):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text)


def is_file_exists(filename):
    return filename if os.path.exists(filename) else ""
