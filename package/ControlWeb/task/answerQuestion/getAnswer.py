# -*- encoding = utf-8 -*-
# @Time : 2021-09-14 0:02
# @Author : Levitan
# @File : getAnswer.py
# @Software : PyCharm

import requests
import json
from package.exception import NoFoundAnswerException


class GetAnswer:
    @staticmethod
    def __API1(question):
        api = r"https://cx.icodef.com/wyn-nb"
        data = {'question': question}
        r = requests.post(url=api, data=data, timeout=10)
        dataText = r.text
        dataJson = json.loads(dataText)
        if dataJson['code'] == -1:
            return ""
        answer = dataJson['data']
        return answer

    @staticmethod
    def __API2(question):
        api = r"https://api.julym.com/class/damn.php?question="
        url = "{}{}".format(api, question)
        r = requests.get(url, timeout=10)
        dataText = r.text
        dataJson = json.loads(dataText)
        if dataJson['code'] == "0" or dataJson['code'] == 0:
            return ""
        if isinstance(dataJson['answer'], list):
            return ""
        answer = dataJson['answer'].encode().decode()
        return answer

    @staticmethod
    def __API3(question):
        api = r"https://api.gochati.cn/jsapi.php?token=cxmooc&q="
        url = "{}{}".format(api, question)
        r = requests.get(url, timeout=10)
        dataText = r.text
        dataJson = json.loads(dataText)
        answer = dataJson["da"]
        return answer

    @staticmethod
    def __API4(question):
        api = "http://api.902000.xyz:88/wkapi.php"
        # 公众号：如月的梦想
        data = {'q': question}
        r = requests.post(url=api, data=data, timeout=10)
        dataText = r.text
        dataJson = json.loads(dataText)
        if dataJson['code'] == 0:
            return ""
        answer = dataJson['answer']
        return answer

    @staticmethod
    def __requestAnswer(question):
        """
        :param question: 需要查询的问题
        :return: 若找到答案则返答案的string，若没找到答案则返回空string
        """
        answer = ""
        try:
            print("正在通过接口1查题")
            answer = GetAnswer.__API1(question)
            if answer == "":
                raise NoFoundAnswerException
        except (
                requests.exceptions.Timeout, json.JSONDecodeError, requests.exceptions.ConnectionError,
                NoFoundAnswerException):
            print("接口1查询失败")
            print("正在通过接口2查题")
            try:
                answer = GetAnswer.__API2(question)
                if answer == "":
                    raise NoFoundAnswerException
            except (requests.exceptions.Timeout, json.JSONDecodeError, NoFoundAnswerException):
                print("接口2查询失败")
                print("正在通过接口3查题")
                try:
                    answer = GetAnswer.__API3(question)
                    if answer == "":
                        raise NoFoundAnswerException
                except (requests.exceptions.Timeout, json.JSONDecodeError, NoFoundAnswerException):
                    print("接口3查询失败")
                    print("正在通过接口4查题")
                    try:
                        answer = GetAnswer.__API4(question)
                        if answer == "":
                            raise NoFoundAnswerException
                    except (requests.exceptions.Timeout, NoFoundAnswerException):
                        print("接口4查询失败")
                        print("本题无法找到答案")
        return answer

    @staticmethod
    def __parseAnswer(answer):
        separator = ("#", "\u0001")
        for i in separator:
            if i in answer:
                return answer.split(i)
        return [answer]

    @staticmethod
    def getAnswer(problem, questionType=""):
        """
        :param problem: 待搜索的题目
        :param questionType: 题目的类型，若不提供题目类型则不检测查找答案正确性
        :return: 若查找到的答案符合题目类型则将答案以列表的方式返回，否者返回None
        """
        print("正在搜索题目：{}".format(problem))
        data = GetAnswer.__requestAnswer(problem)
        answer = GetAnswer.__parseAnswer(data)
        # 没找到答案返回None
        if answer[0] == "":
            return None
        print("搜索成功答案为：{}".format(answer))
        # 验证获取的答案和题目类型是否相同
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

https://api.gochati.cn/jsapi.php?token=cxmooc&q=近平主席提出的“新时代”之“新”,是基于中国特色社会主义进入一个新的发展阶段
http://api.muketool.com/notice?script=习近平主席提出的“新时代”之“新”,是基于中国特色社会主义进入一个新的发展阶段。&version=1.0.7
https://api.julym.com/class/damn.php?question=马克思主义的社会形态理论指出( )
"""

if __name__ == "__main__":
    print(GetAnswer.getAnswer('What does “thee” mean in “Shall I compare thee to a summer’s day”'))
