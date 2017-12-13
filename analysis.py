# -*- coding: utf-8 -*-
# @Time    : 2017/12/13 下午11:13
# @Author  : Yuhsuan
# @File    : analysis.py
# @Software: PyCharm

# 將資料做相似度分析
# 第一天的資料產生文字矩陣後，放在news_documents_r中,開始對他做分析

from term_weighting import *
from log_module import log
import numpy

# 已經做過文字處理的資料
day_one_data = [
    '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_cnn_cr_0_r.txt',
    '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_cnn_cr_1_r.txt',
    '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_cnn_hk_0_r.txt',
    '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_cnn_se_0_r.txt',
    '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_cnn_se_1_r.txt',
    '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_cnn_se_2_r.txt',
    '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_the_cr_0_r.txt',
    '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_the_hk_0_r.txt',
    '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_the_se_0_r.txt',
    '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_the_se_1_r.txt'
]

document_list = []

for data in day_one_data:
    # data = '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_cnn_cr_0_r.txt'
    file = open(data,'r')
    result = file.readline().strip().split(' ')
    document_list.append(result)
log(document_list)
res = tf_idf(document_list)
log('===='*20)
log(res)
log('===='*20)
log(len(res[0]))

for i in range(1,len(res)):
    for j in range(1,i):
        log("%s, %s" % (i,j),lvl='i')
        cosines(res[i],res[j])