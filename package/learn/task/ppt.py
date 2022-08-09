# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 21:47
# @Author : Levitan
# @File : PPT.py
# @Software : PyCharm
import time
import random

# 自定义包
from .interface import Task

# 第三方包
from selenium.webdriver.common.by import By

class PPT(Task):
    __maxSpeed = 3
    __minSpeed = 1

    def __init__(self, driver):
        super().__init__(driver)
        self.__name__ = "PPT"

    def isCurrentTask(self, iframeIndex) -> bool:
        
        iframeList = self._Task__driver.find_elements(By.TAG_NAME, 'iframe')
        return iframeList[iframeIndex].get_attribute("class") in ("ans-attach-online insertdoc-online-pdf", "ans-attach-online insertdoc-online-ppt")

    def finish(self):
        try:
            self.__ppt1()
        except Exception:
            self.__ppt2()

    def __ppt1(self):
        pageData = self._Task__driver.find_element(By.CSS_SELECTOR, '[class="mkeNum mkeNum_bom"]') \
                                   .find_element(By.CSS_SELECTOR, '[class="fl pageInfo"]') \
                                   .text \
                                   .replace(" ", "") \
                                   .partition("/")

        nextBtn = self._Task__driver.find_element(By.CSS_SELECTOR, '[class="mkeNum mkeNum_bom"]') \
                                  .find_element(By.CSS_SELECTOR, '[class="turnpage_Btn"]') \
                                  .find_element(By.CSS_SELECTOR, '[class="nextBtn"]')

        newPage = int(pageData[0])
        endPage = int(pageData[-1])

        while newPage < endPage:
            nextBtn.click()
            newPage += 1
            print('\r' + '已观看{}张'.format(newPage), end='')
            time.sleep(random.randint(self.__minSpeed, self.__maxSpeed))

    def __ppt2(self):
        self._Task__driver.switch_to.frame(self._Task__driver.find_element(By.CSS_SELECTOR, '[id="panView"]'))  # id="iframe"
        imgList = self._Task__driver.find_elements(By.TAG_NAME, 'img')
        print("共有{}张PPT".format(len(imgList)))
        for i in range(len(imgList)):
            print('\r'+"观看第{}张PPT".format(i+1), end="")
            self._Task__driver.execute_script("window.scrollBy(0,2000)")
            time.sleep(random.randint(self.__minSpeed, self.__maxSpeed))
        print()
