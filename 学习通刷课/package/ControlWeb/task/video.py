# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 22:02
# @Author : Levitan
# @File : video.py
# @Software : PyCharm
import time
from selenium.webdriver.common.by import By

class Video:
    def __init__(self, driver):
        self.__driver = driver

    def finish(self):
        self.__driver.find_element(By.CSS_SELECTOR, '[class="vjs-big-play-button"]').click()
        time.sleep(2)
        nowTime = self.__driver.find_element(By.CLASS_NAME, 'vjs-current-time-display').text
        endTime = self.__driver.find_element(By.CLASS_NAME, 'vjs-duration-display').text
        endTimeData = endTime.partition(":")
        print("视频总时长{}分{}秒".format(endTimeData[0], endTimeData[-1]))
        counterTime = 2

        while nowTime != endTime:
            time.sleep(1)
            nowTime = self.__driver.find_element(By.CLASS_NAME, 'vjs-current-time-display').text
            print('\r'+'已观看{}分{}秒'.format(counterTime//60, counterTime % 60), end='')
            counterTime += 1
            try:
                self.__answer()
            except Exception:
                continue
        print("\n视频任务完成")

    def __answer(self):
        title = self.__driver.find_element(By.CSS_SELECTOR, '.ans-videoquiz-title').text[1:4]
        if title == '判断题' or title == '单选题':
            self.__driver\
                .find_element(By.CSS_SELECTOR, '[type="radio"][name="ans-videoquiz-opt"][value="true"]')\
                .click()
            time.sleep(1)
        else:
            answerList = self.__driver.find_elements(By.CSS_SELECTOR, '[type="checkbox"][value="true"]')
            for i in answerList:
                i.click()
                time.sleep(1)
        self.__driver.find_element(By.CSS_SELECTOR, '.ans-videoquiz-submit').click()
