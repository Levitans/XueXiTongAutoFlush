# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 18:52
# @Author : Levitan
# @File : mydriver.py
# @Software : PyCharm

# 自定义包
from . import useragent, driverException as myException

# 第三方包
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement


class MyDriver:
    def __init__(self, browserPath, driverPath, noImg=False, noHead=False, mute=False):
        try:
            # 配置驱动选项
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            if noImg:
                options.add_argument('blink-settings=imagesEnabled=true')
            if noHead:
                options.add_argument('headless')
                options.add_argument('--disable-gpu')
            if mute:
                options.add_argument('--mute-audion')
            options.add_argument('--user-agent={}'.format(useragent.getheaders()))
            options.binary_location = browserPath

            # 创建驱动实例
            self.__driver = webdriver.Chrome(executable_path=driverPath, options=options)
        except Exception as e:
            print(e.__str__())

    # 访问url
    def get_url(self, url):
        self.__driver.get(url)

    # 返回驱动
    def get_driver(self):
        return self.__driver

    # 通过账号密码登陆
    # 登录成功后将会返回cookies
    def login_with_acc_and_pwd(self, act, pwd):
        self.get_url("http://i.chaoxing.com")
        # 1、设置账号
        account = self.__driver.find_element(By.ID, "phone")
        account.send_keys(act)
        # 2、设置密码
        password = self.__driver.find_element(By.ID, "pwd")
        password.send_keys(pwd)
        # 3、点击登录
        self.__driver.find_element(By.ID, "loginBtn").click()
        # 4、等待页面加载
        try:
            self.driver_wait(By.CLASS_NAME, "header")
        except myException.TimeoutException as e:
            raise Exception("网络延迟，页面未正常加载")
        # 5、返回cookies
        return self.__driver.get_cookies()

    # 使用二维码登陆
    # 登陆成功后返回登陆者的姓名和cookies
    def login_with_QRCode(self):
        self.get_url("http://i.chaoxing.com")

        # 等待用户扫描二维码
        try:
            self.driver_wait(By.CLASS_NAME, "user-name")
        except myException.TimeoutException:
            raise Exception("网络延迟，页面未正常加载")

        # 获取用户名和cookies值
        username = self.__driver.find_element(By.CLASS_NAME, "user-name").text
        cookies = self.__driver.get_cookies()
        return username, cookies

    # 通过 cookie 登陆
    def login_with_cookies(self, cookies):
        self.get_url("http://i.chaoxing.com")
        self.set_cookies(cookies)
        self.get_url("http://i.chaoxing.com")

    # 获取二维码的URL
    def getQRCoed(self):
        try:
            img = WebDriverWait(self.__driver, 30, 0.2).until(
                lambda driver: driver.find_element(By.ID, "quickCode")
            )
            path = img.get_attribute("src")
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            return path

    def get_cookies(self):
        cookies = self.__driver.get_cookies()
        return cookies

    def set_cookies(self, cookies):
        try:
            for i in cookies:
                self.__driver.add_cookie(i)
        except exceptions.InvalidCookieDomainException as e:
            print(e.__str__)

    # 跳转到课程的页面
    def go_courses_page(self):
        self.__driver.get("http://mooc1-1.chaoxing.com/visit/interaction")
        self.driver_wait(By.CLASS_NAME, "course-list")

    # 判断元素在页面中是否存在
    # 如果存在，返回该元素
    # 如果不存在，返回None
    def is_element_presence(self, by, value):
        try:
            item = self.__driver.find_element(by, value)
        except:
            return None
        return item

    def getElement(self, by, value) -> WebElement:
        self.driver_wait(by, value)
        return self.__driver.find_element(by, value)

    def getElements(self, by, value) -> list[WebElement]:
        self.driver_wait(by, value)
        return self.__driver.find_elements(by, value)

    # 等待元素出现
    def driver_wait(self, by, value, wait_time=30, wait_times=5):
        waitCount = 1
        while True:
            try:
                WebDriverWait(self.__driver, wait_time, 0.2).until(
                    lambda driver: driver.find_element(by, value)
                )
                break
            except exceptions.TimeoutException:
                waitCount += 1
                if waitCount > wait_times:
                    raise myException.TimeoutException("当前网络延迟严重\n通过 " + by + " 在页面中没有找到 " + value)
                print("当前网络缓慢...")
                print("程序会等待 " + str(wait_times) + " 轮，当前等待第 " + str(waitCount) + " 轮")

    # 使用js
    def go_js(self, js):
        self.__driver.execute_script(js)

    # 关闭驱动
    def quit(self):
        self.__driver.quit()
