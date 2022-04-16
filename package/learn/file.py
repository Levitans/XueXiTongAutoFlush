# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 19:53
# @Author : Levitan
# @File : file.py
# @Software : PyCharm
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
    with open(filename, 'r', encoding="utf-8") as f:
        try:
            json_data = json.load(f)
        except Exception as e:
            print(color.read(filename + "解析错误：" + str(e)))
            print(color.yellow("请检查" + filename + "中的信息"))
            exit()
    return json_data


def save_json_data(filename, dictData):
    with open(filename, "w", encoding="utf-8") as f:
        data = json.dumps(dictData, ensure_ascii=False)
        f.write(data)


def save_text_file(filename, text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
