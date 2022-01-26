# -*- encoding = utf-8 -*-
# @Time : 2021-09-14 0:25
# @Author : Levitan
# @File : manageDate.py
# @Software : PyCharm

import json
import os
from datetime import datetime
from package.user import User


class UserData:
    def __init__(self, path):
        self.__userDataPath = path
        self.__users = []
        self.__readUserData()

    # 读取本地存储的用户数据
    def __readUserData(self):
        """
        读取用户数据，将每个用户数据封装到User中，在存到self.__users中
        """
        f = open(self.__userDataPath, "r", encoding="utf-8")
        inf = f.read()
        f.close()
        users = json.loads(inf)
        keys = list(users.keys())
        values = list(users.values())
        for i in keys:
            act = users[i]['account']
            psd = users[i]['password']
            newUser = User(i, act, psd)
            self.__users.append(newUser)

    # 获取用户信息
    def getUsers(self):
        return self.__users

    # 获取用户数据量
    def getUserAmount(self):
        return len(self.__users)

    # 修改已有用户数据
    def modifyUserData(self, name, newData, mode="password"):
        for i in self.__users:
            if i.getUserName() == name and mode == "password":
                i.setUserPassword(newData)
                break
            if i.getUserName() == name and mode == "account":
                i.setUserAccount(newData)
                break
        self.__saveUsersData()
        print("修改成功")

    # 添加新用户
    def addNewUser(self, name, account, password):
        nameList = [i.getUserName() for i in self.__users]
        if name in nameList:
            raise KeyError("用户名被占用")
        newUser = User(name, account, password)
        self.__users.append(newUser)
        self.__saveUsersData()

    # 保存用户数据
    def __saveUsersData(self):
        userData = {}
        # 将User类解析成dict类
        for i in self.__users:
            userData[i.getUserName()] = {"account": i.getUserAccount(), "password": i.getUserPassword()}
        f = open(self.__userDataPath, "w", encoding="utf-8")
        usersDataString = json.dumps(userData, ensure_ascii=False)
        f.write(usersDataString)
        f.close()


class SubjectData:
    def __init__(self, filePath):
        self.__subjectDataPath = filePath
        self.__subjectData = None
        self.__radeSubjectData()

    # 读取学科数据
    def __radeSubjectData(self):
        f = open(self.__subjectDataPath, "r", encoding="utf-8")
        inf = f.read()
        f.close()
        self.__subjectData = json.loads(inf)

    # 保存学科数据
    def __saveSubjectData(self):
        f = open(self.__subjectDataPath, "w", encoding="utf-8")
        inf = json.dumps(self.__subjectData, ensure_ascii=False)
        f.write(inf)
        f.close()

    # 查找学科数据
    def getSubjectProcess(self, userName, subjectName):
        if not(userName in list(self.__subjectData.keys())):
            self.__subjectData[userName] = {}
        if not(subjectName in list(self.__subjectData[userName].keys())):
            self.modifyClassData(userName, subjectName)
        return self.__subjectData[userName][subjectName]

    # 更改学科数据
    def modifyClassData(self, userName, className, data="1.1"):
        if not (userName in list(self.__subjectData.keys())):
            pass
        elif not (className in list(self.__subjectData[userName].keys())):
            self.__subjectData[userName][className] = data
        else:
            self.__subjectData[userName][className] = data
        self.__saveSubjectData()


# 1表示关闭显示浏览器，0表示开启显示浏览器
class BrowserConfiguration:
    def __init__(self, filPath):
        self.__path = filPath
        self.__browserState = {}
        self.__radeSubjectData()

    def __radeSubjectData(self):
        f = open(self.__path, "r", encoding="utf-8")
        inf = f.read()
        f.close()
        self.__browserState = json.loads(inf)

    def modifyClassData(self, key):
        self.__browserState["browserState"] = key
        self.__save()

    def __save(self):
        f = open(self.__path, "w", encoding="utf-8")
        data = json.dumps(self.__browserState)
        f.write(data)
        f.close()

    def getState(self):
        return self.__browserState["browserState"]


if __name__ == '__main__':
    test = UserData(r"F:\python项目\学习通刷课2\data\user_data.json")
    a = test.getUsers()[0]
    print(a.getUserName())
    print(a.getUserAccount())
    print(a.getUserPassword())
    test.modifyUserData("Levitan", 123123)
