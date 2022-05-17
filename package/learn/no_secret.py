# -*- encoding = utf-8 -*-
# @Time : 2022-05-16 23:31
# @Author : Levitan
# @File : no_secret.py
# @Software : PyCharm
import base64
import hashlib
import re
import os
from package.learn.file import get_json_data
from xml.dom.minidom import parse
from fontTools.ttLib import TTFont

class DecodeSecret:
    def __init__(self, fontFace):
        self.font_dict_name = "./package/font_dict.txt"
        self._secret_dict = {}
        self._font_dict = {}
        self._setSecretDict(fontFace)
        self._setFontDict()

    """
    函数功能：解析加密后的字体数据，将字形信息和字体编码映射到 self._secret_dict 中
    
    参数：
        :fontFace: 页面的 @font_face 中 base64 编码的值
    """
    def _setSecretDict(self, fontFace):
        ttf_temp_path = "./package/temp.ttf"       # 临时文件 temp.ttf 存放路径
        xml_temp_path = "./package/temp.xml"       # 临时文件 temp.xml 存放路径

        # 将 fontFace 解析为 temp.ttf 文件，在吧temp.ttf 文件解析为 temp.xml 文件
        b = base64.b64decode(fontFace)
        with open(ttf_temp_path, "wb") as f:
            f.write(b)
        font = TTFont(ttf_temp_path)
        font.saveXML(xml_temp_path)

        # 将字的十进制code和字形信息映射在 self._secret_dict 中
        domTree = parse(xml_temp_path)
        rootNode = domTree.documentElement
        ttglyph_list = rootNode.getElementsByTagName("TTGlyph")
        for ttglyph in ttglyph_list:
            name = ttglyph.getAttribute('name')
            if name == ".notdef":
                continue
            code = int(re.findall("uni(.*)", name)[0], 16)          # 10进制的值
            ttglyphStr = ""
            contour_list = ttglyph.getElementsByTagName("contour")
            for contour in contour_list:
                ttglyphStr += contour.toxml()
            value = hashlib.md5(ttglyphStr.encode(encoding="utf-8")).hexdigest()
            self._secret_dict[code] = value

        # 删除临时文件
        os.remove(ttf_temp_path)
        os.remove(xml_temp_path)

    """
    函数功能：读取 font_dict.txt 中的数据
        font_dict.txt 中存放的是学习通字体加密前，字形信息的md5值和字体编码的映射
    """
    def _setFontDict(self):
        self._font_dict = get_json_data(self.font_dict_name)

    """
    函数功能：将加密字符串解密
    :string: 被加密的字符串
    :return: 返回解密后的字符串
    """
    def decode(self, string: str):
        trueStr = ""
        for word in string:
            wordMD5 = self._secret_dict.get(ord(word), None)
            if wordMD5 is None:
                trueStr += word
                continue
            trueWordCode = self._font_dict.get(wordMD5, None)
            trueWor = chr(trueWordCode)
            trueStr += trueWor
        return trueStr
