# -*- encoding = utf-8 -*-
# @Time : 2022-01-27 15:37
# @Author : Levitan
# @File : progress.py
# @Software : PyCharm

import threading
import time
from colorama import Fore, Back, init

init(autoreset=True)

class Progress(threading.Thread):
    def __init__(self):
        super(Progress, self).__init__()
        self.key: bool = True

    def run(self):
        print("logging：", end="")
        while self.key:
            print(Fore.GREEN+"▋", end="", flush=True)
            time.sleep(0.5)
        print("\nLanded successfully")


if __name__ == '__main__':
    a = Progress()
    a.start()
    time.sleep(2)
    a.key = False
