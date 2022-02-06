# -*- encoding = utf-8 -*-
# @Time : 2021-12-16 16:21
# @Author : Levitan
# @File : questionType.py
# @Software : PyCharm

# 选择题类
class MultipleChoice:
    def __init__(self, qType, question="", answer="", options=None):
        self.__type = qType
        self.__question = question
        self.__options = options
        self.__answer = answer

    def __str__(self):
        options = ""
        for i in self.__options:
            options += i + "\n"
        return self.__question + '\n' + options + '\n' + self.__answer

    def toString(self):
        options = ""
        for i in self.__options:
            options += i + "\n"
        return self.__question + '\n' + options + self.__answer

    def getType(self):
        return self.__type

    def getAnswer(self):
        return self.__answer

    def getOptions(self):
        return self.__options

# 判断题类
class TrueOrFalse:
    def __init__(self, qType, question="", answer=""):
        self.__type = qType
        self.__question = question
        self.__answer = answer

    def __str__(self):
        return self.__question + '\n' + self.__answer

    def toString(self):
        return self.__question + "\n" + self.__answer

    def getType(self):
        return self.__type

    def getAnswer(self):
        return self.__answer
