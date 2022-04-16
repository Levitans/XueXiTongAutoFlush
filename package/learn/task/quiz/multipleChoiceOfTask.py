# -*- encoding = utf-8 -*-
# @Time : 2022-02-06 16:08
# @Author : Levitan
# @File : multipleChoiceOfTask.py
# @Software : PyCharm

import difflib
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from package.learn.task.quiz.question import MultipleChoice
from package.learn.task.interface import Answerable

class MultipleChoiceOfTask(MultipleChoice, Answerable):
    def __init__(self, questionWebObj, qType, question, answersList, options, optionsWebElements):
        """
        :param qType: 题目类型（单选题，多选题）
        :param question: 题目问题
        :param answersList: 查找到的题目答案，list类型
        :param options: 题目选项文字，list类型
        :param optionsWebElements: 题目选项的WebElement对象， 列表类型
        """
        super(MultipleChoiceOfTask, self).__init__(qType, question, answersList, options)
        self.__optionsWebElements: list[WebElement] = optionsWebElements
        self.qWebObj = questionWebObj       # 整个题目的web对象，用于定位到题目

    def getAnswerWebElement(self):
        """
        :return: 将查找到的答案与题目选项相比较，返回一个包含正确选项WebElement对象的列表
        """
        answerWebElementList = []
        answerList = self.getAnswer()
        options = self.getOptions()
        for answerIndex in range(len(answerList)):
            for i in range(len(options)):
                for j in range(len(answerList[answerIndex])):
                    if self.__optionsWebElements[i] in answerWebElementList:
                        continue
                    similarDiffRatio = difflib.SequenceMatcher(None, options[i], answerList[answerIndex][j]).quick_ratio()
                    if similarDiffRatio > 0.88:
                        if self.__optionsWebElements[i].find_element(By.TAG_NAME, "input").get_attribute("checked") is None:
                            answerWebElementList.append(self.__optionsWebElements[i])
                        else:
                            print("选项已经被选中")
        return answerWebElementList




