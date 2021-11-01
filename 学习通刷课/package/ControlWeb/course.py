# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 14:03
# @Author : Levitan
# @File : course.py
# @Software : PyCharm

import time
from selenium.webdriver.common.by import By

# 课程类
class Course:
    def __init__(self):
        self.__coursesObjectList = []
        self.__coursesNameList = []
        self.nowCourseName = ""

    # 获取课程对象和课程名称
    def getCourseObjectAndName(self, driver):
        driver.find_element(By.CLASS_NAME, "zne_kc_icon").click()
        time.sleep(2)

        driver.switch_to.frame("frame_content")

        findCourseList = driver.find_element(By.CSS_SELECTOR, '[class="course-list"]') \
            .find_elements(By.CSS_SELECTOR, '[class="course clearfix"]')

        # 添加课程WebElement和课程名到课程对象中
        for i in findCourseList:
            self.addCourseObject(i.find_element(By.CSS_SELECTOR, '[target="_blank"]'))
            self.addCourseName(i.find_element(By.CSS_SELECTOR, '[class="color1"]').text)

    def addCourseObject(self, item):
        self.__coursesObjectList.append(item)

    def addCourseName(self, courseName):
        self.__coursesNameList.append(courseName)

    def getCourseObjectList(self):
        return self.__coursesObjectList

    def getCourseNameList(self):
        return self.__coursesNameList


# 章节类
class Chapter:
    def __init__(self):
        self.__chapterObjectList = []
        self.__chaptersNameList = []

    # 获取章节WebDriver对象和名称
    def getChapterObjectAndName(self, driver):
        # 进入页面的iframe
        iframeList = driver.find_elements(By.CSS_SELECTOR, '[id="frame_content-zj-stu"]')
        driver.switch_to.frame(iframeList[-1])

        # 获取章节对象和章节名
        chaptersList = driver.find_elements(By.CSS_SELECTOR, '[class="chapter_unit"]')
        for i in chaptersList:
            sectionList = i.find_elements_by_tag_name("li")
            for j in sectionList:
                self.__chapterObjectList.append(j)

                # 提取章节中的章节号
                string = j.text
                newString = ""
                for s in string:
                    if s.isdigit() or s == ".":
                        newString += s
                    else:
                        break
                self.__chaptersNameList.append(newString)

    def getLength(self):
        return len(self.__chapterObjectList)

    def getChapterObjectList(self):
        return self.__chapterObjectList

    def getChaptersNameList(self):
        return self.__chaptersNameList
