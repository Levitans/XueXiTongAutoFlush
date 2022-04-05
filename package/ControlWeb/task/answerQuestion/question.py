# -*- encoding = utf-8 -*-
# @Time : 2021-12-16 16:21
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


# 选择题类
class MultipleChoice(Question):
    def __init__(self, qType: str, question="", answer: list = None, options: list = None):
        super(MultipleChoice, self).__init__(question, answer)
        self.__type = qType
        self.__options = options

    def __str__(self):
        return "[问题:" + self.getQuestion() + ",答案:" + str(self.getAnswer()) + ",类型:" + self.getType() + ",选项:" + str(
            self.getOptions()) + "]"

    def toString(self):
        info = self.getQuestion()+"\n"
        if self.getOptions() is not None:
            for i in self.getOptions():
                info += i + "\n"
        if self.getAnswer() is not None:
            for i in self.getAnswer():
                info += i + "\n"
        return info

    def getType(self):
        return self.__type

    def getOptions(self):
        return self.__options


# 判断题类
class TrueOrFalse(Question):
    def __init__(self, qType: str, question="", answer: list = None):
        super(TrueOrFalse, self).__init__(question, answer)
        self.__type = qType

    def __str__(self):
        return "[问题:" + self.getQuestion() + ",答案:" + str(self.getAnswer()) + ",类型:" + self.getType() + "]"

    def toString(self):
        return self.getType() + "\n" + self.getQuestion() + "\n" + self.getAnswer()[0]

    def getType(self):
        return self.__type
