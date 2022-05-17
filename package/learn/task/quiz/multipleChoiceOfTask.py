# -*- encoding = utf-8 -*-
# @Time : 2022-02-06 16:08
# @Author : Levitan
# @File : multipleChoiceOfTask.py
# @Software : PyCharm

import difflib
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from package.learn.task.quiz.question import MultipleChoice
from package.learn.task.interface import Answerable
from package.learn import globalvar as gl
from package.learn import color

class MultipleChoiceOfTask(MultipleChoice, Answerable):
    def __init__(self, questionWebObj, qType, question, answersList, options, optionsWebElements):
        """
        :questionWebObj: 题目整体的WebElement对象，用于定位题目位置
        :param qType: 题目类型（单选题，多选题）
        :param question: 题目问题
        :param answersList: 查找到的题目答案，list类型
        :param options: 题目选项文字，list类型
        :param optionsWebElements: 题目选项的WebElement对象， 列表类型
        """
        super(MultipleChoiceOfTask, self).__init__(qType, question, answersList, options)
        self.__optionsWebElements: list[WebElement] = optionsWebElements
        self.qWebObj = questionWebObj

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
                        # 选项是否被选中，用于多选题，多选题重复选择会取消选项
                        # isElementBeClick 为Ture表示选项被选中，False表示选项没被选中
                        try:
                            isElementBeClick = False if self.__optionsWebElements[i].find_element(By.TAG_NAME, "input").get_attribute("checked") is None else True
                        except NoSuchElementException:
                            try:
                                elementClass = self.__optionsWebElements[i].get_attribute("class")
                                isElementBeClick = True if elementClass.split(" ")[-1] == "check_answer" else False
                            except NoSuchElementException:
                                gl.exception_log_manger.writeLog(traceback.format_exc())
                                print(color.read("无法判断选项是否被选中\n默认被选中"))
                                isElementBeClick = True
                        if isElementBeClick:
                            print("选项已经被选中")
                        else:
                            answerWebElementList.append(self.__optionsWebElements[i])
        return answerWebElementList




