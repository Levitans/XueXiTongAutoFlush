# -*- coding: utf-8 -*-
import string
from colorama import Fore, Back, init

init(autoreset=True)

class Display:
    # format: 每个元素控制对应列的宽度，元组第1个参数类型为int表示占位个数，第2个参数类型为boolean表示是否开启略写显示
    #
    #       例如：format = [(10, False), (15, True), (58, True)]表示有一行有每行有3列数据。
    #            以format中第2个元素为例，其表示第二列数据占15个半角位，且开启省略显示
    #            format的长度表示一行的列数
    #
    #       注意：使用Display.printTable()前必须先调用Display.setFormat()对format进行初始化
    #
    # overLengthKey:  控制缩写开关
    # overLengthOfEn: 英文文本长度阈值
    # overSymbolOfEN: 英文文本超过后补充的符号
    # numberCounter: 用于输出序号时记录当前序号
    # separateChar: 段落分隔符
    # warnChar: 警告分隔符

    format = []
    overLengthOfEn = 5
    overSymbolOfEn = "..."
    numberCounter = 1
    separateChar = "="
    warnChar: str = "*"

    @staticmethod
    def setFormat(*formatList):
        """
        :param formatList: 传入的格式控制参数，传入的参数个数表示每行显示的列数
                            e.g.: setFormat(10, (15, True), (58, True))
                                format=[(10, False), (15，True), (58, True)]
        :return: void
        """
        Display.format.clear()
        for i in formatList:
            if isinstance(i, tuple):
                Display.format.append(i)
            elif isinstance(i, int):
                Display.format.append((i, False))
            else:
                raise Exception("参数{}类型错误，应该为int或(int, boolean)".format(i))

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
    def printTable(strDataList, mode="L", displayNumber=False):
        """
        :param strDataList: 需要输出为表格的全部数据
        :param mode: 选择对齐方式
                    ‘l’     左对齐
                    'c'     居中对齐
                    'r'     右对齐
        :param displayNumber: 是否开启显示序号
        :return: 无返回值

            函数根据Display.format对strDataList中的数据进行格式化输出
        """
        if len(Display.format) == 0:
            raise Exception("Display.format未设置")
        step = len(Display.format)
        dataList = [strDataList[i: i+step] for i in range(0, len(strDataList), step)]
        for j in dataList:
            for i in range(len(j)):
                countStr = str(Display.numberCounter) + "." if displayNumber else ""
                strData = Display.__strCount(countStr + j[i], Display.format[i][1])
                if mode in 'lLrR':
                    if mode in 'lL':
                        print(strData[0] + (Display.format[i][0] - strData[1] - strData[2] * 2) * chr(32), end="")
                    elif mode in 'rR':
                        print((Display.format[i][0] - strData[1] - strData[2] * 2) * chr(32) + strData[0], end="")
                elif mode in 'cC':
                    before = (Display.format[i][0] - strData[1] - strData[2] * 2) // 2
                    after = (Display.format[i][0] - strData[1] - strData[2] * 2) - before
                    print(chr(32) * before + strData[0] + chr(32) * after, end="")
                else:
                    raise ValueError("value '{}' is illegal".format(mode))
                if displayNumber:
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
        maxRowOfCh = 0
        maxRowOfEh = 0
        strList = warnString.split("\n")
        newStringList = []
        for i in strList:
            item = Display.__strCount(i)
            if len(item[0]) > maxRow:
                maxRowOfEh = item[1]
                maxRowOfCh = item[2]
                maxRow = len(item[0])
            newStringList.append(item)
        maxRow = maxRowOfEh + maxRowOfCh * 2
        info: str = ""
        info += (Display.warnChar * (maxRow + 4) + '\n')
        for i in newStringList:
            info += (Display.warnChar+" "+i[0]+chr(32)*(maxRow - i[2] * 2 - i[1])+" "+Display.warnChar+"\n")
        info += (Display.warnChar * (maxRow + 4))
        print(Fore.RED+info)
