# -*- coding: utf-8 -*-
# @Time    : 2018/3/9 下午 05:01
# @Author  : Yuhsuan
# @File    : lexrank_summary.py
# @Software: PyCharm

from lexrank import STOPWORDS, LexRank
import os
import json
from log_module import log

log("load reference doc")
documents = []
document_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bbc")

for dirPath, dirNames, fileNames in os.walk(document_dir):
    for f in fileNames:
        try:
            with open(os.path.join(dirPath, f), "rt", encoding="utf8") as file:
                documents.append(file.readlines())
        except Exception as e:
            log("path: %s%s" % (dirPath, f))

lxr = LexRank(documents, stopwords=STOPWORDS['en'])

sentences = [
    'One of David Cameron\'s closest friends and Conservative allies, '
    'George Osborne rose rapidly after becoming MP for Tatton in 2001.',

    'Michael Howard promoted him from shadow chief secretary to the '
    'Treasury to shadow chancellor in May 2005, at the age of 34.',

    'Mr Osborne took a key role in the election campaign and has been at '
    'the forefront of the debate on how to deal with the recession and '
    'the UK\'s spending deficit.',

    'Even before Mr Cameron became leader the two were being likened to '
    'Labour\'s Blair/Brown duo. The two have emulated them by becoming '
    'prime minister and chancellor, but will want to avoid the spats.',

    'Before entering Parliament, he was a special adviser in the '
    'agriculture department when the Tories were in government and later '
    'served as political secretary to William Hague.',

    'The BBC understands that as chancellor, Mr Osborne, along with the '
    'Treasury will retain responsibility for overseeing banks and '
    'financial regulation.',

    'Mr Osborne said the coalition government was planning to change the '
    'tax system \"to make it fairer for people on low and middle '
    'incomes\", and undertake \"long-term structural reform\" of the '
    'banking sector, education and the welfare state.',
]


for file_group in range(19):
    log(str(file_group))

    group_data = {}
    with open("group_data/%s/group_%s.json" % (file_group,file_group),"r",encoding="utf8") as file:
        group_data = json.load(file)

    sen = []
    for i in group_data["source"]:
        sen.append(group_data["source"][i])

    sentences = sen
    log("start summary")
    summary = lxr.get_summary(sentences, summary_size=10, threshold=.1)
    # print(summary)
    if not os.path.exists("lexrank"):
        os.mkdir("lexrank")

    with open("lexrank/%s.text" % file_group, "w", encoding="utf8") as file:
        file.writelines(summary)