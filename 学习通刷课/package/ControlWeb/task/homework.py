# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 22:20
# @Author : Levitan
# @File : homework.py
# @Software : PyCharm
import getopt
from package.ControlWeb.task.getAnswer import GetAnswer
from selenium.webdriver.common.by import By

class Homework:
    def __init__(self, driver):
        self.__driver = driver
        self.__checkpoint = True

        # 进入iframe
        iframe = self.__driver.find_element(By.CSS_SELECTOR, '[id="frame_content"]')
        self.__driver.switch_to.frame(iframe)

        # 保存所有题目的WebDriver对象
        self.__questionList = self.__driver.find_elements(By.CSS_SELECTOR, '[class="Zy_TItle clearfix"]')
        print("有{}个题目".format(len(self.__questionList)))

        # 保存所题目的文字
        self.__questionTextList = []
        for i in self.__questionList:
            question = i.text.partition("\n")[-1]
            self.__questionTextList.append(question)

        # 保存所有选择题对象
        self.__optionsList = self.__driver.find_elements(By.CSS_SELECTOR, '[class="Zy_ulTop w-top fl"]')

        # 保存所有判断题选项对象
        self.__recognizedList = self.__driver.find_elements(By.CSS_SELECTOR, '[class="Zy_ulBottom clearfix"]')

        # 保存每个问题的每个选项对象
        self.__optionsObjectList = []
        choiceIndex = 0
        recognizedIndex = 0
        for i in range(len(self.__questionList)):
            courseType = self.__questionTextList[i].partition("】")[0][1:]
            # 如果题目是判断题则不保存选项的对象
            if courseType == "判断题":
                item = self.__recognizedList[recognizedIndex].find_elements(By.TAG_NAME, 'label')
                self.__optionsObjectList.append(item)
                recognizedIndex += 1
            else:
                options = self.__optionsList[choiceIndex].find_elements(By.CSS_SELECTOR, '[class="fl after"]')
                self.__optionsObjectList.append(options)
                choiceIndex += 1

        # 获取每题的选项文字
        self.__optionsTextList = []
        for i in self.__optionsObjectList:
            optionsText = []
            for j in i:
                optionsText.append(j.text)
            self.__optionsTextList.append(optionsText)

    def finish(self):
        getAnswer = GetAnswer()
        for i in range(len(self.__questionTextList)):
            print("第{}题".format(i + 1))
            courseType = self.__questionTextList[i].partition("】")[0][1:]
            answer = getAnswer.getAnswer(self.__questionTextList[i])

            # 判断是否找到答案
            if answer is None:
                self.__checkpoint = False
                continue

            if courseType == "单选题":
                # 判断单选题答案是否为str，若否则跳过此题
                if not (isinstance(answer, str)):
                    self.__checkpoint = False
                    continue
                for index in range(len(self.__optionsTextList[i])):
                    if answer == self.__optionsTextList[i][index]:
                        self.__optionsObjectList[i][index].click()
                        break

            elif courseType == "多选题":
                if not (isinstance(answer, list)):
                    self.__checkpoint = False
                    continue
                for index in range(len(answer)):
                    for optionIndex in range(len(self.__optionsTextList[i])):
                        if answer[index] == self.__optionsTextList[i][optionIndex]:
                            self.__optionsObjectList[i][optionIndex].click()

            elif courseType == "判断题":
                if not (isinstance(answer, bool)):
                    self.__checkpoint = False
                    continue
                a = 0 if answer else 1
                self.__optionsObjectList[i][a].click()
            time.sleep(2)

    def submitOrSave(self):
        if self.__checkpoint:
            self.__driver.find_element(By.CSS_SELECTOR, '[href="javascript:void(0);"][onclick="btnBlueSubmit();"]').click()
            time.sleep(1)
            self.__driver.find_element(By.CSS_SELECTOR, '[class="bluebtn "][onclick="form1submit();"]').click()
            time.sleep(1)
        else:
            self.__driver.find_element(By.CSS_SELECTOR, '[onclick="noSubmit();"]').click()
            time.sleep(1)
            self.__driver.switch_to.alert.accept()
        print("完成答题")
