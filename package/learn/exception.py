# -*- encoding = utf-8 -*-
# @Time : 2022-02-18 13:22
# @Author : Levitan
# @File : exception.py
# @Software : PyCharm

class AtOrPdException(Exception):
    def __str__(self):
        return "账号或密码错误"

class BrowseOrDriverPathException(Exception):
    def __init__(self, errorBrowserPath, errorDriverPath):
        self.__errorBrowserPath = errorBrowserPath
        self.__errorDriverPath = errorDriverPath

    def __str__(self):
        errorInfo = r"""浏览器地址或浏览器驱动地址配置错误
    当前,浏览器地址为：{}
          驱动地址为：{}

地址格式应该为以下几种
    第一种：
        浏览器地址：C:\\Users\\admin-dell\\Desktop\\chrome\\chrome.exe
        浏览器驱动地址：C:\\Users\\admin-dell\\Desktop\\driver\\chrome\\chromedriver.exe

    第二种：
        浏览器地址：C:/Users/admin-dell/Desktop/chrome/chrome.exe
        浏览器驱动地址：C:/Users/admin-dell/Desktop/driver/chrome/chromedriver.exe
            """.format(self.__errorBrowserPath, self.__errorDriverPath)
        return errorInfo

class NoFoundAnswerException(Exception):
    """
    在接口中没有找到答案抛出此异常。
    """
    pass

class InitializationException(Exception):
    pass

class TimeoutException(Exception):
    pass
