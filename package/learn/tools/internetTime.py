# -*- encoding = utf-8 -*-
# @Time : 2021-11-11 22:50
# @Author : Levitan
# @File : internetTime.py
# @Software : PyCharm

from time import mktime, strftime, strptime
import json
import requests

class InternetTime:
    # 过期时间
    __expirationDate = '2022-07-01 00:00:00'

    @staticmethod
    def isExpiration():
        isExpiration = False
        try:
            url = "http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp"
            r = requests.get(url)
            nowTime = json.loads(r.text)
            nowTime = int(nowTime["data"]["t"])/1000
        except Exception:
            print("网络时间抓取失败")
            return isExpiration

        expirationTimestamp = mktime(strptime(InternetTime.__expirationDate, '%Y-%m-%d %H:%M:%S'))

        isExpiration = True if nowTime < expirationTimestamp else False
        return isExpiration
