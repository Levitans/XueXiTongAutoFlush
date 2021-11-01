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
        r = requests.get(url)
        dataText = r.text
        dataJson = json.loads(dataText)
        data = dataJson["da"]
        return data

    def __parseAnswer(self, answer):
        separator = ("#", "\u0001")
        for i in separator:
            if answer.find(i) == -1:
                continue
            else:
                answer = answer.split(i)
                break
        return answer

    def getAnswer(self, problem):
        print("正在查找：{}".format(problem))
        data = self.__requestAnswer(problem)
        answer = self.__parseAnswer(data)
        print("答案为：{}".format(answer))
        if answer == "":
            return None

        data = {'√': True, '正确': True, 'T': True, 'ri': True, '是': True, '对': True,
                '×': False, '错误': False, '错': False, 'F': False, 'wr': False, '否': False}
        for i in data.keys():
            if answer == i:
                answer = data[i]
                break
        print("查找成功答案为：{}".format(answer))
        return answer

"""
坚持保护优先,自然恢复为主#着力推进绿色发展、循环发展、低碳发展#形成节约资源和保护环境的空间格局
人与社会\u0001人与自然\u0001人与人
使生态文明建设的战略地位更加明确#使中国特色社会主义事业总体布局更加完善#深化了对党执政规律、社会主义建设规律、人类社会发展规律的认识#有利于夺取中国特色社会主义新胜利

https://api.gochati.cn/jsapi.php?token=cxmooc&q=【判断题】习近平主席提出的“新时代”之“新”,是基于中国特色社会主义进入一个新的发展阶段。
"""