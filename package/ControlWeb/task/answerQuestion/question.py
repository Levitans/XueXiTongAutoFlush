# -*- encoding = utf-8 -*-
# @Time : 2022-02-07 12:32
# @Author : Levitan
# @File : question.py
# @Software : PyCharm

class Question:
    def __init__(self, question: str, answer: list):
        self.__question = question
        self.__answer = answer

    def __str__(self):
        return "[问题:"+self.getQuestion()+",答案:"+str(self.getAnswer())+"]"

    def getQuestion(self): return self.__question

    def getAnswer(self): return self.__answer
