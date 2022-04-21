# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 21:47
# @Author : Levitan
# @File : PPT.py
# @Software : PyCharm
import time
import random
from selenium.webdriver.common.by import By
from package.learn.task.interface import Task
from package.learn import globalvar as gl

class PPT(Task):
    def __init__(self, driver):
        self.__name__ = "PPT"
        self.__driver = driver

    def isCurrentTask(self, iframeIndex) -> bool:
        iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
        if iframeList[iframeIndex].get_attribute("class") in \
                ("ans-attach-online insertdoc-online-pdf", "ans-attach-online insertdoc-online-ppt"):
            return True
        else:
            return False

    def finish(self):
        try:
            PPT.__ppt1(self.__driver)
        except Exception:
            PPT.__ppt2(self.__driver)

    @staticmethod
    def __ppt1(driver):
        pageData = driver.find_element(By.CSS_SELECTOR, '[class="mkeNum mkeNum_bom"]') \
                         .find_element(By.CSS_SELECTOR, '[class="fl pageInfo"]') \
                         .text \
                         .replace(" ", "") \
                         .partition("/")

        nextBtn = driver.find_element(By.CSS_SELECTOR, '[class="mkeNum mkeNum_bom"]') \
                        .find_element(By.CSS_SELECTOR, '[class="turnpage_Btn"]') \
                        .find_element(By.CSS_SELECTOR, '[class="nextBtn"]')

        newPage = int(pageData[0])
        endPage = int(pageData[-1])

        while newPage < endPage:
            nextBtn.click()
            newPage += 1
            print('\r' + '已观看{}张'.format(newPage), end='')
            time.sleep(random.randint(gl.ppt_speed_min, gl.ppt_speed_max))

    @staticmethod
    def __ppt2(driver):
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, '[id="panView"]'))  # id="iframe"
        imgList = driver.find_elements(By.TAG_NAME, 'img')
        print("共有{}张PPT".format(len(imgList)))
        for i in range(len(imgList)):
            print('\r'+"观看第{}张PPT".format(i+1), end="")
            driver.execute_script("window.scrollBy(0,2000)")
            time.sleep(random.randint(gl.ppt_speed_min, gl.ppt_speed_max))
        print()
