# -*- encoding = utf-8 -*-
# @Time : 2021-12-16 16:21
# @Author : Levitan
# @File : question.py
# @Software : PyCharm


class MultipleChoice:
    def __init__(self, qType, problem="", options=None, answer=""):
        self.__type = qType
        self.__problem = problem
        self.__options = options
        self.__answer = answer

    def __str__(self):
        options = ""
        for i in self.__options:
            options += i + "\n"
        return self.__problem + '\n' + options + '\n' + self.__answer

    def toString(self):
        options = ""
        for i in self.__options:
            options += i + "\n"
        return self.__problem + '\n' + options + self.__answer

    def getType(self):
        return self.__type


class TrueOrFalse:
    def __init__(self, qType, problem="", answer=""):
        self.__type = qType
        self.__problem = problem
        self.__answer = answer

    def __str__(self):
        return self.__problem + '\n' + self.__answer

    def toString(self):
        return self.__problem + "\n" + self.__answer

    def getType(self):
        return self.__type
