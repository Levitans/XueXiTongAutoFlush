# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 13:17
# @Author : Levitan
# @File : xueXiTong.py
# @Software : PyCharm
import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from package.display import Display
from package.ControlWeb.school import *
from package.ControlWeb.task.PPT import PPT
from package.ControlWeb.task.video import Video
from package.ControlWeb.task.answerQuestion.homework import Homework
from package.exception import AtOrPdException, BrowseOrDriverPathException


class XueXiTong:
    def __init__(self, browserPath, driverPath, browserName, user, browserKey):
        """
        :param browserPath:  Chrome浏览器的地址
        :param driverPath:  Chrome浏览器的driver地址
        :param user:        User对象
        :param browserKey:  标记是否显示浏览器
        """
        self.__user = user
        self.__driver = self.__setDriver(browserPath, driverPath, browserName, browserKey)
        self.__school = self.__setSchool()

    # 设置webDriver
    @staticmethod
    def __setDriver(browserPath, driverPath, browserName, browserKey):
        try:
            if browserName == 'chrome':
                option = webdriver.ChromeOptions()
                option.binary_location = browserPath
                option.add_experimental_option('excludeSwitches', ['enable-logging'])
                # 不显示浏览器
                if browserKey == 1:
                    option.add_argument('headless')  # 浏览器不提供可视化界面
                    option.add_argument('--mute-audion')  # 浏览器静音播放

                driver = webdriver.Chrome(executable_path=driverPath, options=option)
            elif browserName == 'firefox':
                option = webdriver.FirefoxOptions()
                option.binary_location = browserPath
                # 不显示浏览器
                if browserKey == 1:
                    options.add_argument('--headless')
                    options.add_argument('--disable-gpu')
                driver = webdriver.Firefox(executable_path=driverPath, options=option)
            else:
                raise BrowseOrDriverPathException(browserPath, driverPath)
        except selenium.common.exceptions.WebDriverException:
            raise BrowseOrDriverPathException(browserPath, driverPath)
        return driver

    # 设置学校
    def __setSchool(self) -> Learnable:
        return Fuist(self.__driver)

    def closeDriver(self):
        self.__driver.quit()

    def getDriver(self):
        return self.__driver

    # 登陆学习通
    def logging(self):
        self.__driver.get("http://i.chaoxing.com")
        account = self.__driver.find_element(By.ID, "phone")
        account.send_keys(self.__user.getAccount())
        password = self.__driver.find_element(By.ID, "pwd")
        password.send_keys(self.__user.getPassword())
        self.__driver.find_element(By.ID, "loginBtn").click()
        time.sleep(0.5)
        try:
            loggingTest = self.__driver.find_element(By.CSS_SELECTOR, '[class="err-tip"]').text
            if loggingTest == "手机号或密码错误":
                self.closeDriver()
                raise AtOrPdException()
        except selenium.common.exceptions.NoSuchElementException:
            pass
        time.sleep(3)

    def getCourses(self):
        return self.__school.getCourses()

    def enterCourse(self, course):
        self.__school.enterCourse(course)

    def work(self):
        # 获取页面章节
        self.__school.clickChapter()
        time.sleep(1)
        chapterList = self.__school.getChapter()

        # 找到没有完成的章节
        chapterIndex = 0

        print("查找未完成的章节")
        # 跳过以完成的章节
        for i in chapterList:
            if i.isFinish:
                print("《{}》已完成".format(i.name))
                chapterIndex += 1
            else:
                print("《{}》未完成".format(i.name))
                break
            time.sleep(0.2)
        if chapterIndex == len(chapterList):  # 如果当前课程已完成则跳过
            print("当前章节以全部完成")
            return

        Display.separate()

        # 点击进入章节
        chapterList[chapterIndex].webElement.click()
        time.sleep(1)

        # # 切换到第三个窗口
        # # 新版学习通进入章节后会切换窗口
        # head_les = self.__driver.window_handles
        # self.__driver.switch_to.window(head_les[2])

        # 收起目录栏
        self.__driver.find_element(By.CSS_SELECTOR, '[class="switchbtn"]').click()
        time.sleep(1)

        # 循环当前课程的所有章节
        while chapterIndex < len(chapterList):
            js = "var q=document.documentElement.scrollTop=10000"
            self.__driver.execute_script(js)
            time.sleep(1)

            print("当前章节为{}".format(chapterList[chapterIndex].name))

            # 寻找是否有选项卡
            prevTableList = []
            try:
                prevTableList = self.__driver.find_element(By.CSS_SELECTOR, '[class="prev_tab"]') \
                    .find_element(By.CSS_SELECTOR, '[class="prev_ul"]') \
                    .find_elements(By.TAG_NAME, 'li')
                print("当前课程有{}个选项卡".format(len(prevTableList)))
            except selenium.common.exceptions.NoSuchElementException:
                print("当前章节没有选项卡")

            # 如果没有找到选项卡则执行一次
            lenOfPrevTableList = len(prevTableList) if len(prevTableList) != 0 else 1

            # 如果当前章节以完成则跳过当前章节
            # 当前学习通点击下一章节是跳到下一个选项卡，不是跳到下一章节
            if chapterList[chapterIndex].isFinish:
                for i in range(lenOfPrevTableList):
                    self.__driver.find_element(By.CSS_SELECTOR,
                                               '[class="jb_btn jb_btn_92 fs14 prev_next next"]').click()
                    time.sleep(2)
                chapterIndex += 1
                continue

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

                    # 检测任务点是是否完成
                    try:
                        self.__driver.find_element(By.CSS_SELECTOR, '[class="ans-attach-ct ans-job-finished"]')
                        print("当前任务点已完成")
                        continue
                    except selenium.common.exceptions.NoSuchElementException:
                        pass

                    # 判断是否为视频任务点
                    if iframeList[i].get_attribute("class") == 'ans-attach-online ans-insertvideo-online':
                        self.__driver.switch_to.frame(iframeList[i])
                        print("当前任务点是视频")
                        Video.finish(self.__driver)
                        print("视频任务点完成")
                    elif iframeList[i].get_attribute("class") == "ans-attach-online insertdoc-online-pdf":
                        self.__driver.switch_to.frame(iframeList[i])
                        print("当前任务点是ppt")
                        PPT.finish(self.__driver)
                        print("PPT任务点完成")
                    else:
                        self.__driver.switch_to.frame(iframeList[i])
                        try:
                            homework = Homework(self.__driver)
                            homework.getData()
                            homework.finish()
                            homework.submitOrSave()
                            print("测验任务点完成")
                        except selenium.common.exceptions.NoSuchElementException:
                            print("当前任务点无法完成")
                    Display.separate()
                    self.__driver.switch_to.default_content()
                    self.__driver.switch_to.frame("iframe")
                    iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
                self.__driver.switch_to.default_content()
                time.sleep(2)
            print("课程第{}节完成".format(chapterList[chapterIndex].name))
            Display.separate()
            self.__driver.find_element(By.CSS_SELECTOR, '[class="jb_btn jb_btn_92 fs14 prev_next next"]').click()
            chapterIndex += 1
        print("当前章节以全部完成")
