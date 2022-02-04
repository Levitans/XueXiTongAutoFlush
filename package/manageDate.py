# -*- encoding = utf-8 -*-
# @Time : 2021-09-14 0:25
# @Author : Levitan
# @File : manageDate.py
# @Software : PyCharm

import json
import os
from datetime import datetime
from package.user import User

# 管理用户数据
class UserData:
    def __init__(self, path):
        """
        :param path: 数据地址
        users 储存读取到的本地用户数据
        """
        self.__userDataPath = path
        self.__users = []
        self.__readUserData()       # 读取本地数据

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
        """
        :param name: 需要修改信息的用户名
        :param newData: 需要修改的新信息
        :param mode: 需要修改的是账号还是密码，默认修改密码
        :return: void
        """
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
    def addNewUser(self, name: str, account: str, password: str):
        """
        :param name: 用户姓名
        :param account: 用户账号
        :param password: 用户密码
        :return: void
        """
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

    def displayUserName(self):
        for j, i in enumerate(self.__users):
            print(str(j+1)+"、"+i.getUserName())


# 管理学科数据
class SubjectData:
    def __init__(self, filePath):
        """
        :param filePath: 文件读取路径
        __subjectData 指向以读取到的数据生成的字典
        """
        self.__subjectDataPath = filePath
        self.__subjectData = None
        self.__radeSubjectData()        # 开始读取数据

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
        """
        :param userName: 用户名称
        :param subjectName: 学科名称
        :return: 以字符串的形式返回学科进度

        如果学科数据中用户不存在，则将用户添加到学科数据中
        如果学科不存在则将学科添加到学科数据中，默认添加值为"1.1"
        """
        self.__subjectData.setdefault(userName, {})
        data = self.__subjectData[userName].setdefault(subjectName, "1.1")
        self.__saveSubjectData()
        return data

    # 更改学科数据
    def modifyClassData(self, userName, className, data="1.1"):
        """
        :param userName: 用户名称
        :param className: 学科名称
        :param data: 学科进度
        :return: void
        """
        if not (userName in list(self.__subjectData.keys())):
            raise Exception("{}用户不存在".format(userName))
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
