# -*- coding: utf-8 -*-
# @Time    : 2018/3/2 下午 03:09
# @Author  : Yuhsuan
# @File    : semantic_analysis.py
# @Software: PyCharm
import json
import re
import os
import pandas as pd

def main():
    news_data_transformer()

# 將原始資料做整理成方便使用的格式
def news_data_transformer():
    # 最後分群，依照原始檔案路徑的資料
    final_group_file_path = "C://Users//Yuhsuan//Desktop//MEMDS//arrange_day_0//final_group_file.json"
    # 最後分群，依照參考檔案路徑的資料
    final_group_file_reference_path = "C://Users//Yuhsuan//Desktop//MEMDS//arrange_day_0//final_group_file_reference.json"

    final_group_file = {}
    final_group_file_reference = {}

    with open(final_group_file_path,"r") as file:
        final_group_file = json.load(file)

    with open(final_group_file_reference_path,"r") as file:
        final_group_file_reference = json.load(file)

    # 計算有多少個群組
    len_group = len(final_group_file)

    res = []
    # 開始做整理資料格式
    for group_number in range(len_group):
        # 將取得的資料暫存的list
        temp_data_list = []
        for list_number in range(len(final_group_file[str(group_number)])):
            # 定義各欄位資料
            # 原始的檔案路徑
            source_file =""
            # 參考的檔案路徑
            reference_file=""
            # 計算後屬於第幾天的資料
            day_number = ""
            # 原始檔案的來源是屬於哪個新聞媒體
            news_srouce = ""
            # 原始檔案的來源是屬於哪個新聞事件
            news_event = ""
            # 發生的時間
            news_event_date=""
            # 參考檔案中的最後一個第幾天的新聞事件
            news_numer_in_day = ""

            source_file = final_group_file[str(group_number)][list_number]
            reference_file = final_group_file_reference[str(group_number)][list_number]

            m1 = re.match(re.compile("(\d+) \d+.txt"),os.path.basename(source_file))
            news_event_date = m1.group(1)
            m2 = re.match(re.compile(".*day(\d+)_(.*)_(.*)_(\d+).txt"),reference_file)
            news_srouce = m2.group(2)
            news_event = m2.group(3)
            day_number = m2.group(1)
            news_numer_in_day = m2.group(4)
            temp_data_list.append([int(group_number),int(day_number),source_file,reference_file,news_srouce,news_event,news_event_date,news_numer_in_day])
        # print("group: %s\n%s" % (group_number,temp_data_list))
        # print(temp_data_list)

        res.extend(temp_data_list)
    # df = pd.DataFrame(res)
    df = pd.DataFrame(res,columns=["group","day_number","source_file","reference_file","news_srouce","news_event","news_event_date","news_numer_in_day"])
    # print(df)
    df.sort_values(['group', 'day_number'], ascending=[True, True])
    df.to_csv('jupyter.csv', sep=',', encoding='utf-8')

    
if __name__=="__main__":
    main()