# -*- encoding = utf-8 -*-
# @Time : 2022-04-15 21:00
# @Author : Levitan
# @File : fuist.py
# @Software : PyCharm

from package.learn.school.template import Course, Chapter
from selenium.common import exceptions
from selenium.webdriver.common.by import By


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


def get_chapters(driver) -> list[Chapter]:
    chapterUnitList = driver.find_elements(By.CSS_SELECTOR, '[class="chapter_unit"]')
    itemList = []
    for i in chapterUnitList:
        # 因为找到的WebElement是在一个列表中，所用这里使用 “+” 来连接
        itemList += i.find_elements(By.TAG_NAME, "li")
    chaptersList = []
    for i in itemList:
        name = i.find_element(By.CSS_SELECTOR, '[class="chapter_item"]').get_attribute("title")
        catalogTaskText = i.find_element(By.CSS_SELECTOR, '[class="catalog_task"]').text
        finishKey = True if catalogTaskText == "" else False
        chaptersList.append(Chapter(name, i, finishKey))
    return chaptersList
