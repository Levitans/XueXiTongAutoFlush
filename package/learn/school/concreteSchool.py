# -*- encoding = utf-8 -*-
# @Time : 2022-04-15 21:00
# @Author : Levitan
# @File : concreteSchool.py
# @Software : PyCharm

# 自定义包
from .template import Course, Chapter, School

# 第三方包
from selenium.common import exceptions
from selenium.webdriver.common.by import By

"""
    这是程序中默认获取课程列表和章节列表的类
    该类对大部分学校的学习通都适用
    
    如果默认的类无法获取的你学习通上的课程或章节
"""
class Default(School):
    @staticmethod
    def get_courses(driver) -> list[Course]:
        courseList = []
        item_list = driver.find_elements(By.CSS_SELECTOR, '[class="course clearfix"]')
        for i in item_list:
            courseid = i.get_attribute("courseid")
            clazzid = i.get_attribute("clazzid")
            personid = i.get_attribute("personid")
            name = i.find_element(By.CSS_SELECTOR, '[class="color1"]').text
            url = i.find_element(By.TAG_NAME, "a").get_attribute("href")
            courseList.append(Course(name, courseid, clazzid, personid, url))
        return courseList

    @staticmethod
    def get_chapters(driver) -> list[Chapter]:
        chapterUnitList = driver.find_elements(By.CSS_SELECTOR, '[class="chapter_unit"]')
        itemList = []
        for i in chapterUnitList:
            # 因为找到的WebElement是在一个列表中，所用这里使用 “+” 来连接
            itemList += i.find_elements(By.TAG_NAME, "li")
        chaptersList = []
        for i in itemList:
            catalog_sbar = i.find_element(By.CSS_SELECTOR, '[class="catalog_sbar"]').text
            name = i.find_element(By.CSS_SELECTOR, '[class="chapter_item"]').get_attribute("title")
            catalogTaskText = i.find_element(By.CSS_SELECTOR, '[class="catalog_task"]').text
            finishKey = True if catalogTaskText == "" else False
            chaptersList.append(Chapter(catalog_sbar, name, i, finishKey))
        return chaptersList


class Default2(Default):
    """
    这个是在默认类中获取课程适用，但是获取章节不适用的一种情况

    """
    @staticmethod
    def get_chapters(driver) -> list[Chapter]:
        chapterUnitList = driver.find_elements(By.CSS_SELECTOR, '[class="chapter_unit"]')
        itemList = []
        for i in chapterUnitList:
            itemList += i.find_elements(By.CSS_SELECTOR, '[class="chapter_item"]')
        chaptersList = []
        for i in itemList:
            catalog_sbar = i.find_element(By.CSS_SELECTOR, '[class="catalog_sbar"]').text
            name = i.get_attribute("title")
            catalogTaskText = i.find_element(By.CSS_SELECTOR, '[class="catalog_task"]').text
            finishKey = True if catalogTaskText == "" else False
            chaptersList.append(Chapter(catalog_sbar, name, i, finishKey))
        return chaptersList
