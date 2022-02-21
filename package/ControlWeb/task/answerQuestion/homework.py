# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 22:20
# @Author : Levitan
# @File : homework.py
# @Software : PyCharm
import time

import requests.exceptions

from package.ControlWeb.task.answerQuestion.getAnswer import GetAnswer
from package.ControlWeb.task.answerQuestion.multipleChoiceOfTask import MultipleChoiceOfTask
from package.ControlWeb.task.answerQuestion.trueOrFalseOfTask import TrueOrFalseOfTask
from package.ControlWeb.task.answerQuestion.answerable import Answerable
from package.display import Display
from selenium.webdriver.common.by import By


class Homework:
    def __init__(self, driver):
        self.__driver = driver
        self.__questionList: list[Answerable] = []

    def getData(self):
        # 进入iframe
        iframe = self.__driver.find_element(By.CSS_SELECTOR, '[id="frame_content"]')
        self.__driver.switch_to.frame(iframe)

        # 获取页面中的所有题目
        questionList = self.__driver.find_elements(By.CSS_SELECTOR, '[class="TiMu"]')
        print("当前页面共有{}题".format(len(questionList)))

        for i in range(len(questionList)):
            Display.separate(10)
            item = questionList[i]
            title = item.find_element(By.CSS_SELECTOR, '[class="Zy_TItle clearfix"]').text.replace("\n", "")
            # 获取问题
            question = title[title.find("】")+1:]

            # 题目类型
            questionType = title[title.find("【")+1: title.find("】")]

            # 获取问题答案
            answer = GetAnswer.getAnswer(question, questionType)
            # 判断是否找到答案
            if answer is None:
                continue
            if questionType in ("单选题", "多选题"):
                # 获取题目选项的WebElement对象
                # optionWebElementList = item.find_elements(By.CSS_SELECTOR, '[class="fl after"]')
                optionWebElementList = item.find_elements(By.TAG_NAME, 'li')
                # 获取题目选项
                optionTextList = []
                for option in optionWebElementList:
                    optionTextList.append(option.find_element(By.CSS_SELECTOR, '[class="fl after"]').text.replace("\n", ""))
                self.__questionList.append(
                    MultipleChoiceOfTask(item, questionType, question, answer, optionTextList, optionWebElementList))
            elif questionType == "判断题":
                answerWebElementList = item.find_elements(By.TAG_NAME, "label")
                self.__questionList.append(TrueOrFalseOfTask(item, questionType, question, answer, answerWebElementList))
            else:
                raise Exception("当前题目类型为：{}，不在（单选题、多选题、判断题）中，程序无法解决".format(questionType))

    def finish(self):
        for i in range(len(self.__questionList)):
            print("正在完成第{}题".format(i+1))
            webElementList = self.__questionList[i].getAnswerWebElement()
            if len(webElementList) == 0:
                print("查找答案和选项答案不匹配")
                continue
            for answerWebElement in webElementList:
                self.__driver.execute_script("arguments[0].scrollIntoView();", self.__questionList[i].qWebObj)
                time.sleep(1)
                answerWebElement.click()

    def submitOrSave(self):
        # if self.__checkpoint:
        #     self.__driver.find_element(By.CSS_SELECTOR, '[href="javascript:void(0);"][onclick="btnBlueSubmit();"]').click()
        #     time.sleep(1)
        #     try:
        #         self.__driver.find_element(By.CSS_SELECTOR, '[class="bluebtn "][onclick="form1submit();"]').click()
        #     except Exception:
        #         self.__driver.find_element(By.CSS_SELECTOR, '[class="bluebtn "][onclick="submitCheckTimes();"]').click()
        #     time.sleep(1)
        # else:
        #     self.__driver.find_element(By.CSS_SELECTOR, '[onclick="noSubmit();"]').click()
        #     time.sleep(1)
        #     self.__driver.switch_to.alert.accept()
        self.__driver.find_element(By.CSS_SELECTOR, '[onclick="noSubmit();"]').click()
        time.sleep(1)
        self.__driver.switch_to.alert.accept()
