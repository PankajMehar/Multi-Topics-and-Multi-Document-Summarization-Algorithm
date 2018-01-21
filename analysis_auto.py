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
from sklearn import metrics
import json
import os


def similuity(file_path):
    # 儲存用的資料結構
    RESULT = {}

    # 先取得目錄下所有的檔案名稱
    file_list = get_file_list(file_path)

    # 所有的資料存放的地方
    file_info = []

    # 取得每個資料的日,來源,主題
    for i in file_list:
        # 將.json與.csv剔除
        if '.json' not in i and '.csv' not in i:
            m = re.match('.*day(\d+)_(.*)_(.*)_.*.txt', i)
            file_info.append([m.group(0), int(m.group(1)), m.group(2), m.group(3)])

    # 顯示所有的資料
    log('%s\n\n' % file_info, lvl='i')

    # 取得最大的日子
    df = pandas.DataFrame(file_info, columns=['file_name', 'day', 'source', 'theme'])
    max_day = max(df['day'])
    log('max_day: %s' % max_day, lvl='i')

    RESULT['max_day']=max_day
    RESULT['daily_data'] = []
    result_daily_data = RESULT['daily_data']
    # 處理每一天的數據
    for day in list(set(df['day'])):
        log('====' * 20)
        log('process day: %s data' % day)

        # 紀錄第幾天的資料
        daily_result = {}
        daily_result['day'] = day
        daily_result['process_day'] = []
        daily_result['real_data'] = []
        daily_result['cos'] = []
        daily_result['tf_idf'] = []
        daily_result['tf_pdf'] = []

        # 每天的所有資料
        file_info_days = []

        for i in file_info:
            if int(i[1]) == day:
                file_info_days.append(i)

        # 轉換成dataframe
        df = pandas.DataFrame(file_info_days, columns=['file_name', 'day', 'source', 'theme'])
        log('Day %s data:\n %s' % (day, df))
        source = list(set(df['source']))
        log('source: %s' % source)

        # 建立channel_list給TF_PDF用
        channel_list = []
        for i in df['source']:
            for j in range(len(source)):
                if i == source[j]:
                    channel_list.append(j + 1)
        log('channel_list: %s' % channel_list)

        # 建立day_one_data取得每一天內的檔案們
        day_one_data = df['file_name']

        document_list = []
        for data in day_one_data:
            # data = '/Users/yuhsuan/Desktop/MEMDS/news_documents_r/day0_cnn_cr_0_r.txt'
            file = open(data, 'r', encoding='utf8')
            # print(str(data))
            result = file.readline().strip().split(' ')
            document_list.append(result)
        log('document_list: %s' % document_list)

        # tf_idf的預測與結果
        tf_idf_cos = []
        tf_idf_pre = []
        tf_idf_act = []
        tf_idf_criteria = 0.05  # 設定準確率
        # tf_pdf的預測與結果
        tf_pdf_pre = []
        tf_pdf_act = []
        tf_pdf_criteria = 0.1

        #計算一般的字詞資料
        log('計算一般字詞資料' + '====' * 20, lvl='i')
        res = simple(document_list)
        log('====' * 20)
        log('一般字詞: %s' % res)
        log('====' * 20)
        log('length of simple: %s' % len(res[0]), lvl='i')

        # 計算一般的字詞相似度
        log('計算一般的字詞相似度' + '====' * 20, lvl='i')
        matrix = [[None] * (len(res) - 1) for i in range(len(res) - 1)]
        for i in range(1, len(res)):
            for j in range(1, i):
                log("%s, %s" % (i, j), lvl='i')
                cos = cosines(res[i], res[j])
                daily_result['cos'].append(cos)

        # 計算tf_idf資料
        log('計算tf-idf資料' + '====' * 20, lvl='i')
        res = tf_idf(document_list)
        log('====' * 20)
        log('tf-idf: %s' % res)
        log('====' * 20)
        log('length of tf-idf: %s' % len(res[0]), lvl='i')

        # 計算tf-idf相似度
        log('計算tf-idf相似度' + '====' * 20, lvl='i')
        matrix = [[None] * (len(res) - 1) for i in range(len(res) - 1)]
        for i in range(1, len(res)):
            for j in range(1, i):
                log("%s, %s" % (i, j))
                daily_result['process_day'].append((i,j))

                # 真實部分
                if df['theme'][i - 1] == df['theme'][j - 1]:
                    daily_result['real_data'].append(True)
                else:
                    daily_result['real_data'].append(False)

                cos = cosines(res[i], res[j])
                daily_result['tf_idf'].append(cos)

                tf_idf_cos.append(cos)

        #         # 預測部分
        #         if cos >= tf_idf_criteria:
        #             tf_idf_pre.append(True)
        #         else:
        #             tf_idf_pre.append(False)
        #

        #
        #         matrix[j - 1][i - 1] = cos
        # log('tf-idf: \n%s' % matrix, lvl='i')
        # log('tf_idf_cos: %s,tf_idf_pre: %s, tf_idf_act: %s' % (tf_idf_cos, tf_idf_pre, tf_idf_act), lvl='i')
        # # from sklearn import metrics
        #
        # log('\n\nday: %s, files: %s, accuracy: %s, precision: %s, recall: %s, f1-score: %s\n\n' % (
        # day, len(df), metrics.accuracy_score(tf_idf_act, tf_idf_pre), metrics.precision_score(tf_idf_act, tf_idf_pre),
        # metrics.recall_score(tf_idf_act, tf_idf_pre), metrics.f1_score(tf_idf_act, tf_idf_pre)), lvl='i')
        #

        # 計算tf_pdf資料
        log('計算tf-pdf資料' + '====' * 20, lvl='i')
        res = tf_pdf(document_list, channel_list)
        log('====' * 20)
        log(res)
        log('====' * 20)
        log('length of tf-pdf: %s' % len(res[0]), lvl='i')

        # 計算tf-pdf相似度
        log('計算tf-pdf相似度' + '====' * 20, lvl='i')
        matrix = [[None] * (len(res) - 1) for i in range(len(res) - 1)]
        for i in range(1, len(res)):
            for j in range(1, i):
                log("%s, %s" % (i, j))
                cos = cosines(res[i], res[j])
                daily_result['tf_pdf'].append(cos)
                # matrix[j - 1][i - 1] = cos
        # log('tf-pdf: \n%s' % matrix, lvl='i')
        result_daily_data.append(daily_result)

    output_path = os.path.join(file_path,'analysis_temp.json')
    with open(output_path,'w') as fp:
        json.dump(RESULT,fp)
    return output_path

