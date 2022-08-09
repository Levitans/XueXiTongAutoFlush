# -*- encoding = utf-8 -*-
# @Time : 2021-09-14 0:02
# @Author : Levitan
# @File : getanswer.py
# @Software : PyCharm
import json
from concurrent.futures import ThreadPoolExecutor

# 自定义文件
from .exception import NoFoundAnswerException

# 第三方包
from concurrent.futures._base import TimeoutError
import requests

class GetAnswer:
    __debug = False

    def __init__(self, debug=False):
        GetAnswer.__debug = debug
        self.__pool = ThreadPoolExecutor(max_workers=5)

    @staticmethod
    def __API1(question):
        api = r"https://cx.icodef.com/wyn-nb"
        data = {'question': question}
        try:
            r = requests.post(url=api, data=data, timeout=10)
        except requests.exceptions.Timeout:
            return ""
        dataText = r.text

        #   ==============显示返回内容，测试时使用=================
        if GetAnswer.__debug:
            print("API1返回内容："+dataText)

        dataJson = json.loads(dataText)
        if dataJson['code'] == -1:
            raise NoFoundAnswerException(dataJson["data"])
        answer = dataJson['data']
        return answer

    @staticmethod
    def __API2(question):
        api = r"https://api.julym.com/class/damn.php?question="
        url = "{}{}".format(api, question)
        try:
            r = requests.get(url, timeout=10)
        except requests.exceptions.Timeout:
            return ""
        dataText = r.text

        #   ==============显示返回内容，测试时使用=================
        if GetAnswer.__debug:
            print("API2返回内容："+dataText)

        dataJson = json.loads(dataText)
        if dataJson['code'] == "0" or dataJson['code'] == 0:
            raise NoFoundAnswerException(dataJson['answer'].encode().decode())
        if isinstance(dataJson['answer'], list):
            return ""
        answer = dataJson['answer'].encode().decode()
        return answer

    @staticmethod
    def __API3(question):
        api = r"https://api.gochati.cn/jsapi.php?token=cxmooc&q="
        url = "{}{}".format(api, question)
        try:
            r = requests.get(url, timeout=10)
        except requests.exceptions.Timeout:
            raise NoFoundAnswerException
        dataText = r.text

        #   ==============显示返回内容，测试时使用=================
        if GetAnswer.__debug:
            print("API3返回内容："+dataText)

        try:
            dataJson = json.loads(dataText)
        except json.decoder.JSONDecodeError:
            raise NoFoundAnswerException
        if dataJson["code"] == 0:
            return ""
        answer = dataJson["da"]
        return answer

    @staticmethod
    def __API4(question):
        api = "http://api.902000.xyz:88/wkapi.php"
        # 公众号：如月的梦想
        data = {'q': question}
        try:
            r = requests.post(url=api, data=data, timeout=10)
        except requests.exceptions.Timeout:
            return ""
        dataText = r.text

        #   ==============显示返回内容，测试时使用=================
        if GetAnswer.__debug:
            print("API4返回内容："+dataText)

        dataJson = json.loads(dataText)
        if dataJson['code'] == 0:
            raise NoFoundAnswerException(dataJson['answer'])
        answer = dataJson['answer']
        return answer

    @staticmethod
    def __API5(question):
        api = "http://118.25.10.121/moocapi?q="
        url = "{}{}".format(api, question)
        try:
            r = requests.get(url, timeout=10)
        except requests.exceptions.Timeout:
            raise NoFoundAnswerException
        dataText = r.text

        # ==============显示返回内容，测试时使用=================
        if GetAnswer.__debug:
            print("API5返回内容："+dataText)

        dataJson = json.loads(dataText)
        if dataJson["code"] == -1:
            raise NoFoundAnswerException(dataJson["msg"])
        answer = dataJson['answer']
        return answer

    def __requestAnswer(self, question, questionType):
        """
        :param question: 需要查询的问题
        :return: 若找到答案则返答案的string，若没找到答案则返回空string
        """
        answerList = []

        future1 = self.__pool.submit(GetAnswer.__API1, question)
        future2 = self.__pool.submit(GetAnswer.__API2, question)
        future3 = self.__pool.submit(GetAnswer.__API3, question)
        future4 = self.__pool.submit(GetAnswer.__API4, question)
        future5 = self.__pool.submit(GetAnswer.__API5, question)

        try:
            answer1 = future1.result(timeout=20)
            answerList.append(GetAnswer.__parseAnswer(answer1, questionType))
        except TimeoutError:
            print("线程1响应超时")
        except NoFoundAnswerException as e:
            print("线程1未找到答案，返回信息："+str(e))
        except ConnectionError:
            print("接口1连接失败")

        try:
            answer2 = future2.result(timeout=20)
            answerList.append(GetAnswer.__parseAnswer(answer2, questionType))
        except TimeoutError:
            print("线程2响应超时")
        except NoFoundAnswerException as e:
            print("线程2未找到答案，返回信息："+str(e))
        except requests.exceptions.ConnectionError:
            print("接口2连接失败")

        try:
            answer3 = future3.result(timeout=20)
            answerList.append(GetAnswer.__parseAnswer(answer3, questionType))
        except TimeoutError:
            print("线程3响应超时")
        except NoFoundAnswerException:
            print("线程3未找到答案，返回信息：None")
        except requests.exceptions.ConnectionError:
            print("接口3连接失败")

        try:
            answer4 = future4.result(timeout=20)
            answerList.append(GetAnswer.__parseAnswer(answer4, questionType))
        except TimeoutError:
            print("线程4响应超时")
        except NoFoundAnswerException as e:
            print("线程4未找到答案，返回信息："+str(e))
        except requests.exceptions.ConnectionError:
            print("接口4连接失败")

        try:
            answer5 = future5.result(timeout=20)
            answerList.append(GetAnswer.__parseAnswer(answer5, questionType))
        except TimeoutError:
            print("线程5响应超时")
        except NoFoundAnswerException as e:
            print("线程5未找到答案，返回信息："+str(e))
        except requests.exceptions.ConnectionError:
            print("接口5连接失败")
        print()
        return answerList

    @staticmethod
    def __parseAnswer(answer, questionType):
        if answer == "":
            return None
        separator = ("#", "\u0001", "\x01", "&nbsp;")
        for i in separator:
            if i in answer:
                answer = answer.split(i)
                break

        # 验证获取的答案和题目类型是否相同
        if questionType == "":
            return answer

        elif questionType == "单选题":
            if isinstance(answer, list):
                return None
            return [answer]

        elif questionType == "多选题":
            if not isinstance(answer, list):
                return None
            return answer
        elif questionType == "判断题":
            if isinstance(answer, list):
                return None
            data = {'√': True, '正确': True, 'T': True, 'ri': True, '是': True, '对': True,
                    '×': False, '错误': False, '错': False, 'F': False, 'wr': False, '否': False}
            for i in data.keys():
                if answer == i:
                    return [data[i]]
            return None

    @staticmethod
    def callback(question, answer, qType=""):
        url = "http://118.25.10.121/moocapi2?t={}&q={}&a={}".format(qType, question, answer)
        r = requests.get(url)

    def getAnswer(self, question, questionType=""):
        """
        :param question: 待搜索的题目
        :param questionType: 题目的类型，若不提供题目类型则不检测查找答案正确性
        :return: 形如[[答案1], [答案2], [答案3]]的二维列表，其中列表的元素个数在[0, 5]范围内
        """
        print("正在搜索题目：{}\n".format(question))
        answerList = self.__requestAnswer(question, questionType)
        while None in answerList:
            answerList.remove(None)
        if len(answerList) != 0:
            GetAnswer.callback(question, str(answerList[0]), questionType)
        print("找到 " + str(len(answerList)) + " 个答案")
        for i in range(len(answerList)):
            print("答案{}：{}".format(i + 1, answerList[i]))
        return answerList

    def getSingleAnswer(self, question, questionType=""):
        answerList = self.getAnswer(question, questionType)
        similarityMatrix = [[0 for j in range(len(answerList))] for i in range(len(answerList))]
        maxSimilarDiffRatio = 0
        for item1 in range(len(answerList)):
            for item2 in range(item1, len(answerList)):
                if item1 == item2:
                    continue
                similarQuestionNumber = 0
                for q1 in answerList[item1]:
                    for q2 in answerList[item2]:
                        similarDiffRatio = difflib.SequenceMatcher(None, q1, q2).quick_ratio()
                        if similarDiffRatio > 0.9:
                            similarQuestionNumber += 1
                similarityMatrix[item1][item2] = similarQuestionNumber
        print(similarityMatrix)

    def close(self):
        self.__pool.shutdown()


if __name__ == "__main__":
    getAnswer = GetAnswer(True)
    while True:
        q = input("输入题目（q退出）：")
        if q == "q":
            break
        answerList = getAnswer.getAnswer(q)
        print(answerList)
        print()

"""
资本-帝国主义列强不能灭亡和瓜分近代中国的最根本原因是(    )。
['物质是第一性的,意识是第二性的', '主观能动性的发挥,必须尊重客观规律']
['物质是第一性的,意识是第二性的', '主观能动性的发挥,必须尊重客观规律']
['物质是第一性的，意识是第二性的', '主观能动性的发挥，必须尊重客观规律']
"""
