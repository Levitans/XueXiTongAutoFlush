# -*- encoding = utf-8 -*-
# @Time : 2022-02-06 16:08
# @Author : Levitan
# @File : multipleChoiceOfTask.py
# @Software : PyCharm

import difflib
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from package.ControlWeb.task.answerQuestion.questionType import MultipleChoice
from package.ControlWeb.task.answerQuestion.answerable import Answerable

class MultipleChoiceOfTask(MultipleChoice, Answerable):
    def __init__(self, qType, question, answers, options, optionsWebElements):
        """
        :param qType: 题目类型（单选题，多选题）
        :param question: 题目问题
        :param answers: 查找到的题目答案，list类型
        :param options: 题目选项文字，list类型
        :param optionsWebElements: 题目选项的WebElement对象， 列表类型
        """
        super(MultipleChoiceOfTask, self).__init__(qType, question, answers, options)
        self.__optionsWebElements: list[WebElement] = optionsWebElements

    def getAnswerWebElement(self):
        """
        :return: 将查找到的答案与题目选项相比较，返回一个包含正确选项WebElement对象的列表
        """
        answerWebElementList = []
        answer = self.getAnswer()
        options = self.getOptions()
        for i in range(len(options)):
            for j in range(len(answer)):
                similarDiffRatio = difflib.SequenceMatcher(None, options[i], answer[j]).quick_ratio()
                # print("{}和{}的匹配率为：{}".format(options[i], answer[j], similarDiffRatio))
                if similarDiffRatio > 0.88:
                    inputTge = self.__optionsWebElements[i].find_element(By.TAG_NAME, "input")
                    if not inputTge.is_selected():
                        answerWebElementList.append(self.__optionsWebElements[i])
                    else:
                        print("选项已经被选中")
        return answerWebElementList




