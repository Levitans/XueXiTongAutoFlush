# -*- encoding = utf-8 -*-
# @Time : 2022-02-06 12:47
# @Author : Levitan
# @File : atOrPdException.py
# @Software : PyCharm

class AtOrPdException(Exception):
    def __str__(self):
        return "账号或密码错误"
