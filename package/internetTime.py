# -*- encoding = utf-8 -*-
# @Time : 2021-11-11 22:50
# @Author : Levitan
# @File : internetTime.py
# @Software : PyCharm

import requests
import json
from package.display import Display

class InternetTime:
    # 过期时间
    expirationDate = 20221010

    @staticmethod
    def isExpiration():
        isExpiration = False
        nowTime = 9999999
        try:
            url = "http://quan.suning.com/getSysTime.do"
            r = requests.get(url)
            nowTime = json.loads(r.text)
            nowTime = nowTime["sysTime2"]
            nowTime = nowTime.partition(" ")
            nowTime = nowTime[0].replace("-", "")
        except Exception:
            Display.printWarning("网络时间抓取失败")
            return isExpiration
        isExpiration = True if int(nowTime) < InternetTime.expirationDate else False
        return isExpiration
