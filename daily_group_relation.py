# -*- coding: utf-8 -*-
# @Time    : 2018/2/5 下午 03:48
# @Author  : Yuhsuan
# @File    : daily_group_relation.py
# @Software: PyCharm

"""
將daily_data_clusting.py處理出來的每天各群體中所代表的資料，進行跨天的分群分析
'C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\first_clusting_result.json'
目標是將這些相似度資料進行分析成下面格式
{
    "max_day": 113,
    "daily_data": [{
        "day": 0,
        "file_info":[]
        "compare_day": [
            {
                "day": 1,
                "file_info":[各群所代表的檔案],
                "process_group": [[第0天的group,第1天的group]],
                "cos": [相似度,...],
                "tf_idf": [相似度,...],
                "tf_pdf": [相似度,...]
            },
            {
                "day": 2,
                "file_info":[各群所代表的檔案],
                "process_group": [[第0天的group,第2天的group]],
                "cos": [相似度,...],
                "tf_idf": [相似度,...],
                "tf_pdf": [相似度,...]
            }
        ]
    }]
}
"""

import json

from log_module import log
from term_weighting import *

def main():
    # 先讀檔案
    json_input_path = 'C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\first_clusting_result.json'

    SOURCE_DATA = {}
    with open(json_input_path, 'r') as openfile:
        SOURCE_DATA = json.load(openfile)

    # 定義最後輸出的目標資料名稱
    OUTPUT_DATA={}

    # 從來源中可以取得最大的資料筆數
    TOTAL_SOURCE_LEN = len(SOURCE_DATA)

    # 先取得最大天數
    # 因為是list, 取得最大資料後要-1才可以得到正確的list位置
    OUTPUT_DATA['max_day'] = SOURCE_DATA[TOTAL_SOURCE_LEN-1]['day']

    # 建立daily_data的結構
    OUTPUT_DATA['daily_data'] = []
    daily_data = OUTPUT_DATA['daily_data']

    # 建立每天的資料"day": 0,....
    for process_day in range(TOTAL_SOURCE_LEN):
        # 預計輸出的資料格式
        output_temp = {}
        # 取得的資料格式
        source_temp = {}

        #day的資料
        source_temp = SOURCE_DATA[process_day]
        output_temp['day'] = source_temp['day']

        # file_info的資料
        output_temp['file_info'] = [source_temp['group_file'][i] for i in source_temp['group_file']]

        # compare_day的資料
        output_temp['compare_day'] = []
        compare_day = output_temp['compare_day']

        # 這邊要開始做compare_day的小迴圈
        for compare_day_num in range(process_day+1,TOTAL_SOURCE_LEN):
            # 建立"compare_day":的結構
            compare_day_temp = {}
            compare_day_temp['day'] = SOURCE_DATA[compare_day_num]['day']
            compare_day_temp['file_info'] = [SOURCE_DATA[compare_day_num]['group_file'][i] for i in SOURCE_DATA[compare_day_num]['group_file']]

            compare_day.append(compare_day_temp)
        daily_data.append(output_temp)


    log(OUTPUT_DATA, lvl='i')

if __name__ == '__main__':
    main()