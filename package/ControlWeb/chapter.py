# -*- encoding = utf-8 -*-
# @Time : 2022-02-05 12:44
# @Author : Levitan
# @File : chapter.py
# @Software : PyCharm

from selenium.webdriver.common.by import By
from package.ControlWeb.chapterItem import ChapterItem

# 章节类
class Chapter:
    def __init__(self):
        self.__chapterItemList: list[ChapterItem] = []

    # 获取章节WebDriver对象和名称
    def getChapterItem(self, driver):
        # 进入页面的iframe
        iframeList = driver.find_elements(By.CSS_SELECTOR, '[id="frame_content-zj-stu"]')
        if len(iframeList) == 0:
            iframeList = driver.find_elements(By.CSS_SELECTOR, '[id="frame_content-zj"]')
        driver.switch_to.frame(iframeList[-1])

        # 获取章节对象和章节名
        chaptersList = driver.find_elements(By.CSS_SELECTOR, '[class="chapter_unit"]')
        for i in chaptersList:
            sectionList = i.find_elements_by_tag_name("li")
            for j in sectionList:
                self.__chapterItemList.append(ChapterItem(j))

    def getLength(self):
        """
        :return: 章节的个数
        """
        return len(self.__chapterItemList)

    def getChapterItemList(self):
        return self.__chapterItemList
