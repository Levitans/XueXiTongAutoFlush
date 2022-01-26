# -*- coding: utf-8 -*-
import string
class Display:
    """
    format: 每个元素控制对应列的宽度，元组第1个参数代表英文个数，第2次参数代表中文个数
                   元组1、2两个元素的和代表列宽。元组第3个参数表示是否需要略写显示。

          例如：((3, 3), (5, 10, true), (58, 6), (2, 5), (5, 3))表示有一行有5列数据。
                以元组中的第二个元素为例，其表示第二列数据占5个半角字符，10个全角字符，且开启省略显示

    overLengthKey:  控制缩写开关
    overLengthOfEn: 英文文本长度阈值
    overSymbolOfEN: 英文文本超过后补充的符号
    """
    format = [(10, 10, False) for i in range(10)]
    overLengthOfEn = 5
    overSymbolOfEn = "..."

    @staticmethod
    def setFormat(formatList):
        Display.format.clear()
        for i in formatList:
            if len(i) == 2:
                Display.format.append((i[0], i[1], False))
            else:
                Display.format.append((i[0], i[1], True))

    @staticmethod
    def __strCount(str, outKey):
        countEn = 0
        countCn = 0
        newStr = ""
        for s in str:
            # 英文
            if s in string.ascii_letters or s in './ ':
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
            if outKey and countEn + countCn >= Display.overLengthOfEn:
                newStr += Display.overSymbolOfEn
                countEn += len(Display.overSymbolOfEn)
                break
            # 判断是否超过长度
        return newStr, countEn, countCn

    @staticmethod
    def printTable(strDataList, mode="L"):
        """
        :param strDataList: 一个列表，表示表格一行的所有元素。
        :param mode: 选择对齐方式
                    ‘l’     左对齐
                    'c'     居中对齐
                    'r'     右对齐
        :return: 无返回值
        """
        if mode in 'lLrR':
            for i in range(len(strDataList)):
                strData = Display.__strCount(strDataList[i], Display.format[i][2])
                numSpaceEn = Display.format[i][0] - strData[1]
                numSpaceCh = Display.format[i][1] - strData[2]
                if mode in 'lL':
                    print(strData[0]+chr(32)*numSpaceEn+chr(12288)*numSpaceCh, end="")
                elif mode in 'rR':
                    print(chr(32)*numSpaceEn+chr(12288)*numSpaceCh+strData[0], end="")
            print()
        elif mode in 'cC':
            for i in range(len(strDataList)):
                strData = Display.__strCount(strDataList[i], Display.format[i][2])
                numSpaceEn = Display.format[i][0]-strData[1]
                numSpaceCh = Display.format[i][1]-strData[2]
                beforeEn = numSpaceEn//2
                beforeCh = numSpaceCh//2
                afterEn = numSpaceEn-beforeEn
                afterCh = numSpaceCh-beforeCh
                print(chr(32)*beforeEn + chr(12288)*beforeCh + strData[0] + chr(32)*afterEn + chr(12288)*afterCh, end="")
            print()
        else:
            raise ValueError("value '{}' is illegal".format(mode))

    @staticmethod
    def separate(number=20):
        separateChar = "="
        print(separateChar*number)

    @staticmethod
    def printWarning(inf):
        print(inf)


if __name__ == '__main__':
    Display.setFormat(((10, 10, True), (10, 10, True)))
    Display.overLengthOfEn = 10
    data = ['大学物理', '2021-2022上马克思主义基本原理概论', '面向对象程序设计（Java）', '形势与政策1/3（2021-2022学年第一学期）', '计算机网络与通信', '大学英语（三）非艺术类', '线性代数A(21-22(1))', '网络数据采集实践', '大学体育3（定向）2021-2022第一学期', '教务管理信息系统、教学云平台使用指南（学生版）', '实验室安全教育', '实验室安全教育', '职业生涯规划1', '形势与政策2/4（20-21学年第二学期）', 'Python程序设计', '外教口语（二）', '大学英语（二）', '信息技术基础（二）-20-21(2)', '高等数学A（下）', '大学生心理与学业指导', '外教口语（一）', '外教口语（一）', '大学英语（一）非艺术类', '3月10日-11日市质检试卷', '2020年全市高中毕业质量检测-考前模拟', '书香九中智慧阅读', '2020届生物复习', '“新冠病毒”及其他（年段通识课）', '高三化学', '每天一点财富金融学（2021下）', '产业经济学（2021下）', '数据结构', '毛泽东思想和中国特色社会主义理论体系概论2', '毛泽东思想和中国特色社会主义理论体系概论1']
    dataLength = 0
    if len(data) % 2 == 0:
        dataLength = len(data)
    else:
        dataLength = len(data)+1
        data.append(None)
    print(data)
    for i in range(0, dataLength, 2):
        Display.printTable([data[i], data[i+1]])
        # print([data[i], data[i+1]])
    # 123123