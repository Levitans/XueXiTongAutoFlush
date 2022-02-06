# -*- encoding = utf-8 -*-
# @Time : 2022-02-06 16:08
# @Author : Levitan
# @File : multipleChoiceOfTask.py
# @Software : PyCharm

import selenium.webdriver.remote.webelement
from package.ControlWeb.Spider.questionType import MultipleChoice

class MultipleChoiceOfTask(MultipleChoice):
    def __init__(self, qType, question, answers, options, optionsWebElements):
        """
        :param qType: 题目类型（单选题，多选题）
        :param question: 题目问题
        :param answers: 查找到的题目答案
        :param options: 题目选项文字，列表类型
        :param optionsWebElements: 题目选项的WebElement对象， 列表类型
        """
        super(MultipleChoiceOfTask, self).__init__(qType, question, answers, options)
        self.__optionsWebElements: list[selenium.webdriver.remote.webelement.WebElement] = optionsWebElements

    def getAnswerWebElement(self):
        """
        :return: 将查找到的答案与题目选项相比较，返回一个包含正确选项WebElement对象的列表
        """
        answerWebElementList = []
        answer = self.getAnswer()
        options = self.getOptions()
        for i in range(len(options)):
            if options[i] in answer:
                answerWebElementList.append(self.__optionsWebElements[i])
        return answerWebElementList

"""
具有思维能力、从事社会实践和认识活动的人
======
['A .绝对精神', 'B .具有思维能力、从事社会实践和认识活动的人', 'C .人', 'D .人的意识']

进入主体的认识和实践范围的客观事物
======
['绝对精神的对象化', '客观物质世界', '人的意识的创造物', '进人主体的认识和实践范围的客观事物']

客体对于主体的满足程度与主体需求之间的关系
======
['主体对客体的物质欲望和要求', '主体对客体的能动反映', '主体对客体的改造和变革的结果', '客体对于主体的有用性和效益性']

实践是认识发展的动力
======
['实践是认识的来源', '技术推动了科学的发展', '实践是认识发展的动力', '科学进步是实践的目的']

['物质生产实践', '科学文化实践', '社会政治实践']
======
['物质生产实践', '虚拟实践', '社会政治实践', '科学文化实践']

['实践是社会关系形成的基础', '实践形成了社会生活的基本领域', '实践构成了社会发展的动力']
======
['实践是社会关系形成的基础', '实践形成了社会生活的基本领域', '实践构成了社会发展的动力', '实践是检验真理的唯一标准']
    """



