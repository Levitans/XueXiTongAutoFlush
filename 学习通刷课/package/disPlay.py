# -*- encoding = utf-8 -*-
# @Time : 2021-10-31 14:14
# @Author : Levitan
# @File : disPlay.py
# @Software : PyCharm

import string

class DisPlay:
    # 统计中英文字符个数，返回去掉特殊字符的字符串
    @staticmethod
    def __strCount(str):
        countEn = 0
        countCn = 0
        newStr = ""
        for s in str:
            # 英文
            if s in string.ascii_letters or s == '.':
                countEn += 1
                newStr += s
            # 数字
            elif s.isdigit():
                countEn += 1
                newStr += s
            # 空格
            elif s.isspace():
                countEn += 1
                newStr += s
            # 中文
            elif s.isalpha():
                countCn += 1
                newStr += s
            # 特殊字符
            else:
                pass
        return newStr, countEn, countCn

    @staticmethod
    def disPlay(strDataList):
        for i in range(len(strDataList)):
            strData = DisPlay.__strCount(str(i+1)+"."+strDataList[i])
            numOfSpaceEn = 15-strData[1]
            numOfSpaceCn = 20-strData[2]
            print(strData[0]+chr(32)*numOfSpaceEn+chr(12288)*numOfSpaceCn, end="")
            if i % 2 == 1:
                print()
        print()

