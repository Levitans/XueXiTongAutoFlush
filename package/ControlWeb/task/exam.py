# -*- encoding = utf-8 -*-
# @Time : 2021-11-22 1:03
# @Author : Levitan
# @File : exam.py
# @Software : PyCharm

import time
from selenium.webdriver.common.by import By

class Exam:
    def __init__(self, driver):
        self.__driver = driver

    def enterExam(self):
        self.__driver.find_element(By.CSS_SELECTOR, '[class="nav_side"]') \
            .find_element(By.CSS_SELECTOR, '[class="sideCon"]') \
            .find_element(By.CSS_SELECTOR, '[class="nav-content "]') \
            .find_element(By.CSS_SELECTOR, '[dataname="ks"]').click()
        iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
        self.__driver.switch_to.frame(iframeList[-1])

        examList = self.__driver.find_element(By.CSS_SELECTOR, '[class="has-content"]')\
                                .find_element(By.CSS_SELECTOR, '[class="bottomList"]')\
                                .find_elements(By.TAG_NAME, "li")
        # examList[0].click()
        # item = self.__driver.find_element(By.CSS_SELECTOR, '[id="examDescription"]')\
        #                     .find_element(By.CSS_SELECTOR, '[class="popDiv wid440 popMove"]')\
        #                     .find_element(By.CSS_SELECTOR, '[class="popBottom"]')\
        #                     .find_element(By.CSS_SELECTOR, '[class="jb_btn jb_btn_92 fr fs14"]')
        #
        #
        # time.sleep(1)
        # self.__driver.find_element(By.CSS_SELECTOR, '[id="confirmEnterWin"]')\
        #              .find_element(By.CSS_SELECTOR, '[class="popDiv wid440 popMove"]')\
        #              .find_element(By.CSS_SELECTOR, '[class="popBottom"]')\
        #              .find_element(By.CSS_SELECTOR, '[onclick="confirmEnterAction()"]').click()
        input()
        headLes = self.__driver.window_handles
        self.__driver.switch_to.window(headLes[2])

        input("进入整卷浏览")

        # self.__driver.find_element(By.CSS_SELECTOR, '[class="subNav"]')\
        #              .find_element(By.CSS_SELECTOR, '[class="sub-button fr"]').click()
        #
        # time.sleep(1)
        # js = "var q=document.documentElement.scrollTop=100000"
        # self.__driver.execute_script(js)
        # time.sleep(1)

    def crawlQuestions(self):
        markTableList = self.__driver.find_element(By.CSS_SELECTOR, '[class="fanyaMarking TiMu"]')\
                                     .find_element(By.CSS_SELECTOR, '[class="fanyaMarking_left whiteBg minHet600"]')\
                                     .find_elements(By.CSS_SELECTOR, '[class="mark_table"]')

        singList = []
        for i in range(1, 112):
            item = markTableList[0].find_element(By.CSS_SELECTOR, '[class="whiteDiv"]')\
                                   .find_element(By.CSS_SELECTOR, '[data="{}"]'.format(882427896+i))
            singList.append(item)

        print("有单选题：{}".format(len(singList)))
        f = open(r"F:\python项目\学习通刷课2\单选题.txt", 'w', encoding="utf-8")
        for i in range(len(singList)):
            markName = singList[i].find_element(By.CSS_SELECTOR, '[class="mark_name colorDeep"]').text
            f.write(markName+"\n")
            print(markName)
            stemAnswerList = singList[i].find_element(By.TAG_NAME, 'form')\
                                        .find_element(By.CSS_SELECTOR, '[class="stem_answer"]')\
                                        .find_elements(By.CSS_SELECTOR, '[class="clearfix answerBg"]')
            for j in range(len(stemAnswerList)):
                string = stemAnswerList[j].text
                x = string.split("\n")
                string = x[0]+"、"+x[1]
                f.write(string+"\n")
                print(string)
            f.write("\n")
            print()
        f.close()

        """
        抓取填空题
        """
        fillBlankList = []
        for i in range(1, 60):
            item = markTableList[1].find_element(By.CSS_SELECTOR, '[class="whiteDiv"]')\
                                   .find_element(By.CSS_SELECTOR, '[data="{}"]'.format(882428007+i))
            fillBlankList.append(item)

        print("有填空题：{}".format(len(fillBlankList)))
        f = open(r"F:\python项目\学习通刷课2\填空题.txt", 'w', encoding="utf-8")
        for i in range(len(fillBlankList)):
            markName = fillBlankList[i].find_element(By.CSS_SELECTOR, '[class="mark_name colorDeep"]').text
            f.write(markName+"\n\n")
            print(markName)
        f.close()

        """
        抓取简答题
        """
        shortAnswerList = []
        for i in range(1, 12):
            item = markTableList[2].find_element(By.CSS_SELECTOR, '[class="whiteDiv"]')\
                                   .find_element(By.CSS_SELECTOR, '[data="{}"]'.format(882428066+i))
            shortAnswerList.append(item)

        print("有简答题：{}".format(len(shortAnswerList)))
        f = open(r"F:\python项目\学习通刷课2\简答题.txt", 'w', encoding="utf-8")
        for i in range(len(shortAnswerList)):
            markName = shortAnswerList[i].find_element(By.CSS_SELECTOR, '[class="mark_name colorDeep"]').text
            f.write(markName+"\n\n")
            print(markName)
        f.close()