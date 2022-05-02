# -*- encoding = utf-8 -*-
# @Time : 2022-04-14 21:10
# @Author : Levitan
# @File : datamanger.py
# @Software : PyCharm

import time
import pickle
import base64
from package.learn import file
from package.learn import globalvar as gl


class UserManger:
    def __init__(self, filename):
        self.__filename = filename
        self.__users = file.get_json_data(filename)

    def getUserData(self, username) -> dict:
        return self.__users[username]

    def getUsersName(self) -> list:
        return list(self.__users.keys())

    def modifyUserData(self, name, newData, mode="pwd"):
        """
        :param name: 需要修改信息的用户名
        :param newData: 需要修改的新信息
        :param mode:
            "pwd": 修改密码
            "acc": 修改账号
            "del": 删除用户
        :return: void
        """
        if mode == "pwd":
            self.__users[name]["password"] = newData
        elif mode == "acc":
            self.__users[name]["account"] = newData
        elif mode == "del":
            self.__users.pop(name)
        file.save_json_data(self.__filename, self.__users)

    def addNewUser(self, name, account, password):
        self.__users[name] = {"account": account, "password": password}
        file.save_json_data(self.__filename, self.__users)


class CookiesManger:
    def __init__(self, filename):
        self.__filename = filename
        self.__cookies = file.get_json_data(filename)

    def getNameList(self):
        return list(self.__cookies.keys())

    def getCookies(self, username):
        # 用户不存在返回空
        if username not in list(self.__cookies.keys()):
            return []
        cookies_b64 = self.__cookies[username]
        cookies_bytes = base64.b64decode(cookies_b64)
        cookies_list = pickle.loads(cookies_bytes)
        # 检查cookies是否过期
        for i in cookies_list:
            if "expiry" not in list(i.keys()):
                continue
            expiry_timestamp = int(i['expiry'])
            if expiry_timestamp < int(time.time()):
                return []
        return cookies_list

    def setCookies(self, username, cookies):
        cookies_bytes = pickle.dumps(cookies)
        cookies_b64 = base64.b64encode(cookies_bytes)
        self.__cookies[username] = str(cookies_b64, encoding="utf-8")
        file.save_json_data(self.__filename, self.__cookies)

    def removeCookie(self, username):
        self.__cookies.pop(username)
        file.save_json_data(self.__filename, self.__cookies)

    def removeAll(self):
        self.__cookies.clear()
        file.save_json_data(self.__filename, self.__cookies)


class ExceptionLogManger:
    def __init__(self, filename):
        self.__filename = filename

    def writeLog(self, info):
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        version = file.get_json_data(gl.version_file_path)["current_version"]
        data = "时间："+nowTime+"\n版本："+version+"\n异常信息："+info+"\n\n"
        file.append_text_file(self.__filename, data)
