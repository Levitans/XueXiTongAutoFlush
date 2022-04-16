# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 22:02
# @Author : Levitan
# @File : video.py
# @Software : PyCharm
import time
from selenium.webdriver.common.by import By
from package.learn.task.interface import Task

class Video(Task):
    def __init__(self, driver):
        self.__name__ = "视频"
        self.__driver = driver

    def isCurrentTask(self, iframeIndex) -> bool:
        iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
        if iframeList[iframeIndex].get_attribute("class") == "ans-attach-online ans-insertvideo-online":
            return True
        else:
            return False

    def finish(self):
        # 将按钮移动到屏幕中在点击
        button = self.__driver.find_element(By.CSS_SELECTOR, '[class="vjs-big-play-button"]')
        self.__driver.execute_script("arguments[0].scrollIntoView(false);", button)
        time.sleep(1)
        button.click()

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
                self.__answer(self.__driver)
            except Exception:
                continue

    @staticmethod
    def __answer(driver):
        title = driver.find_element(By.CSS_SELECTOR, '.ans-videoquiz-title').text[1:4]
        if title == '判断题' or title == '单选题.txt':
            driver\
                .find_element(By.CSS_SELECTOR, '[type="radio"][name="ans-videoquiz-opt"][value="true"]')\
                .click()
            time.sleep(1)
        else:
            answerList = driver.find_elements(By.CSS_SELECTOR, '[type="checkbox"][value="true"]')
            for i in answerList:
                i.click()
                time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.ans-videoquiz-submit').click()
