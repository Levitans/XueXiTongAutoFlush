# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 21:47
# @Author : Levitan
# @File : PPT.py
# @Software : PyCharm
import time
import random
from selenium.webdriver.common.by import By

class PPT:
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
            time.sleep(random.randint(2, 4))
            newPage += 1
            print('\r' + '已观看{}张'.format(newPage), end='')

    @staticmethod
    def __ppt2(driver):
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, '[id="panView"]'))
        imgList = driver.find_elements(By.TAG_NAME, 'img')
        print("共有{}张PPT".format(len(imgList)))
        for i in range(len(imgList)):
            print("观看第{}张PPT".format(i+1))
            driver.execute_script("window.scrollBy(0,2000)")
            time.sleep(1)

    @staticmethod
    def finish(driver):
        try:
            PPT.__ppt1(driver)
        except Exception:
            PPT.__ppt2(driver)
