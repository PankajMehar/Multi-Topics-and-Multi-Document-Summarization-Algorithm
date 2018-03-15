# -*- coding: utf-8 -*-
# @Time    : 2018/3/9 下午 05:01
# @Author  : Yuhsuan
# @File    : lexrank_summary.py
# @Software: PyCharm

from lexrank import STOPWORDS, LexRank
import os
import json

documents = []
document_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"bbc")

for dirPath, dirNames, fileNames in os.walk(document_dir):
    for f in fileNames:
        try:
            with open(os.path.join(dirPath, f),"rt",encoding="utf8") as file:
                documents.append(file.readlines())
        except Exception as e:
            print(dirPath,f)

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

a = {}
with open("group_22.json","r",encoding="utf8") as file:
    a = json.load(file)

sen=[]
for i in a["source"]:
    sen.append(a["source"][i])

sentences=sen
print(sentences)

print("\n\n\n\n\n\n\n")
# get summary with classical LexRank algorithm
summary = lxr.get_summary(sentences, summary_size=2, threshold=.1)
print(summary)
print("\n\n\n\n\n\n\n")

# ['Mr Osborne said the coalition government was planning to change the tax '
#  'system "to make it fairer for people on low and middle incomes", and '
#  'undertake "long-term structural reform" of the banking sector, education and '
#  'the welfare state.',
#  'The BBC understands that as chancellor, Mr Osborne, along with the Treasury '
#  'will retain responsibility for overseeing banks and financial regulation.']


# get summary with continuous LexRank
# default value for 'summary_size' is 1 and 'threshold' is not referenced
summary_cont = lxr.get_summary(sentences, discretize=False)
print(summary_cont)

# ['The BBC understands that as chancellor, Mr Osborne, along with the Treasury '
#  'will retain responsibility for overseeing banks and financial regulation.']

# get LexRank scores for sentences
# when 'normalize' is True, all the scores are divided by the maximal one
# 'fast_power_method' speeds up the calculation, but requires more memory
scores_cont = lxr.rank_sentences(
    sentences,
    discretize=False,
    normalize=True,
    fast_power_method=False,
)
print(scores_cont)

#  [1.0896493024505858,
#  0.9010711968859021,
#  1.1139166497016315,
#  0.8279523250808547,
#  0.8112028559566362,
#  1.185228912485382,
#  1.0709787574388283]