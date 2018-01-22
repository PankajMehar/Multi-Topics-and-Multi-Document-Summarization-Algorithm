# -*- coding: utf-8 -*-
# @Time    : 2018/1/22 下午 12:20
# @Author  : Yuhsuan
# @File    : chart_generator.py
# @Software: PyCharm
# 讀取csv後產生圖檔
import pandas as pd
import numpy as np
import os

def main():
    csv_file_path = 'C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_113\\analysis.csv'
    df = pd.read_csv(csv_file_path, sep=",")
    ana_list = ['cos','tf_idf','tf_pdf']
    for ana_type in ana_list:
        result = []
        for i in range(1,100,1):
            threshold = df['threshold']==(i/100)
            type = df['type']==ana_type
            accuracy = df['accuracy'] >=0
            precision = df['precision'] >= 0
            recall = df['recall'] >= 0
            f1_score = df['f1-score'] >= 0
            temp = df[threshold & type & accuracy & precision & recall & f1_score]
            temp_list = [(i/100),temp['accuracy'].mean(),temp['precision'].mean(),temp['recall'].mean(),temp['f1-score'].mean()]
            result.append(temp_list)
        df2 = pd.DataFrame(result,columns=['threshold','accuracy','precision','recall','f1-score'])
        df2.to_csv(os.path.join(os.path.dirname(csv_file_path),(ana_type+'_average.csv')), sep=',', encoding='utf-8')

if __name__ == '__main__':
    main()