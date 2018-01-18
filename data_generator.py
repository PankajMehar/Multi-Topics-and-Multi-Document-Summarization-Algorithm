# -*- coding: utf-8 -*-
# @Time    : 2018/1/18 下午 01:35
# @Author  : Yuhsuan
# @File    : data_generator.py
# @Software: PyCharm
# 用來產生需要的分析資料

import os
import json
from shutil import copyfile

# 自訂功能
from text_processor import path_is_exists
from log_module import log

def generate_file_from_json(source_json_file,output_folder):
    # 先建立輸出資料夾
    path_is_exists(output_folder)

    # 先確輸入的檔案路徑是否存在
    if os.path.exists(source_json_file):
        # 將json檔案資料讀出，並轉為dict
        json_file = {}
        with open(source_json_file, 'r') as f:
            json_file = json.load(f)

        # 把dict中的資料輸出到預設的資料夾中
        for news_event in json_file:
            file_infos = news_event['file_info']
            # 紀錄共有多少筆資料
            j=0
            for file_info in file_infos:
                j=j+1
                # 複製的來源
                copy_source = file_info[0]
                # 複製的目標地
                # ('.*day(\d+)_(.*)_(.*)_.*.txt',i)
                copy_dist_file_name = 'day%s_%s_%s_%s.txt' % (file_info[5],file_info[3],file_info[4],j)
                copy_dist_file_path = os.path.join(output_folder,copy_dist_file_name)
                copyfile(copy_source,copy_dist_file_path)
