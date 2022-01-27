# -*- coding: utf-8 -*-
import string
from colorama import Fore, Back, init

init(autoreset=True)

class Display:
    # format: 每个元素控制对应列的宽度，元组第1个参数代表英文个数，第2次参数代表中文个数
    #                元组1、2两个元素的和代表列宽。元组第3个参数表示是否需要略写显示。
    #
    #       例如：((3, 3), (5, 10, true), (58, 6), (2, 5), (5, 3))表示有一行有5列数据。
    #             以元组中的第二个元素为例，其表示第二列数据占5个半角字符，10个全角字符，且开启省略显示
    #
    # overLengthKey:  控制缩写开关
    # overLengthOfEn: 英文文本长度阈值
    # overSymbolOfEN: 英文文本超过后补充的符号
    # numberCounter: 用于输出序号时记录当前序号
    # separateChar: 段落分隔符
    # warnChar: 警告分隔符

    format = [(10, 10, False) for i in range(10)]
    overLengthOfEn = 5
    overSymbolOfEn = "..."
    numberCounter = 1
    separateChar = "="
    warnChar: str = "*"

    @staticmethod
    def setFormat(formatList):
        Display.format.clear()
        for i in formatList:
            if len(i) == 2:
                Display.format.append((i[0], i[1], False))
            else:
                Display.format.append((i[0], i[1], True))

    @staticmethod
    def __strCount(strData: str, outKey: bool = False):
        """
        :param strData: 需要统计个数的字符串
        :param outKey: 控制是否缩写
        :return:
            返回三个元素的元组：
                newStr：新字符串
                countEn：新字符串中英文的个数
                countCn：新字符串中中文的个数
        """
        countEn = 0
        countCn = 0
        newStr = ""
        for s in strData:
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
    def printTable(strDataList, mode="L", numberKey=False):
        """
        :param strDataList: 一个列表，表示表格一行的所有元素。
        :param mode: 选择对齐方式
                    ‘l’     左对齐
                    'c'     居中对齐
                    'r'     右对齐
        :param numberKey: 是否开启显示序号
        :return: 无返回值
        """
        for i in range(len(strDataList)):
            countStr = str(Display.numberCounter) + "." if numberKey else ""
            strData = Display.__strCount(countStr + strDataList[i], Display.format[i][2])
            numSpaceEn = Display.format[i][0] - strData[1]
            numSpaceCh = Display.format[i][1] - strData[2]
            if mode in 'lLrR':
                if mode in 'lL':
                    print(strData[0] + chr(32) * numSpaceEn + chr(12288) * numSpaceCh, end="")
                elif mode in 'rR':
                    print(chr(32) * numSpaceEn + chr(12288) * numSpaceCh + strData[0], end="")
            elif mode in 'cC':
                beforeEn = numSpaceEn // 2
                beforeCh = numSpaceCh // 2
                afterEn = numSpaceEn - beforeEn
                afterCh = numSpaceCh - beforeCh
                print(
                    chr(32) * beforeEn + chr(12288) * beforeCh + strData[0] + chr(32) * afterEn + chr(12288) * afterCh,
                    end="")
            else:
                raise ValueError("value '{}' is illegal".format(mode))
            if numberKey:
                Display.numberCounter += 1
        print()

    @staticmethod
    def separate(number=40):
        print("\n"+Display.separateChar * number)

    @staticmethod
    def printWarning(warnString: str):
        """
        :param warnString: 警告内容
        :return: void
        """
        maxRow = 0
        maxCh = 0
        strList = warnString.split("\n")
        newStringList = []
        for i in strList:
            item = Display.__strCount(i)
            ch = item[2]
            maxRow = max(maxRow, len(item[0]))
            maxCh = max(maxCh, ch)
            newStringList.append(item)
        maxRow += 3
        info: str = ""
        info += (Display.warnChar*(maxRow+maxCh)+'\n')
        for i in newStringList:
            info += (Display.warnChar+" "+i[0]+(maxRow-maxCh-i[1])*chr(32)+(maxCh-i[2])*chr(12288)+Display.warnChar+"\n")
        info += (Display.warnChar * (maxRow + maxCh))
        print(Fore.RED+info)


if __name__ == '__main__':
    # print("="*100+"示例1")
    # # 正常输出
    # Display.setFormat(((15, 10), (10, 10)))
    # data = [['大学物理', '2021-2022上马克思主义基本原理概论'], ['面向对象程序设计（Java）', '形势与政策1/3（2021-2022学年第一学期）'], ['计算机网络与通信', '大学英语（三）非艺术类'], ['线性代数A(21-22(1))', '网络数据采集实践'], ['大学体育3（定向）2021-2022第一学期', '教务管理信息系统、教学云平台使用指南（学生版）'], ['实验室安全教育', '实验室安全教育'], ['职业生涯规划1', '形势与政策2/4（20-21学年第二学期）'], ['Python程序设计', '外教口语（二）'], ['大学英语（二）', '信息技术基础（二）-20-21(2)']]
    # for i in range(len(data)):
    #     Display.printTable(data[i])

    # print("="*100+"示例2")
    # # 折叠输出
    # Display.setFormat(((15, 10, True), (10, 10, True)))
    # for i in range(len(data)):
    #     Display.printTable(data[i])
    #
    # print("="*100+"示例3")
    # # 居中输出
    # Display.setFormat(((13, 20), (13, 20)))
    # data = [['大学物理', '2021-2022上马克思主义基本原理概论'], ['面向对象程序设计（Java）', '形势与政策1/3（2021-2022学年第一学期）'], ['计算机网络与通信', '大学英语（三）非艺术类'], ['线性代数A(21-22(1))', '网络数据采集实践'], ['大学体育3（定向）2021-2022第一学期', '教务管理信息系统、教学云平台使用指南（学生版）'], ['实验室安全教育', '实验室安全教育'], ['职业生涯规划1', '形势与政策2/4（20-21学年第二学期）'], ['Python程序设计', '外教口语（二）'], ['大学英语（二）', '信息技术基础（二）-20-21(2)']]
    # for i in range(len(data)):
    #     Display.printTable(data[i], "c")
    #
    # print("="*100+"示例4")
    # # 右对齐输出
    # Display.setFormat(((13, 20), (13, 20)))
    # data = [['大学物理', '2021-2022上马克思主义基本原理概论'], ['面向对象程序设计（Java）', '形势与政策1/3（2021-2022学年第一学期）'], ['计算机网络与通信', '大学英语（三）非艺术类'], ['线性代数A(21-22(1))', '网络数据采集实践'], ['大学体育3（定向）2021-2022第一学期', '教务管理信息系统、教学云平台使用指南（学生版）'], ['实验室安全教育', '实验室安全教育'], ['职业生涯规划1', '形势与政策2/4（20-21学年第二学期）'], ['Python程序设计', '外教口语（二）'], ['大学英语（二）', '信息技术基础（二）-20-21(2)']]
    # for i in range(len(data)):
    #     Display.printTable(data[i], "r")
    #
    print("="*100+"示例5")
    # 输出警告信息
    Display.printWarning("这是一个警告\n当前程序可能出错")