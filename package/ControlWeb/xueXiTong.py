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
from package.ControlWeb.course import Course
from package.ControlWeb.chapter import Chapter
from package.ControlWeb.task.PPT import PPT
from package.ControlWeb.task.video import Video
from package.ControlWeb.task.answerQuestion.homework import Homework
from package.exception.atOrPdException import AtOrPdException
from package.exception.browseOrDriverPathException import BrowseOrDriverPathException

class XueXiTong:
    def __init__(self, browserPath, driverPath, browserName, user, browserKey):
        """
        :param browserPath:  Chrome浏览器的地址
        :param driverPath:  Chrome浏览器的driver地址
        :param user:        User对象
        :param browserKey:  标记是否显示浏览器
        """
        self.__user = user
        self.__driverPath = driverPath

        try:
            if browserName == 'chrome':
                option = webdriver.ChromeOptions()
                option.binary_location = browserPath
                option.add_experimental_option('excludeSwitches', ['enable-logging'])
                # 不显示浏览器
                if browserKey == 1:
                    option.add_argument('headless')  # 浏览器不提供可视化界面
                    option.add_argument('--mute-audion')  # 浏览器静音播放

                self.__driver = webdriver.Chrome(executable_path=self.__driverPath, options=option)
            elif browserName == 'firefox':
                option = webdriver.FirefoxOptions()
                option.binary_location = browserPath
                # 不显示浏览器
                if browserKey == 1:
                    option.add_argument('headless')  # 浏览器不提供可视化界面
                    option.add_argument('--mute-audion')  # 浏览器静音播放
                self.__driver = webdriver.Firefox(executable_path=self.__driverPath, options=option)
            elif browserName == 'Edge':
                pass
        except selenium.common.exceptions.WebDriverException:
            raise BrowseOrDriverPathException(browserPath, driverPath)

        # 实例化章节对象
        self.chapter = Chapter()

        # 实例化课程类
        # 课程类可被外部访问
        self.course = Course()

    def closeDriver(self):
        self.__driver.quit()

    def getDriver(self):
        return self.__driver

    # 登陆学习通
    def logging(self):
        self.__driver.get("http://i.chaoxing.com")
        account = self.__driver.find_element(By.ID, "phone")
        account.send_keys(self.__user.getUserAccount())
        password = self.__driver.find_element(By.ID, "pwd")
        password.send_keys(self.__user.getUserPassword())
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

    # 获取页面中的课程
    def getCourses(self):
        self.course.getCourseObjectAndName(self.__driver)
        return self.course.getCourseNameList()

    # 进入课程
    def enterCourse(self, courseIndex):
        item = self.course.getCourseObjectList()[courseIndex]
        self.__driver.execute_script("arguments[0].focus();", item)
        time.sleep(1)

        # 防止浮动层阻挡点击
        if courseIndex >= 3:
            self.__driver.switch_to.default_content()
            self.__driver.execute_script("window.scrollBy(0,100)")
            self.__driver.switch_to.frame("frame_content")

        item.click()
        # 保存课程名
        self.course.nowCourseName = self.course.getCourseNameList()[courseIndex]

        # 切换浏览器窗口
        headLes = self.__driver.window_handles
        self.__driver.switch_to.window(headLes[1])
        time.sleep(3)

        # 测试中发现不同电脑打开学习通章节元素的dataname值不同
        try:
            self.__driver.find_element(By.CSS_SELECTOR, '[class="nav_side"]') \
                .find_element(By.CSS_SELECTOR, '[class="sideCon"]') \
                .find_element(By.CSS_SELECTOR, '[class="nav-content "]') \
                .find_element(By.CSS_SELECTOR, '[dataname="zj-stu"]').click()
        except Exception:
            self.__driver.find_element(By.CSS_SELECTOR, '[class="nav_side"]') \
                .find_element(By.CSS_SELECTOR, '[class="sideCon"]') \
                .find_element(By.CSS_SELECTOR, '[class="nav-content "]') \
                .find_element(By.CSS_SELECTOR, '[dataname="zj"]').click()
        # 获取章节
        self.chapter.getChapterItem(self.__driver)

    def work(self):
        # 找到没有完成的章节
        chapterItemList = self.chapter.getChapterItemList()
        chapterItemIndex = 0

        print("查找未完成的章节")
        # 跳过以完成的章节
        for i in chapterItemList:
            if i.isFinish:
                print("《{}{}》已完成".format(i.number, i.name))
                chapterItemIndex += 1
            else:
                print("《{}{}》未完成".format(i.number, i.name))
                break
            time.sleep(0.2)
        if chapterItemIndex == self.chapter.getLength():    # 如果当前课程已完成则跳过
            print("当前章节以全部完成")
            return

        Display.separate()
        # chapterItemList[chapterItemIndex].webObj.click()
        chapterItemList[20].webObj.click()

        # # 切换到第三个窗口
        # # 新版学习通进入章节后会切换窗口
        # head_les = self.__driver.window_handles
        # self.__driver.switch_to.window(head_les[2])
        # time.sleep(1)

        # 收起目录栏
        self.__driver.find_element(By.CSS_SELECTOR, '[class="switchbtn"]').click()
        time.sleep(1)

        # 循环当前课程的所有章节
        while chapterItemIndex < self.chapter.getLength():
            js = "var q=document.documentElement.scrollTop=10000"
            self.__driver.execute_script(js)
            time.sleep(1)

            print("当前章节为{}{}".format(chapterItemList[chapterItemIndex].number, chapterItemList[chapterItemIndex].name))

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

            # 如果当前章节以完成则跳过当前章节
            # 当前学习通点击下一章节是跳到下一个选项卡，不是跳到下一章节
            if chapterItemList[chapterItemIndex].isFinish:
                for i in range(lenOfPrevTableList):
                    self.__driver.find_element(By.CSS_SELECTOR, '[class="jb_btn jb_btn_92 fs14 prev_next next"]').click()
                    time.sleep(2)
                chapterItemIndex += 1
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
                            try:
                                print("尝试答题打开任务点")
                                homework = Homework(self.__driver)
                                homework.getData()
                                homework.finish()
                                input("暂停")
                                homework.submitOrSave()
                            except Exception:
                                print("当前任务点不是题目\n当前任务点无法解决，跳过当前任务点")
                    Display.separate()
                    self.__driver.switch_to.default_content()
                    self.__driver.switch_to.frame("iframe")
                    iframeList = self.__driver.find_elements(By.TAG_NAME, 'iframe')
                self.__driver.switch_to.default_content()
                time.sleep(2)
            print("课程第{}{}节完成".format(chapterItemList[chapterItemIndex].number, chapterItemList[chapterItemIndex].name))
            Display.separate()
            self.__driver.find_element(By.CSS_SELECTOR, '[class="jb_btn jb_btn_92 fs14 prev_next next"]').click()
            chapterItemIndex += 1
        print("当前章节以全部完成")
