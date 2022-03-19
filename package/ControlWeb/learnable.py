# -*- encoding = utf-8 -*-
# @Time : 2022-03-15 15:07
# @Author : Levitan
# @File : learnable.py
# @Software : PyCharm

from abc import abstractmethod, ABCMeta
from selenium.webdriver.remote.webelement import WebElement

class Course:
    def __init__(self, name: str, webElement: WebElement):
        self.name = name
        self.webElement = webElement

class ChapterItem:
    def __init__(self, name, webElement, finishKey):
        self.name: str = name
        self.webElement: WebElement = webElement
        self.isFinish: bool = finishKey

class Learnable(metaclass=ABCMeta):
    @abstractmethod
    def isNew(self) -> bool:    # 判断进入课程后的页面是否为新版本页面
        pass

    @abstractmethod
    def changeToNewPage(self):    # 将旧页面切换为新页面
        pass

    @abstractmethod
    def getCourses(self) -> list[Course]:   # 获取页面课程
        pass

    @abstractmethod
    def enterCourse(self, course: Course) -> bool:      # 进入课程
        pass

    @abstractmethod
    def clickChapter(self) -> bool:     # 点击课程左侧的章节选项
        pass

    @abstractmethod
    def getChapter(self) -> list[ChapterItem]:      # 获取页面中的章节
        pass
