# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 13:26
# @Author : Levitan
# @File : user.py
# @Software : PyCharm

class User:
    def __init__(self, name, account, password):
        self.__name: str = name
        self.__account: str = account
        self.__password: str = password

    def getName(self):
        return self.__name

    def getAccount(self):
        return self.__account

    def getPassword(self):
        return self.__password

    def setAccount(self, accountData):
        self.__account = accountData

    def setPassword(self, passwordData):
        self.__password = passwordData
