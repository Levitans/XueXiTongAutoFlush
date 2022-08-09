# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 22:20
# @Author : Levitan
# @File : homework.py
# @Software : PyCharm
import time
import random

from ..interface import Task, Answerable
from .getanswer import GetAnswer
from .multipleChoiceOfTask import MultipleChoiceOfTask
from .trueOrFalseOfTask import TrueOrFalseOfTask
from .no_secret import DecodeSecret

# 导入全局变量
from package.learn.globalvar import decode_secret_status, quiz_get_answer_speed_min, quiz_get_answer_speed_max, \
    quiz_click_speed_min, quiz_click_speed_max, color, spliter

# 第三方库
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class QuizOfTask(Task):
    def __init__(self, driver):
        super().__init__(driver)
        self.__name__ = "答题"
        self.__questionList: list[Answerable] = []
    
    def isCurrentTask(self, iframeIndex) -> bool:
        # 还没找到判断任务点是否为答题的方法，所以直接返回True
        return True

    def __getData(self):
        # 进入iframe
        iframe = self._Task__driver.find_element(By.CSS_SELECTOR, '[id="frame_content"]')
        self._Task__driver.switch_to.frame(iframe)

        # 实例化 DecodeSecret 类
        decodeSecret = DecodeSecret(decode_secret_status)
        if decode_secret_status == 0:
            print(color.yellow("不启用字体解密"))
        elif decode_secret_status == 1:
            print(color.yellow("启用字体解密"))
        elif decode_secret_status == 2:
            print(color.yellow("程序自动判断是是否需要字体解密"))
        decodeSecret.getFontFace(self._Task__driver)

        # 获取页面中的所有题目
        questionList = self._Task__driver.find_elements(By.CSS_SELECTOR, '[class="TiMu"]')
        print("当前页面共有{}题".format(len(questionList)))

        myGetAnswer = GetAnswer()
        for i in range(len(questionList)):
            spliter.print()
            item = questionList[i]
            title = decodeSecret.decode(item.find_element(By.CSS_SELECTOR, '[class="Zy_TItle clearfix"]').text.replace("\n", ""))
            # 获取问题
            question = title[title.find("】")+1:]

            # 题目类型
            questionType = title[title.find("【")+1: title.find("】")]

            # 判断题目能否解决
            if questionType not in ("单选题", "多选题", "判断题"):
                print(color.blue("程序能回答的题有：单选题、多选题、判断题"))
                print(color.blue("本题类型为：" + questionType))
                print(color.blue("跳过该题"))
                continue
            # 获取问题答案
            answerList = myGetAnswer.getAnswer(question, questionType)
            # 判断是否找到答案
            if answerList is None or len(answerList) == 0:
                continue
            if questionType in ("单选题", "多选题"):
                # 获取题目选项的WebElement对象
                # optionWebElementList = item.find_elements(By.CSS_SELECTOR, '[class="fl after"]')
                optionWebElementList = item.find_elements(By.TAG_NAME, 'li')
                # 获取题目选项
                optionTextList = []
                for option in optionWebElementList:
                    """
                    说明变更时间：===========2022-05-14===========
                    目前发现，在课程章节里的答题任务点中，单选和多选题目类型的选项标签中有以下三个class值
                    
                        class="fl after"
                        class="font-cxsecret fl after"
                        class="fl before"
                    
                    学习通的作业页面中的答题任务和章节中的答题任务差异非常大，所以目前 quiz 模块无直接用于作业功能
                    """
                    try:
                        rawData = option.find_element(By.CSS_SELECTOR, '[class="fl after"]').text.replace("\n", "")
                        optionTextList.append(decodeSecret.decode(rawData))
                    except NoSuchElementException:
                        try:
                            rawData = option.find_element(By.CSS_SELECTOR, '[class="font-cxsecret fl after"]').text.replace("\n", "")
                            optionTextList.append(decodeSecret.decode(rawData))
                        except NoSuchElementException:
                            try:
                                rawData = option.find_element(By.CSS_SELECTOR, '[class="fl before"]').text.replace("\n", "")
                                optionTextList.append(decodeSecret.decode(rawData))
                            except NoSuchElementException:
                                raise NoSuchElementException('题目的选项的class不在 ["fl after", "font-cxsecret fl after", "fl before"] 中，系统无法获取题目选项')
                self.__questionList.append(
                    MultipleChoiceOfTask(item, questionType, question, answerList, optionTextList, optionWebElementList))
            elif questionType == "判断题":
                answerWebElementList = item.find_elements(By.TAG_NAME, "label")
                self.__questionList.append(TrueOrFalseOfTask(item, questionType, question, answerList[0], answerWebElementList))
            else:
                print(color.read("当前题目类型程序无法判断"))
                print(color.read("题目类型："+questionType))
                print(color.read("题目内容："+question))
                print(color.read("跳过该题目"))
            time.sleep(random.randint(quiz_get_answer_speed_min, quiz_get_answer_speed_max))        # 防止访问接口频率过高被判断为爬虫
        myGetAnswer.close()

    def finish(self):
        self.__getData()
        for i in range(len(self.__questionList)):
            print("正在完成第{}题".format(i+1))
            webElementList = self.__questionList[i].getAnswerWebElement()
            if len(webElementList) == 0:
                print("查找答案和选项答案不匹配")
                continue
            for answerWebElement in webElementList:
                self._Task__driver.execute_script("arguments[0].scrollIntoView();", self.__questionList[i].qWebObj)
                time.sleep(1)
                answerWebElement.click()
            time.sleep(random.randint(quiz_click_speed_min, quiz_get_answer_speed_max))
        self.__submitOrSave()

    def __submitOrSave(self):
        # 暂时不启用判断是否提交
        # 现在都是点击保存，程序不会主动提交
        # if self.__checkpoint:
        #     self._Task__driver.find_element(By.CSS_SELECTOR, '[href="javascript:void(0);"][onclick="btnBlueSubmit();"]').click()
        #     time.sleep(1)
        #     try:
        #         self._Task__driver.find_element(By.CSS_SELECTOR, '[class="bluebtn "][onclick="form1submit();"]').click()
        #     except Exception:
        #         self._Task__driver.find_element(By.CSS_SELECTOR, '[class="bluebtn "][onclick="submitCheckTimes();"]').click()
        #     time.sleep(1)
        # else:
        #     self._Task__driver.find_element(By.CSS_SELECTOR, '[onclick="noSubmit();"]').click()
        #     time.sleep(1)
        #     self._Task__driver.switch_to.alert.accept()
        self._Task__driver.find_element(By.CSS_SELECTOR, '[onclick="noSubmit();"]').click()
        time.sleep(1)
        self._Task__driver.switch_to.alert.accept()

