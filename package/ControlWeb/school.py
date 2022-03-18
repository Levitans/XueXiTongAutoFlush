# -*- encoding = utf-8 -*-
# @Time : 2022-03-15 15:35
# @Author : Levitan
# @File : school.py
# @Software : PyCharm
import selenium.common.exceptions

from package.ControlWeb.learnable import Learnable, Course, ChapterItem
from selenium.webdriver.common.by import By
import time


class Fuist(Learnable):
    def __init__(self, webDriver):
        self.__driver = webDriver

    def isNew(self) -> bool:
        pass

    def getCourses(self) -> list[Course]:
        self.__driver.find_element(By.CSS_SELECTOR, '[name="课程"]').click()
        time.sleep(2)

        self.__driver.switch_to.frame("frame_content")

        itemList = self.__driver.find_element(By.CSS_SELECTOR, '[class="course-list"]') \
            .find_elements(By.CSS_SELECTOR, '[class="course clearfix"]')

        coursesList = []

        for i in itemList:
            webElement = i.find_element(By.CSS_SELECTOR, '[target="_blank"]')
            name = i.find_element(By.CSS_SELECTOR, '[class="color1"]').text
            coursesList.append(Course(name, webElement))

        return coursesList

    def enterCourse(self, course) -> bool:
        item = course.webElement
        self.__driver.execute_script("arguments[0].focus();", item)
        time.sleep(1)
        try:
            item.click()
        except selenium.common.exceptions.WebDriverException:
            self.__driver.switch_to.default_content()
            self.__driver.execute_script("window.scrollBy(0,100)")
            self.__driver.switch_to.frame("frame_content")
            time.sleep(1)
            item.click()

        # 切换浏览器窗口
        headLes = self.__driver.window_handles
        self.__driver.switch_to.window(headLes[1])
        time.sleep(3)

        return True

    def clickChapter(self) -> bool:
        try:
            self.__driver.find_element(By.CSS_SELECTOR, '[class="nav_side"]') \
                .find_element(By.CSS_SELECTOR, '[class="sideCon"]') \
                .find_element(By.CSS_SELECTOR, '[class="nav-content "]') \
                .find_element(By.CSS_SELECTOR, '[dataname="zj-stu"]').click()
        except selenium.common.exceptions.NoSuchElementException:
            try:
                self.__driver.find_element(By.CSS_SELECTOR, '[class="nav_side"]') \
                    .find_element(By.CSS_SELECTOR, '[class="sideCon"]') \
                    .find_element(By.CSS_SELECTOR, '[class="nav-content "]') \
                    .find_element(By.CSS_SELECTOR, '[dataname="zj"]').click()
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    self.__driver.find_element(By.CSS_SELECTOR, '[class="nav_side"]') \
                        .find_element(By.CSS_SELECTOR, '[class="sideCon"]') \
                        .find_element(By.CSS_SELECTOR, '[class="nav-content   stuNavigationList"]') \
                        .find_element(By.CSS_SELECTOR, '[dataname="zj"]').click()
                except selenium.common.exceptions.NoSuchElementException:
                    return False
        return True

    def getChapter(self) -> list[ChapterItem]:
        # 进入页面的iframe
        iframeList = self.__driver.find_elements(By.CSS_SELECTOR, '[id="frame_content-zj-stu"]')
        if len(iframeList) == 0:
            iframeList = self.__driver.find_elements(By.CSS_SELECTOR, '[id="frame_content-zj"]')
        self.__driver.switch_to.frame(iframeList[-1])

        # 找到页面所有章节单元
        chapterUnitList = self.__driver.find_elements(By.CSS_SELECTOR, '[class="chapter_unit"]')

        # 找到章节单元中的章节保存到itemList中
        itemList = []
        for i in chapterUnitList:
            itemList += i.find_elements(By.TAG_NAME, "li")

        # 将itemList中的元素解析为Chapter对象保存到chapterLIst中
        chapterList = []
        for i in itemList:
            name = i.find_element(By.CSS_SELECTOR, '[class="chapter_item"]').get_attribute("title")
            catalogTaskText = i.find_element(By.CSS_SELECTOR, '[class="catalog_task"]').text
            finishKey = True if catalogTaskText == "" else False
            chapterList.append(ChapterItem(name, i, finishKey))

        return chapterList
