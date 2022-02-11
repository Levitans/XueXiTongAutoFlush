# -*- encoding = utf-8 -*-
# @Time : 2022-01-29 17:48
# @Author : Levitan
# @File : spider.py
# @Software : PyCharm


import time

import selenium.common.exceptions
from selenium.webdriver.common.by import By
from package.display import Display
from package.ControlWeb.xueXiTong import XueXiTong
from package.ControlWeb.task.answerQuestion.questionType import MultipleChoice
from package.ControlWeb.task.answerQuestion.questionType import TrueOrFalse


class Spider(XueXiTong):
    def __init__(self, browserPath, driverPath, browserName, user, browserKey, saveFilePath):
        super().__init__(browserPath, driverPath, browserName, user, browserKey)
        self.__driver = self.getDriver()
        self.__questionList = []
        self.DanXPath = "{}\\单选题.txt".format(saveFilePath)
        self.DuoXpath = "{}\\多选题.txt".format(saveFilePath)
        self.PanDPath = "{}\\判断题.txt".format(saveFilePath)

    def __getData(self):
        self.__driver.switch_to.frame(self.__driver.find_element(By.CSS_SELECTOR, '[id="frame_content"]'))

        # 保存所有题目的WebDriver对象
        questionList = self.__driver.find_elements(By.CSS_SELECTOR, '[class="TiMu"]')

        for i in range(len(questionList)):
            item = questionList[i]

            # 获取问题
            question = item.find_element(By.CSS_SELECTOR, '[class="Zy_TItle clearfix"]').text.replace("\n", "")
            question = question[question.find("【"):]

            # 题目类型
            questionType = question.partition("】")[0][1:]

            # 获取选项
            options = item.find_elements(By.CSS_SELECTOR, '[class="clearfix"]')
            options.pop(0)
            optionsText = []        # 保存选项文本
            for j in options:
                optionsText.append(j.text.replace("\n", ""))

            # 我的答案的标签
            py_answer_itme = item.find_element(By.CSS_SELECTOR, '[class="Py_answer clearfix"]')
            py_answerItme = py_answer_itme.text.split("\n")
            py_answer = ""
            for s in py_answerItme:
                py_answer += (s + " "*5)

            # 获取我的答案是否正确
            trueOrFalseKey = py_answer_itme.find_element(By.TAG_NAME, "i").get_attribute("class")
            if trueOrFalseKey == "fr dui":
                py_answer += "√"
            elif trueOrFalseKey == "fr cuo" or trueOrFalseKey == "fr bandui":
                py_answer += "×"

            if questionType == "判断题":
                self.__questionList.append(TrueOrFalse("判断题", question, [py_answer]))
            elif questionType == "单选题":
                self.__questionList.append(MultipleChoice("单选题", question, [py_answer], optionsText))
            elif questionType == "多选题":
                self.__questionList.append(MultipleChoice("多选题", question, [py_answer], optionsText))

    def work(self):
        # 进入课程的第一个章节
        chapterItemList = self.chapter.getChapterItemList()
        chapterItemList[0].webObj.click()
        time.sleep(2)

        # 收起目录栏
        self.__driver.find_element(By.CSS_SELECTOR, '[class="switchbtn"]').click()
        time.sleep(1)

        for i in range(self.chapter.getLength()-1):
            js = "var q=document.documentElement.scrollTop=10000"
            self.__driver.execute_script(js)
            time.sleep(1)

            # 寻找是否有选项卡
            prevTableList = []
            try:
                prevTableList = self.__driver.find_element(By.CSS_SELECTOR, '[class="prev_tab"]') \
                    .find_element(By.CSS_SELECTOR, '[class="prev_ul"]') \
                    .find_elements(By.TAG_NAME, 'li')
                print("当前课程有{}个选项卡".format(len(prevTableList)))
            except Exception:
                print("当前章节没有选项卡")

            # 如果没有找到选项卡则执行一次
            lenOfPrevTableList = len(prevTableList) if len(prevTableList) != 0 else 1
            for tableIndex in range(lenOfPrevTableList):
                if tableIndex != 0:
                    # 选项卡移动到屏幕中
                    self.__driver.execute_script("arguments[0].scrollIntoView(false);",
                                                 prevTableList[tableIndex].find_element(By.TAG_NAME, 'div'))
                    prevTableList[tableIndex].find_element(By.TAG_NAME, 'div').click()
                    time.sleep(2)

                # 进入第一层iframe
                self.__driver.switch_to.frame("iframe")
                iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
                print("当前小节有{}个任务点".format(len(iframeList)))
                for i in range(len(iframeList)):
                    print("当前为第{}个任务点".format(i + 1))
                    self.__driver.switch_to.frame(iframeList[i])
                    try:
                        self.__getData()
                        self.__writerData()
                    except selenium.common.exceptions.NoSuchElementException:
                        print("当前任务点不是题目")
                    Display.separate(10)
                    self.__driver.switch_to.default_content()
                    self.__driver.switch_to.frame("iframe")
                    iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
                self.__driver.switch_to.default_content()
                time.sleep(2)
            self.__questionList.clear()

            # 点击下一章
            time.sleep(3)
            self.__driver.find_element(By.CSS_SELECTOR, '[class="jb_btn jb_btn_92 fs14 prev_next next"]').click()

    # 写入数据
    def __writerData(self):
        f1 = open(self.DanXPath, "a", encoding="utf-8")
        f2 = open(self.DuoXpath, "a", encoding="utf-8")
        f3 = open(self.PanDPath, "a", encoding="utf-8")
        for i in self.__questionList:
            if i.getType() == "单选题":
                f1.write(i.toString() + "\n\n")
                print(i)
            elif i.getType() == "多选题":
                f2.write(i.toString() + "\n\n")
                print(i)
            elif i.getType() == "判断题":
                f3.write(i.toString() + "\n\n")
                print(i)
        f1.close()
        f2.close()
        f3.close()
        print("写入成功")
