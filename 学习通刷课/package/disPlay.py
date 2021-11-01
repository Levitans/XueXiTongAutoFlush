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


if __name__ == "__main__":
    data = ["大数据导论", "面向对象程序设计(Java)", '2021-2022上马克思主义基本原理概论', '数据结构', '网络数据采集实践',
            '形势与政策1/3（2021-2022学年第一学期）', '计算机网络与通信', '大学体育3（羽毛球）', '大学英语（三）非艺术类',
            '大学物理', '毛泽东思想和中国特色社会主义理论体系概论2', '线性代数A(21-22(1))',
            '教务管理信息系统、教学云平台使用指南（学生版）', '实验室安全教育', '实验室安全教育',
            '职业生涯规划1', '外教口语（二）', "形势与政策2/4（20-21学年第二学期）",
            'Python程序设计', '外教口语（二）', '大学英语（二）', '日本漫画鉴赏（公选）',
            '信息技术基础（二）-20-21(2)', '高等数学A（下）', '大学生心理与学业指导', '灌口中学高三寒假云课堂',
            '灌口中学高三寒假云课堂', '2020届高三化学寒假云课堂', '灌口中学高三寒假云课堂', '毛泽东思想和中国特色社会主义理论体系概论1',
            '2020届高三物理寒假云课堂', '2018届高三暑期语文云课堂', '厦门市2020寒假高三数学云课堂', '2020届高三英语寒假云课堂',
            '2020届高三生物寒假云课堂']
    DisPlay.disPlay(data)

