# -*- encoding = utf-8 -*-
# @Time : 2022-03-26 22:00
# @Author : Levitan
# @File : taskInterface.py
# @Software : PyCharm
from abc import abstractmethod, ABCMeta


class Achievable(metaclass=ABCMeta):
    @abstractmethod
    def isCurrentTask(self, iframeIndex) -> bool:
        pass

    @abstractmethod
    def finish(self):
        pass
