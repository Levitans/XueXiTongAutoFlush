# -*- encoding = utf-8 -*-
# @Time : 2022-02-07 20:09
# @Author : Levitan
# @File : browseOrDriverPathException.py
# @Software : PyCharm

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
        