# -*- encoding = utf-8 -*-
# @Time : 2022-07-27 23:15
# @Author : Levitan
# @File : getter.py
# @Software : PyCharm

from .template import School
from . import concreteSchool as cs

# 学校实例获取器
# 通过传入学校类的类名来获取学校实例
def schoolGetter(schoolType: str) -> School:
    try:
        school_obj_class = getattr(cs, schoolType)
    except AttributeError:
        raise Exception
    return school_obj_class()
