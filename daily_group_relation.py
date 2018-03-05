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
import re
import json

from log_module import log
from term_weighting import simple, cosines, tf_idf, tf_pdf

def document_to_word_list(file_path_list):
    """
    Description:
        用來將輸入的檔案list轉換成各檔案中所包含的文字list

    Args:
        file_path_list: 要進行轉換的檔案路徑們

    Returns:
        words_matrix: 是個二維陣列，[[很多文字],[很多文字]]
    """

    words_matrix = []
    for file_path in file_path_list:
        with open(file_path,'r',encoding='utf8') as file:
            words = file.readline().strip().split(' ')
        words_matrix.append(words)
    return words_matrix

def process_group_info(daily_data_file_info,compare_day_file_info):
    """
    Description:
        用來計算主要的檔案與被比對的檔案們之間的排列組合

    Args:
        daily_data_file_info: 主要的檔案，是從output_temp['file_info']來的
        compare_day_file_info: 比對的檔案，compare_day_temp['file_info']來的

    Returns:
        process_group: 是個二維陣列，[[第0天的group,第1天的group]]
        daily_data_len: 主要的檔案長度
        compare_day_len: 比對的檔案長度
    """
    log("daily_data_file_info: %s" % daily_data_file_info)
    log("compare_day_file_info: %s" % compare_day_file_info)

    process_group = []
    daily_data_len = len(daily_data_file_info)
    compare_day_len = len(compare_day_file_info)
    for i in range(daily_data_len):
        for j in range(compare_day_len):
            process_group.append([i,j])
    return process_group,daily_data_len,compare_day_len

def words_matrix_cosine_compare(words_matrix,daily_data_len,compare_day_len):
    """
    Description:
        用來計算各group的cosine值

    Args:
        words_matrix: 整個文字矩陣的數量資料
        daily_data_file_info: 主要的檔案，是從output_temp['file_info']來的
        compare_day_file_info: 比對的檔案，compare_day_temp['file_info']來的

    Returns:
        result: 將所有的cosin資料形成的一維陣列
    """
    result = []
    # 因為會多出第一列是所有的文字資料，所以計算的時候要扣除第一行
    for i in range(1, daily_data_len+1):
        for j in range(1+daily_data_len,compare_day_len+daily_data_len+1):
            result.append(cosines(words_matrix[i],words_matrix[j]))
    return result

def words_matrix_tf_idf_compare(words_matrix, daily_data_len, compare_day_len):
    """
    Description:
        用來計算各group的tf_idf值

    Args:
        words_matrix: 整個文字矩陣的數量資料
        daily_data_file_info: 主要的檔案，是從output_temp['file_info']來的
        compare_day_file_info: 比對的檔案，compare_day_temp['file_info']來的

    Returns:
        result: 將所有的tf_idf資料形成的一維陣列
    """
    result = []
    words_matrix = tf_idf(words_matrix)
    log(words_matrix)
    # 因為會多出第一列是所有的文字資料，所以計算的時候要扣除第一行
    for i in range(1, daily_data_len+1):
        for j in range(1+daily_data_len,compare_day_len+daily_data_len+1):
            result.append(cosines(words_matrix[i],words_matrix[j]))
    return result

def words_matrix_tf_pdf_compare(words_matrix, daily_data_len, compare_day_len,channel_list):
    result = []
    words_matrix = tf_pdf(words_matrix, channel_list)
    log(words_matrix)
    # 因為會多出第一列是所有的文字資料，所以計算的時候要扣除第一行
    for i in range(1, daily_data_len+1):
        for j in range(1+daily_data_len,compare_day_len+daily_data_len+1):
            result.append(cosines(words_matrix[i], words_matrix[j]))
    return result

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
        log("process_day: %s" % process_day, lvl='C')
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
            log("compare_day_num: %s" % compare_day_num, lvl='C')
            # 建立"compare_day":的結構
            compare_day_temp = {}
            compare_day_temp['day'] = SOURCE_DATA[compare_day_num]['day']
            compare_day_temp['file_info'] = [SOURCE_DATA[compare_day_num]['group_file'][i] for i in SOURCE_DATA[compare_day_num]['group_file']]
            # 因為直接計算出兩個比較天的各自group數量，所以記得要接三個參數
            compare_day_temp['process_group'], daily_data_len, compare_day_len = process_group_info(output_temp['file_info'],compare_day_temp['file_info'])

            # 用來記錄每次執行的檔案名字們
            file_list=[]
            file_list.extend(output_temp['file_info'])
            file_list.extend(compare_day_temp['file_info'])
            log("file_list: %s" % file_list )

            # 用來處理檔案內所有的source來源
            # /Users/yuhsuan/Desktop/MEMDS/arrange_day_0/day0_CNN_missile_1.txt
            channel_list_temp = []
            channel_list = []
            pattern = re.compile(".*day\d+_(.*)_.*_.*txt")
            for file_path in file_list:
                m = re.match(pattern,file_path)
                channel_list_temp.append(m.group(1))
            source = list(set(channel_list_temp))
            for i in channel_list_temp:
                for j in range(len(source)):
                    if i == source[j]:
                        channel_list.append(j + 1)
                        break

            # 開始做文字的矩陣的轉換
            words_matrix_temp = document_to_word_list(file_list)
            words_matrix = simple(words_matrix_temp)

            # 進行cosine的相似度比較
            compare_day_temp['cos'] = words_matrix_cosine_compare(words_matrix, daily_data_len, compare_day_len)
            compare_day_temp['tf_idf'] = words_matrix_tf_idf_compare(words_matrix_temp, daily_data_len, compare_day_len)
            # print(daily_data_len, compare_day_len,channel_list)
            compare_day_temp['tf_pdf'] = words_matrix_tf_pdf_compare(words_matrix_temp, daily_data_len, compare_day_len,channel_list)

            compare_day.append(compare_day_temp)
        daily_data.append(output_temp)

    # OUTPUT_DATA = json.dumps(OUTPUT_DATA, indent=4, sort_keys=True, ensure_ascii=False)
    log(OUTPUT_DATA, lvl='i')

    json_input_path = 'C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\clusting_tree_values.json'
    with open(json_input_path, 'w') as outfile:
        json.dump(OUTPUT_DATA, outfile)

if __name__ == '__main__':
    main()