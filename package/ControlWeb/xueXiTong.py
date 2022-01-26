# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 13:17
# @Author : Levitan
# @File : xueXiTong.py
# @Software : PyCharm
import time
import sys
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from package.display import Display                         # **************************************
from package.ControlWeb import course
from package.ControlWeb.task.getAnswer import GetAnswer
from package.ControlWeb.task.PPT import PPT
from package.ControlWeb.task.video import Video
from package.ControlWeb.task.homework import Homework
from package.ControlWeb.task.exam import Exam
from package.ControlWeb.Spider.spider import Spyder

class XueXiTong:
    def __init__(self, chromePath, driverPath, user, browserKey):
        """
        :param chromePath:  Chrome浏览器的地址
        :param driverPath:  Chrome浏览器的driver地址
        :param user:        User对象
        :param browserKey:  标记是否显示浏览器
        """
        self.__user = user
        self.__driverPath = driverPath

        if browserKey == 0:
            # 显示浏览器
            option = webdriver.ChromeOptions()
            option.binary_location = chromePath
            option.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.__driver = webdriver.Chrome(executable_path=self.__driverPath, options=option)
            self.__driver.maximize_window()
        else:
            # 不显示浏览器
            option = webdriver.ChromeOptions()
            option.binary_location = chromePath
            option.add_argument('headless')             # 浏览器不提供可视化界面
            option.add_argument('--mute-audion')        # 浏览器静音播放
            option.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.__driver = webdriver.Chrome(executable_path=self.__driverPath, options=option)

        # 实例化章节对象
        self.__chapter = course.Chapter()

        # 实例化课程类
        # 课程类可被外部访问
        self.course = course.Course()

    # 登陆学习通
    def landing(self):
        self.__driver.get("http://i.chaoxing.com")
        account = self.__driver.find_element(By.ID, "phone")
        account.send_keys(self.__user.getUserAccount())
        password = self.__driver.find_element(By.ID, "pwd")
        password.send_keys(self.__user.getUserPassword())
        self.__driver.find_element(By.ID, "loginBtn").click()
        time.sleep(3)

    # 获取页面中的课程
    def getCourses(self):
        self.course.getCourseObjectAndName(self.__driver)
        return self.course.getCourseNameList()

    # 进入课程
    def enterCourse(self, courseIndex):
        item = self.course.getCourseObjectList()[courseIndex]
        self.__driver.execute_script("arguments[0].focus();", item)
        try:
            item.click()
        except selenium.common.exceptions.WebDriverException:
            Display.separate()
            print("当前课程无法关闭浏览器学习")
            print("修改浏览器设置后可再次进行尝试")
            print("作者正在疯狂解决问题")
            Display.separate()
            sys.exit(1)
        # 保存课程名
        self.course.nowCourseName = self.course.getCourseNameList()[courseIndex]

        # 切换浏览器窗口
        headLes = self.__driver.window_handles
        self.__driver.switch_to.window(headLes[1])
        time.sleep(1)

        # 测试中发现不同电脑打开学习通章节元素的dataname值不同
        try:
            self.__driver.find_element(By.CSS_SELECTOR, '[class="nav_side"]')\
                         .find_element(By.CSS_SELECTOR, '[class="sideCon"]')\
                         .find_element(By.CSS_SELECTOR, '[class="nav-content "]')\
                         .find_element(By.CSS_SELECTOR, '[dataname="zj-stu"]').click()
        except Exception:
            self.__driver.find_element(By.CSS_SELECTOR, '[class="nav_side"]')\
                         .find_element(By.CSS_SELECTOR, '[class="sideCon"]')\
                         .find_element(By.CSS_SELECTOR, '[class="nav-content "]')\
                         .find_element(By.CSS_SELECTOR, '[dataname="zj"]').click()
        # 获取章节
        self.__chapter.getChapterObjectAndName(self.__driver)
        return self.__chapter.getChaptersNameList()

    def automaticLearning(self, chapterIndex, subjectData):
        self.__chapter.getChapterObjectList()[chapterIndex].click()
        time.sleep(2)

        # 切换到第三个窗口
        # 新版学习通进入章节后会切换窗口
        head_les = self.__driver.window_handles
        self.__driver.switch_to.window(head_les[2])
        time.sleep(1)

        # 收起目录栏
        self.__driver.find_element(By.CSS_SELECTOR, '[class="switchbtn"]').click()
        time.sleep(1)

        # 循环当前课程的所有章节
        while chapterIndex < self.__chapter.getLength():
            js = "var q=document.documentElement.scrollTop=10000"
            self.__driver.execute_script(js)
            time.sleep(1)

            # 寻找是否有选项卡
            prevTableList = []
            try:
                prevTableList = self.__driver.find_element(By.CSS_SELECTOR, '[class="prev_tab"]')\
                                    .find_element(By.CSS_SELECTOR, '[class="prev_ul"]')\
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
                    time.sleep(1)
                # 进入第一层iframe
                self.__driver.switch_to.frame("iframe")
                iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
                print("当前小节有{}个任务点".format(len(iframeList)))
                for i in range(len(iframeList)):
                    print("当前为第{}个任务点".format(i+1))
                    self.__driver.switch_to.frame(iframeList[i])
                    try:
                        print("尝试视频打开任务点")
                        video = Video(self.__driver)
                        video.finish()
                    except Exception:
                        print("当前任务点不是视频")
                        try:
                            print("尝试ppt打开任务点")
                            powerPoint = PPT(self.__driver)
                            powerPoint.finish()
                        except Exception:
                            print("当前任务点不是ppt")
                            homework = Homework(self.__driver)
                            homework.finish()
                            homework.submitOrSave()
                            try:
                                print("尝试答题打开任务点")
                                homework = Homework(self.__driver)
                                homework.finish()
                                homework.submitOrSave()
                            except Exception:
                                print("当前任务点不是题目\n当前任务点无法解决，跳过当前任务点")
                    Display.separate()
                    self.__driver.switch_to.default_content()
                    self.__driver.switch_to.frame("iframe")
                    iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
                self.__driver.switch_to.default_content()
                time.sleep(2)

            # 保存进度
            subjectData.modifyClassData(self.__user.getUserName(),
                                        self.course.nowCourseName,
                                        self.__chapter.getChaptersNameList()[chapterIndex])

            print("课程第{}节完成".format(self.__chapter.getChaptersNameList()[chapterIndex]))
            chapterIndex += 1

            # 点击下一章
            self.__driver.find_element(By.CSS_SELECTOR, '[class="jb_btn jb_btn_92 fs14 prev_next next"]').click()
        print("当前章节以全部完成")

    def crawlData(self):
        self.__chapter.getChapterObjectList()[0].click()
        time.sleep(2)

        # 切换到第三个窗口
        # 新版学习通进入章节后会切换窗口
        head_les = self.__driver.window_handles
        self.__driver.switch_to.window(head_les[2])
        time.sleep(1)

        # 收起目录栏
        self.__driver.find_element(By.CSS_SELECTOR, '[class="switchbtn"]').click()
        time.sleep(1)

        for i in range(self.__chapter.getLength()):
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
                    time.sleep(1)

                # self.__driver.execute_script("arguments[0].scrollIntoView(false);",
                #                              prevTableList[1].find_element(By.TAG_NAME, 'div'))
                # prevTableList[1].find_element(By.TAG_NAME, 'div').click()
                # time.sleep(1)

                # 进入第一层iframe
                self.__driver.switch_to.frame("iframe")
                iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
                print("当前小节有{}个任务点".format(len(iframeList)))
                for i in range(len(iframeList)):
                    print("当前为第{}个任务点".format(i + 1))
                    self.__driver.switch_to.frame(iframeList[i])
                    #
                    #
                    # spyder = Spyder(self.__driver)
                    # spyder.getText()
                    # spyder.writerData()
                    try:
                        spyder = Spyder(self.__driver)
                        spyder.getText()
                        spyder.writerData()
                    except Exception:
                        print("当前任务点不是题目")
                    self.__driver.switch_to.default_content()
                    self.__driver.switch_to.frame("iframe")
                    iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
                self.__driver.switch_to.default_content()
                time.sleep(2)

            # 点击下一章
            time.sleep(3)
            self.__driver.find_element(By.CSS_SELECTOR, '[class="jb_btn jb_btn_92 fs14 prev_next next"]').click()
