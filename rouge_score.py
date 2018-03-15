# -*- coding: utf-8 -*-
# @Time    : 2018/3/8 下午 09:35
# @Author  : Yuhsuan
# @File    : rouge.py
# @Software: PyCharm

from sumeval.metrics.rouge import RougeCalculator


rouge = RougeCalculator(stopwords=True, lang="en")

sum = """I went to the Mars from my living town."""

ref = """I went to Mars"""

rouge_1 = rouge.rouge_n(
            summary=sum,
            references=ref,
            n=1)

rouge_2 = rouge.rouge_n(
            summary=sum,
            references=ref,
            n=2)

rouge_l = rouge.rouge_l(
            summary=sum,
            references=ref,)

print("ROUGE-1: {}, ROUGE-2: {}, ROUGE-L: {}".format(
    rouge_1, rouge_2, rouge_l
).replace(", ", "\n"))