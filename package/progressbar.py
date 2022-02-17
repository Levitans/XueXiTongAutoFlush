# -*- encoding = utf-8 -*-
# @Time : 2022-01-27 15:37
# @Author : Levitan
# @File : progressbar.py
# @Software : PyCharm

import threading
import time
import math
from colorama import Fore, Back, init

init(autoreset=True)

class ProgressBar(threading.Thread):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.key: bool = True

    def run(self):
        print("logging：", end="")
        while self.key:
            print(Fore.GREEN+"▋", end="", flush=True)
            time.sleep(0.5)
        print()

class ProgressBar2(threading.Thread):
    def __init__(self):
        super(ProgressBar2, self).__init__()
        self.key: bool = True

    def run(self) -> None:
        scale = 50
        starTime = time.time()
        x = 50
        number = 0
        a = 0
        b = 0
        dur = 0
        strFormat = "\r{:^3.0f}%|{}{}| {:.2f}s"
        while self.key:
            number += 1/x*43
            if (number / scale) * 100 >= 99:
                c = 99
            else:
                c = (number / scale) * 100
                a = "█" * math.ceil(number)
                b = " " * math.ceil(scale - number)
            dur = time.time() - starTime
            print(strFormat.format(c, a, b, dur), end="")
            time.sleep(0.1)
            x += 1
        print(strFormat.format(100, "█"*scale, "", dur))


if __name__ == '__main__':
    test = ProgressBar2()
    test.run()
