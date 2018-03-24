# -*- coding: utf-8 -*-
# @Time    : 2018/3/24 下午 12:58
# @Author  : Yuhsuan
# @File    : mainpath_textrank_summary.py
# @Software: PyCharm

# pip install summa
import os
from summa import summarizer

if not os.path.exists("textrank"):
    os.mkdir("textrank")

for file_group in range(19):
    for i in range(1,100):

        if os.path.exists("main_path_summary/%s_%s.txt" % (file_group,i)):
            text = ""
            with open("main_path_summary/%s_%s.txt" % (file_group,i), "r", encoding="utf8") as file:
                text = file.read()

            textrank = summarizer.summarize(text)

            with open("textrank/%s_%s.txt" % (file_group,i), "w", encoding="utf8") as file:
                file.write(textrank)
