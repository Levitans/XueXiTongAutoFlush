# -*- encoding = utf-8 -*-
# @Time : 2022-08-01 19:39
# @Author : Levitan
# @File : exception.py
# @Software : PyCharm

class NoFoundAnswerException(Exception):
    """
    在接口中没有找到答案抛出此异常。
    """
    pass
