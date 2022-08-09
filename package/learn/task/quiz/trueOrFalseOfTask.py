# -*- encoding = utf-8 -*-
# @Time : 2022-02-06 22:28
# @Author : Levitan
# @File : trueOrFalseOfTask.py
# @Software : PyCharm

# 自定义包
from ..interface import Answerable
from .question import TrueOrFalse

# 第三方包
from selenium.webdriver.remote.webelement import WebElement


class TrueOrFalseOfTask(TrueOrFalse, Answerable):
    def __init__(self, questionWebObj, qType, question, answer, answerWebElementList):
        """
        :param qType: 题目类型（单选题，多选题）
        :param question: 题目问题
        :param answer: 查找到的题目答案
        :param answerWebElementList: 题目选项的WebElement对象， 列表类型
        """
        super(TrueOrFalseOfTask, self).__init__(qType, question, answer)
        self.__answerWebElementList: list[WebElement] = answerWebElementList
        self.qWebObj = questionWebObj  # 整个题目的web对象，用于定位到题目

    def getAnswerWebElement(self):
        """
        :return: 返回正确答案的WebElement对象
        """
        answer = self.getAnswer()[0]
        if not isinstance(answer, bool):
            return []
        index = 0 if answer else 1
        return [self.__answerWebElementList[index]]
