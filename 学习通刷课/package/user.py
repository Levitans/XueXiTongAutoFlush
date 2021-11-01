# -*- encoding = utf-8 -*-
# @Time : 2021-10-30 13:26
# @Author : Levitan
# @File : user.py
# @Software : PyCharm

class User:
    def __init__(self, name, account, password):
        self.__name = name
        self.__account = account
        self.__password = password

    def getUserName(self):
        return self.__name

    def getUserAccount(self):
        return self.__account

    def getUserPassword(self):
        return self.__password

    def setUserAccount(self, accountData):
        self.__account = accountData

    def setUserPassword(self, passwordData):
        self.__password = passwordData
