# -*- encoding = utf-8 -*-
# @Time : 2022-04-15 15:01
# @Author : Levitan
# @File : template.py
# @Software : PyCharm

import abc

# 第三方包
from selenium.webdriver.chrome.webdriver import WebDriver

class Course:
    def __init__(self, name, courseid, clazzid, personid, url):
        """
            :name: 课程名称
            :courseid: 课程的id，这个值由学习通提供，可在页面中找到
            :clazzid: 这个值由学习通提供，可在页面中找到
            :personid: 这个值由学习通提供，可在页面中找到
            :url: 课程的url
        """
        self.name = name
        self.courseid = courseid
        self.clazzid = clazzid
        self.personid = personid
        self.url = url

    # 获取课程的章节地址
    def get_ZJ_path(self):
        father_path = "https://mooc2-ans.chaoxing.com/mycourse/studentcourse?"
        return "{}courseid={}&clazzid={}&cpi={}&ut=s".format(father_path, self.courseid, self.clazzid, self.personid)


class Chapter:
    """
        :catalog_sbar: 章节号
        :name: 章节名字
        :weElement: 章节的WebElement对象
        :isFinish: 当前章节是否完成的标志
    """
    def __init__(self, catalog_sbar, name, webElement, isFinish):
        self.catalog_sbar = catalog_sbar
        self.name = name
        self.webElement = webElement
        self.isFinish = isFinish

    # 返回当前章节的描述
    def toString(self) -> str:
        return "{} {}".format(self.catalog_sbar, self.name)


class School(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_courses(driver: WebDriver) -> list[Course]:
        ...

    @staticmethod
    @abc.abstractmethod
    def get_chapters(driver: WebDriver) -> list[Chapter]:
        ...
