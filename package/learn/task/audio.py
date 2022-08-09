# -*- encoding = utf-8 -*-
# @Time : 2022-03-26 21:47
# @Author : Levitan
# @File : audio.py
# @Software : PyCharm
import time

# 第三方包
from selenium.webdriver.common.by import By
from package.learn.task.interface import Task

class Audio(Task):
    def __init__(self, driver):
        super().__init__(driver)
        self.__name__ = "音频"

    def isCurrentTask(self, iframeIndex) -> bool:
        iframeList = self._Task__driver.find_elements(By.TAG_NAME, 'iframe')
        return iframeList[iframeIndex].get_attribute("class") == "ans-attach-online ans-insertaudio"

    def finish(self):
        button = self._Task__driver.find_element(By.CSS_SELECTOR, '[class="vjs-play-control vjs-control vjs-button"]')
        self._Task__driver.execute_script("arguments[0].scrollIntoView(false);", button)

        nowTime = self._Task__driver.find_element(By.CSS_SELECTOR, '[class="vjs-current-time vjs-time-control vjs-control"]')\
            .find_element(By.CSS_SELECTOR, '[class="vjs-current-time-display"]').text

        endTime = self._Task__driver.find_element(By.CSS_SELECTOR, '[class="vjs-duration vjs-time-control vjs-control"]')\
            .find_element(By.CSS_SELECTOR, '[class="vjs-duration-display"]').text

        button.click()

        while nowTime != endTime:
            time.sleep(1)
            nowTime = self._Task__driver.find_element(By.CSS_SELECTOR, '[class="vjs-current-time vjs-time-control vjs-control"]') \
                .find_element(By.CSS_SELECTOR, '[class="vjs-current-time-display"]').text
            print("\r"+"当前音频进度{}/{}".format(nowTime, endTime), end="")
