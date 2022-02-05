# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 14:03
# @Author : Levitan
# @File : course.py
# @Software : PyCharm

import time

from selenium.webdriver.common.by import By
from package.display import Display

# 课程类
class Course:
    def __init__(self):
        self.__coursesObjectList = []
        self.__coursesNameList = []
        self.nowCourseName = ""

    # 获取课程对象和课程名称
    def getCourseObjectAndName(self, driver):
        """
        :param driver: 传入需要获取章节的WebDriver对象。
        :return:
        """
        driver.find_element(By.CSS_SELECTOR, '[name="课程"]').click()
        time.sleep(2)

        driver.switch_to.frame("frame_content")

        findCourseList = driver.find_element(By.CSS_SELECTOR, '[class="course-list"]') \
            .find_elements(By.CSS_SELECTOR, '[class="course clearfix"]')

        # 添加课程WebElement和课程名到课程对象中
        for i in findCourseList:
            self.__coursesObjectList.append(i.find_element(By.CSS_SELECTOR, '[target="_blank"]'))
            self.__coursesNameList.append(i.find_element(By.CSS_SELECTOR, '[class="color1"]').text)

    def getCourseObjectList(self):
        return self.__coursesObjectList

    def getCourseNameList(self):
        return self.__coursesNameList
