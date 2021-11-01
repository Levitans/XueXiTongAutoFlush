# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 21:47
# @Author : Levitan
# @File : PPT.py
# @Software : PyCharm
import time
import random
from selenium.webdriver.common.by import By

class PPT:
    def __init__(self, driver):
        self.__pageData = driver.find_element(By.CSS_SELECTOR, '[class="mkeNum mkeNum_bom"]')\
                                .find_element(By.CSS_SELECTOR, '[class="fl pageInfo"]')\
                                .text\
                                .replace(" ", "") \
                                .partition("/")

        self.__nextBtn = driver.find_element(By.CSS_SELECTOR, '[class="mkeNum mkeNum_bom"]')\
                               .find_element(By.CSS_SELECTOR, '[class="turnpage_Btn"]')\
                               .find_element(By.CSS_SELECTOR, '[class="nextBtn"]')

        self.__newPage = int(self.__pageData[0])
        self.__endPage = int(self.__pageData[-1])

    def finish(self):
        while self.__newPage < self.__endPage:
            self.__nextBtn.click()
            time.sleep(random.randint(2, 4))
            self.__newPage += 1
            print('\r' + '已观看{}张'.format(self.__newPage), end='')
        print("\nppt任务完成")
