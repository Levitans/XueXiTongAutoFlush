# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 18:52
# @Author : Levitan
# @File : mydriver.py
# @Software : PyCharm

import time
from package.learn import useragent
from package.learn import globalvar as gl
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MyDriver:
    def __init__(self, noImg=None, noHead=None):
        if not gl.is_init:
            raise Exception("程序尚未初始化")
        noImg = gl.no_img if(noImg is None) else noImg
        noHead = gl.no_head if(noHead is None) else noHead

        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            if noImg:
                options.add_argument('blink-settings=imagesEnabled=true')
            if noHead:
                options.add_argument('headless')
            if gl.mute:
                options.add_argument('--mute-audion')
            options.add_argument('--user-agent={}'.format(useragent.getheaders()))
            options.binary_location = gl.browser_path
            self.__driver = webdriver.Chrome(executable_path=gl.driver_path, options=options)
        except Exception as e:
            print(e.__str__())

    def get_url(self, url):
        self.__driver.get(url)

    def get_driver(self):
        return self.__driver

    # 通过账号密码登陆
    def login_with_acc_and_pwd(self, username):
        self.__driver.get("http://i.chaoxing.com")
        users = gl.user_manager.getUserData(username)
        account = self.__driver.find_element(By.ID, "phone")
        account.send_keys(users["account"])
        password = self.__driver.find_element(By.ID, "pwd")
        password.send_keys(users["password"])
        self.__driver.find_element(By.ID, "loginBtn").click()
        try:
            self.driver_wait(By.CLASS_NAME, "header")
        except exceptions.TimeoutException:
            print("登陆失败")
            exit()
        cookies = self.__driver.get_cookies()
        gl.cookie_manager.setCookies(username, cookies)

    def login_with_QRCode(self):
        self.__driver.get("http://i.chaoxing.com")
        try:
            self.driver_wait(By.CLASS_NAME, "user-name")
        except exceptions.TimeoutException:
            print("登陆超时")
            exit()
        username = self.__driver.find_element(By.CLASS_NAME, "user-name").text
        cookies = self.__driver.get_cookies()
        gl.cookie_manager.setCookies(username, cookies)
        return username

    # 通过 cookie 登陆
    def login_with_cookies(self, username):
        self.__driver.get("http://i.chaoxing.com")
        cookies = gl.cookie_manager.getCookies(username)

        # cookies 过期或没有找到 cookies
        if len(cookies) == 0:
            pass

        self.set_cookies(cookies)
        self.__driver.get("http://i.chaoxing.com")

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

    def go_courses_page(self):
        self.__driver.get("http://mooc1-1.chaoxing.com/visit/interaction")
        try:
            self.driver_wait(By.CLASS_NAME, "course-list")
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
            exit()

    def is_element_presence(self, by, value):
        try:
            item = self.__driver.find_element(by, value)
        except:
            return None
        return item

    def driver_wait(self, by, value, wait_time=30):
        try:
            WebDriverWait(self.__driver, wait_time, 0.2).until(
                lambda driver: driver.find_element(by, value))
        except exceptions.TimeoutException:
            print("当前网络缓慢...")

    def go_js(self, js):
        self.__driver.execute_script(js)

    def quit(self):
        self.__driver.quit()