def metrics_value(day,type,testing_data,real_data,start,add,stop):
    # type = simple or tf-idf or tf-pdf
    # testing_data = daily['cos'] or daily['tf-idf'] or daily['tf-pdf']
    # real_data = daily['real_data']
    # start, 開始測試的門檻
    # add, 每次增加的門檻
    # stop, 結束的門檻
    #
    temp_result = []

    # log('start: %s, add: %s, stop: %s' % (start, add, stop))
    for i in np.arange(start, stop, add):
        prediction_result = []
        for j in testing_data:
            if j >= i:
                prediction_result.append(True)
            else:
                prediction_result.append(False)
        # print(real_data,len(real_data))
        # print(prediction_result,len(prediction_result))

        accuracy = metrics.accuracy_score(real_data, prediction_result)
        precision = metrics.precision_score(real_data, prediction_result)
        recall = metrics.recall_score(real_data, prediction_result)
        f1_score = metrics.f1_score(real_data, prediction_result)
        threshold = i
        res = [day,type,accuracy,precision,recall,f1_score,threshold]
        # print(res)
        # print('====' * 20)
        temp_result.append(res)
    return temp_result

def threshold_test(json_file_path,simple_testing=None,tf_idf_testing=None,tf_pdf_testing=None):
    # 預讀資料到記憶體
    json_file = {}
    with open(json_file_path, 'r') as f:
        json_file = json.load(f)

    # 建立一個暫存的list
    # columns=['day', 'type', 'accuracy', 'precision','recall','f1-score','threshold']
    TEMP_RESULT = []

    # analysis
    daily_data = json_file['daily_data']
    for daily in daily_data:
        log('process day %s data' % daily['day'],lvl = 'i')

        TEMP_RESULT_COS = metrics_value(day = daily['day'],type='cos',testing_data = daily['cos'],real_data = daily['real_data'], start = 0.01,add = 0.01,stop = 1)
        TEMP_RESULT.extend(TEMP_RESULT_COS)
        TEMP_RESULT_TF_IDF = metrics_value(day = daily['day'],type='tf_idf',testing_data = daily['tf_idf'],real_data = daily['real_data'], start = 0.01,add = 0.01,stop = 1)
        TEMP_RESULT.extend(TEMP_RESULT_TF_IDF)
        TEMP_RESULT_TF_PDF = metrics_value(day = daily['day'],type='tf_pdf',testing_data = daily['tf_pdf'],real_data = daily['real_data'], start = 0.01,add = 0.01,stop = 1)
        TEMP_RESULT.extend(TEMP_RESULT_TF_PDF)

    log(TEMP_RESULT)
    # 將資料寫到dataframe並且輸出
    df = pandas.DataFrame(TEMP_RESULT,columns=['day', 'type', 'accuracy', 'precision','recall','f1-score','threshold'])
    csv_file_path = os.path.join(os.path.dirname(json_file_path),'analysis.csv')
    df.to_csv(csv_file_path, sep=',', encoding='utf-8')

def main():
    file_path = '/Users/yuhsuan/Desktop/MEMDS/arrange_day_15/'
    temp_file = similuity(file_path)

    # path = 'C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_30\\analysis_temp.json'
    threshold_test(temp_file,simple_testing=(0.1,0.1,1))


if __name__ == '__main__':
    main()
    # import requests
    #
    # url = 'https://www.lnb.com.tw/api/market-place?page=1&per_page=10&sendback=2'
    # res = requests.get(url,verify=False)
    # print(res.json())