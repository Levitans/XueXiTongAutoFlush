# -*- encoding = utf-8 -*-
# @Time : 2021-09-14 0:02
# @Author : Levitan
# @File : getAnswer.py
# @Software : PyCharm

import requests
import json


class GetAnswer:
    def __init__(self):
        self.__url = r"https://api.gochati.cn/jsapi.php?token=cxmooc&q="

    def __requestAnswer(self, problem):
        url = "{}{}".format(self.__url, problem)
        r = requests.get(url, timeout=10)
        dataText = r.text
        # print(dataText)
        dataJson = json.loads(dataText)
        data = dataJson["da"]
        return data

    @staticmethod
    def __parseAnswer(answer):
        separator = ("#", "\u0001")
        for i in separator:
            if i in answer:
                return answer.split(i)
        return [answer]

    def getAnswer(self, problem, questionType=""):
        """
        :param problem: 待搜索的题目
        :param questionType: 题目的类型，若不提供题目类型则不检测查找答案正确性
        :return: 若查找到的答案符合题目类型则将答案以列表的方式返回，否者返回None
        """
        data = self.__requestAnswer(problem)
        print("正在搜索题目：{}".format(problem))
        answer = self.__parseAnswer(data)
        print("搜索成功答案为：{}".format(answer))
        # 没找到答案返回None
        if answer == "":
            return None

        if questionType == "":
            return answer

        elif questionType == "单选题":
            if len(answer) > 1:
                return None
            return answer

        elif questionType == "多选题":
            if len(answer) == 1:
                return None
            return answer
        elif questionType == "判断题":
            if len(answer) > 1:
                return None
            data = {'√': True, '正确': True, 'T': True, 'ri': True, '是': True, '对': True,
                    '×': False, '错误': False, '错': False, 'F': False, 'wr': False, '否': False}
            for i in data.keys():
                if answer[0] == i:
                    return [data[i]]
            return None

"""
坚持保护优先,自然恢复为主#着力推进绿色发展、循环发展、低碳发展#形成节约资源和保护环境的空间格局
人与社会\u0001人与自然\u0001人与人
使生态文明建设的战略地位更加明确#使中国特色社会主义事业总体布局更加完善#深化了对党执政规律、社会主义建设规律、人类社会发展规律的认识#有利于夺取中国特色社会主义新胜利

https://api.gochati.cn/jsapi.php?token=cxmooc&q=【多选题】马克思确认社会生活在本质上是实践的,也就是把社会生活“当作实践去理解”。社会生活的实践性体现在( )
http://api.muketool.com/notice?script=习近平主席提出的“新时代”之“新”,是基于中国特色社会主义进入一个新的发展阶段。&version=1.0.7
"""

if __name__ == "__main__":
    a = GetAnswer()
    print(a.getAnswer('【单选题】实践的主体是( )'))
