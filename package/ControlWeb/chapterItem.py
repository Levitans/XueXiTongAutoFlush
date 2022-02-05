# -*- encoding = utf-8 -*-
# @Time : 2022-02-05 12:36
# @Author : Levitan
# @File : chapterItem.py
# @Software : PyCharm

from selenium.webdriver.common.by import By

class ChapterItem:
    def __init__(self, webObj):
        self.number: str = ""
        self.name: str = ""
        self.isFinish: bool = False
        self.webObj = webObj
        self.__parseWebObj(webObj)

    def __parseWebObj(self, webObject):
        self.name = webObject.find_element(By.CSS_SELECTOR, '[class="chapter_item"]').get_attribute("title")
        string = webObject.find_element(By.CSS_SELECTOR, '[class="catalog_name"]').text
        self.number = string[:string.find(self.name)]
        catalogTaskText = webObject.find_element(By.CSS_SELECTOR, '[class="catalog_task"]').text
        self.isFinish = True if catalogTaskText == "" else False

    def __str__(self):
        return "number="+self.number+",name="+self.name+",isFinish="+str(self.isFinish)
