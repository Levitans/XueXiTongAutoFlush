# -*- encoding = utf-8 -*-
# @Time : 2022-02-07 13:13
# @Author : Levitan
# @File : answerable.py
# @Software : PyCharm

from abc import abstractmethod, ABCMeta

from selenium.webdriver.remote.webelement import WebElement


class Answerable(metaclass=ABCMeta):
    @abstractmethod
    def getAnswerWebElement(self) -> list[WebElement]:
        pass
