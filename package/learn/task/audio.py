# -*- encoding = utf-8 -*-
# @Time : 2022-03-26 21:47
# @Author : Levitan
# @File : audio.py
# @Software : PyCharm
import time

from selenium.webdriver.common.by import By
from package.learn.task.interface import Task

class Audio(Task):
    def __init__(self, driver):
        self.__name__ = "音频"
        self.__driver = driver

    def isCurrentTask(self, iframeIndex) -> bool:
        iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
        if iframeList[iframeIndex].get_attribute("class") == "ans-attach-online ans-insertaudio":
            return True
        else:
            return False

    def finish(self):
        button = self.__driver.find_element(By.CSS_SELECTOR, '[class="vjs-play-control vjs-control vjs-button"]')
        self.__driver.execute_script("arguments[0].scrollIntoView(false);", button)

        nowTime = self.__driver.find_element(By.CSS_SELECTOR, '[class="vjs-current-time vjs-time-control vjs-control"]')\
            .find_element(By.CSS_SELECTOR, '[class="vjs-current-time-display"]').text

        endTime = self.__driver.find_element(By.CSS_SELECTOR, '[class="vjs-duration vjs-time-control vjs-control"]')\
            .find_element(By.CSS_SELECTOR, '[class="vjs-duration-display"]').text

        button.click()

        while nowTime != endTime:
            time.sleep(1)
            nowTime = self.__driver.find_element(By.CSS_SELECTOR, '[class="vjs-current-time vjs-time-control vjs-control"]') \
                .find_element(By.CSS_SELECTOR, '[class="vjs-current-time-display"]').text
            print("\r"+"当前音频进度{}/{}".format(nowTime, endTime), end="")
