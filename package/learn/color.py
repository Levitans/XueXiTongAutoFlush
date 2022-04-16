# -*- encoding = utf-8 -*-
# @Time : 2022-04-15 13:54
# @Author : Levitan
# @File : color.py
# @Software : PyCharm

from colorama import Fore, Back

def read(some_str):
    return Fore.LIGHTRED_EX + some_str + Fore.RESET

def yellow(some_str):
    return Fore.YELLOW + some_str + Fore.RESET

def blue(some_str):
    return Fore.BLUE + some_str + Fore.RESET

def green(some_str):
    return Fore.GREEN + some_str + Fore.RESET

def magenta(some_str):
    return Fore.MAGENTA + some_str + Fore.RESET