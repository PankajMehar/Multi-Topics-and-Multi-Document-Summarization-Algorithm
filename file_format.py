# -*- coding: utf-8 -*-
# @Time    : 2017/9/11 上午10:19
# @Author  : Yuhsuan
# @File    : file_formate.py
# @Software: PyCharm Community Edition

import numpy
import codecs
# from text to csv
def txt_to_csv(filepath):
    f = codecs.open(filepath, 'r', encoding='utf8')
    lines = f.readlines()
    f.close()

    file_name = []
    news_title = []
    url = []

    for row in lines[1:]:
        _row = row.strip()
        _fields = _row.split("   ")
        print(_fields)
        file_name.append(_fields[0].strip())
        news_title.append(_fields[1].strip())
        url.append(_fields[2].strip())

    return file_name,news_title,url

