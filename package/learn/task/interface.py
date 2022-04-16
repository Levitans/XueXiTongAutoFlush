# -*- encoding = utf-8 -*-
# @Time : 2022-04-15 22:53
# @Author : Levitan
# @File : interface.py
# @Software : PyCharm
from abc import abstractmethod, ABCMeta
from selenium.webdriver.remote.webelement import WebElement

class Task(metaclass=ABCMeta):
    @abstractmethod
    def isCurrentTask(self, iframeIndex) -> bool:
        pass

    @abstractmethod
    def finish(self):
        pass


class Answerable(metaclass=ABCMeta):
    @abstractmethod
    def getAnswerWebElement(self) -> list[WebElement]:
        pass
