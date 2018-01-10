# -*- coding: utf-8 -*-
# @Time    : 2017/12/17 下午4:13
# @Author  : Yuhsuan
# @File    : analysis_auto.py
# @Software: PyCharm

# 自動抓取news_documents_r內的資料
# 根據每天將資料抓出來進行比對

from term_weighting import *
from log_module import log
from text_processor import get_file_list
import re
import numpy as np
import pandas

# 先取得目錄下所有的檔案名稱
file_list = get_file_list('/Users/yuhsuan/Desktop/MEMDS/news_documents/')

file_info = []
# 取得每個資料的日,來源,主題
for i in file_list:
    m = re.match('.*day(\d+)_(.*)_(.*)_.*.txt',i)
    file_info.append([m.group(0),int(m.group(1)),m.group(2),m.group(3)])

# 顯示所有的資料
log('%s\n\n' % file_info,lvl = 'i')

# 取得最大的日子
df = pandas.DataFrame(file_info,columns=['file_name','day','source','theme'])
max_day = max(df['day'])
log('max_day: %s' % max_day,lvl='i')

# 處理每一天的數據
for day in list(set(df['day'])):
    log('===='*20,lvl='i')
    log('process day: %s data' % day,lvl='i')
    # 每天的所有資料
    file_info_days = []

    for i in file_info:
        if int(i[1]) == day:
            file_info_days.append(i)

    # 轉換成dataframe
    df = pandas.DataFrame(file_info_days,columns=['file_name','day','source','theme'])
    log('Day %s data:\n %s' % (day,df),lvl='i')
    source = list(set(df['source']))
    log('source: %s' % source,lvl = 'i')

    # 建立channel_list給TF_PDF用
    channel_list = []
    for i in df['source']:
        for j in range(len(source)):
            if i == source[j]:
                channel_list.append(j+1)
    log('channel_list: %s' % channel_list,lvl = 'i')

    # 建立day_one_data取得每一天內的檔案們
    day_one_data = df['file_name']

    document_list=[]
    for data in day_one_data:
        # data = '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_cnn_cr_0_r.txt'
        file = open(data, 'r')
        # print(str(data))
        result = file.readline().strip().split(' ')
        document_list.append(result)
    log('document_list: %s' % document_list)

    # tf_idf的預測與結果
    tf_idf_cos = []
    tf_idf_pre = []
    tf_idf_act = []
    tf_idf_cre = 0.05 #設定準確率
    # tf_pdf的預測與結果
    tf_pdf_pre = []
    tf_pdf_act = []
    tf_pdf_cre = 0.1

    # 計算tf_idf資料
    log('計算tf-idf資料'+'===='*20,lvl='i')
    res = tf_idf(document_list)
    log('====' * 20)
    log('tf-idf: %s' % res)
    log('====' * 20)
    log(len(res[0]))

    # 計算tf-idf相似度
    log('計算tf-idf相似度' + '====' * 20, lvl='i')
    matrix = [[None]*(len(res)-1) for i in range(len(res)-1)]
    for i in range(1, len(res)):
        for j in range(1, i):
            log("%s, %s" % (i, j), lvl='i')
            cos = cosines(res[i], res[j])

            tf_idf_cos.append(cos)
            # 預測部分
            if cos>=tf_idf_cre:
                tf_idf_pre.append(True)
            else:
                tf_idf_pre.append(False)

            # 真實部分
            if df['theme'][i-1]==df['theme'][j-1]:
                tf_idf_act.append(True)
            else:
                tf_idf_act.append(False)

            matrix[j-1][i-1] = cos
    log('tf-idf: \n%s' % matrix,lvl='i')
    log('tf_idf_cos: %s,tf_idf_pre: %s, tf_idf_act: %s' % (tf_idf_cos,tf_idf_pre,tf_idf_act),lvl='i')
    from sklearn import metrics

    log('\n\nday: %s, files: %s, accuracy: %s, precision: %s, recall: %s, f1-score: %s\n\n' % (day,len(df),metrics.accuracy_score(tf_idf_act, tf_idf_pre),metrics.precision_score(tf_idf_act, tf_idf_pre),metrics.recall_score(tf_idf_act, tf_idf_pre),metrics.f1_score(tf_idf_act, tf_idf_pre)),lvl='i')
    # 計算tf_pdf資料
    log('計算tf-pdf資料' + '====' * 20, lvl='i')
    res = tf_pdf(document_list, channel_list)
    log('====' * 20)
    log(res)
    log('====' * 20)
    log('我是什麼東東？%s' % len(res[0]),lvl='i')

    # 計算tf-pdf相似度
    log('計算tf-pdf相似度' + '====' * 20, lvl='i')
    matrix = [[None] * (len(res)-1) for i in range(len(res)-1)]
    for i in range(1, len(res)):
        for j in range(1, i+1):
            log("%s, %s" % (i, j), lvl='i')
            cos = cosines(res[i], res[j])
            matrix[j-1][i-1] = cos
    log('tf-pdf: \n%s' % matrix, lvl='i')