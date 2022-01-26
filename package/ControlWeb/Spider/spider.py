# -*- encoding = utf-8 -*-
# @Time : 2021-12-16 16:25
# @Author : Levitan
# @File : spider.py
# @Software : PyCharm

from os import truncate
import time
from selenium.webdriver.common.by import By
from package.ControlWeb.Spider.question import MultipleChoice
from package.ControlWeb.Spider.question import TrueOrFalse

class Spyder:
    def __init__(self, driver):
        self.__driver = driver
        self.__questionList = []
        # 进入第三层iframe
        self.__driver.switch_to.frame(self.__driver.find_element(By.CSS_SELECTOR, '[id="frame_content"]'))

    def getText(self):
        # 保存所有题目的WebDriver对象
        questionList = self.__driver.find_elements(By.CSS_SELECTOR, '[class="TiMu"]')

        for i in range(len(questionList)):
            item = questionList[i]

            # 有显示真确答案用着一段获取
            """
            py_answer = item.find_element(By.CSS_SELECTOR, '[class="Py_answer clearfix"]').text.partition("我的答案")[0]
            questionAndOptions = item.find_elements(By.CSS_SELECTOR, '[class="clearfix"]')
            question = questionAndOptions[0].text

            optionsList = []
            for j in range(1, len(questionAndOptions)):
                optionsList.append(questionAndOptions[j].text.replace("\n", ""))

            courseType = question.partition("】")[0][1:]
            if courseType == "判断题":
                self.__questionList.append(TrueOrFalse("判断题", question, py_answer))
            elif courseType == "单选题":
                self.__questionList.append(MultipleChoice("单选题", question, optionsList, py_answer))
            elif courseType == "多选题":
                self.__questionList.append(MultipleChoice("多选题", question, optionsList, py_answer))
            """

            # 没有显示正确答案，只显示自己答案用这段获取

            # 我的答案的标签
            py_answer_itme = item.find_element(By.CSS_SELECTOR, '[class="Py_answer clearfix"]')
            py_answer = py_answer_itme.text

            questionAndOptions = item.find_elements(By.CSS_SELECTOR, '[class="clearfix"]')
            question = questionAndOptions[0].text

            optionsList = []
            for j in range(1, len(questionAndOptions)):
                optionsList.append(questionAndOptions[j].text.replace("\n", ""))
            
            courseType = question.partition("】")[0][1:]
            if courseType == "判断题":
                # 获取我的答案是否正确
                trueOrFalseKey = py_answer_itme.find_elements(By.TAG_NAME, "i")[-1].get_attribute("class")
                if trueOrFalseKey == "fr dui":
                    py_answer += " "*5+"√"
                elif trueOrFalseKey == "fr cuo" or trueOrFalseKey == "fr bandui":
                    py_answer += " "*5+"×"
                
                self.__questionList.append(TrueOrFalse("判断题", question, py_answer))
            else:
                # 获取我的答案是否正确
                trueOrFalseKey = py_answer_itme.find_element(By.TAG_NAME, "i").get_attribute("class")
                if trueOrFalseKey == "fr dui":
                    py_answer += " "*5+"√"
                elif trueOrFalseKey == "fr cuo" or trueOrFalseKey == "fr bandui":
                    py_answer += " "*5+"×"
                
                if courseType == "单选题":
                    self.__questionList.append(MultipleChoice("单选题", question, optionsList, py_answer))
                elif courseType == "多选题":
                    self.__questionList.append(MultipleChoice("多选题", question, optionsList, py_answer))

    def writerData(self):
        f1 = open("单选题.txt", "a", encoding="utf-8")
        f2 = open("多选题.txt", "a", encoding="utf-8")
        f3 = open("判断题.txt", "a", encoding="utf-8")
        for i in self.__questionList:
            if i.getType() == "单选题":
                f1.write(i.toString()+"\n\n")
                print(i)
            elif i.getType() == "多选题":
                f2.write(i.toString()+"\n\n")
                print(i)
            elif i.getType() == "判断题":
                f3.write(i.toString()+"\n\n")
                print(i)
        f1.close()
        f2.close()
        f3.close()
        print("写入成功")
