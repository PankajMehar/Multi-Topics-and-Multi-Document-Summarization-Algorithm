# -*- coding: utf-8 -*-
# @Time    : 2018/1/10 下午10:27
# @Author  : Yuhsuan
# @File    : main.py
# @Software: PyCharm
import os
from data_downloader import news_creater
from text_processor import *
from data_generator import *

# 產生文字處理與字根還原的資料
def create_stemming_data(news_sources,news_events,output_path):
    for source in news_sources:
        for news_event in news_events:

            # 取得各資料夾內檔案的清單，存到各變數中
            # 因為裡面的檔案命名都是以發生的時間，所以將要的檔案清單用正規表示法做限定
            file_list = get_file_list(current_dir + '/'+source+'/'+news_event, pattern="\d+")

            # 開始計算所有主題內的新聞報導時間，包含開始、結束、報導的總時間(結束-開始)、各報導的檔案＋日期＋第n天報導的混合矩陣
            start_time, end_time, diff_time, matrix = run_days(file_list)

            # create_document(matrix, '%s_%s' % (source,news_event))
            format_document(matrix,output_path)

def main():
    # 根目錄
    ROOT_DIR = os.path.dirname(__file__)
    # 處理後的文字資料路徑
    STEMMING_DATA_DIR = os.path.join(os.path.dirname(__file__),'stemming_data')

    # 執行檔案下載,設定來源路徑, 主題路徑名稱
    SOURCES = ['CNN', 'NewYorkTimes', 'Theguardian']
    NEWS_EVENTS = ['brexit', 'catalan', 'crimea', 'gravitational', 'hk', 'missile', 'sewol', 'syria', 'turkish']

    # 執行檔案下載,設定來源路徑, 主題路徑名稱
    # 測試用資料
    # SOURCES = ['CNN', 'NewYorkTimes']
    # NEWS_EVENTS = ['brexit', 'catalan']

    # # 根據找到的url檔案，將新聞資料抓下來
    # news_creater(sources=SOURCES,file_list=NEWS_EVENTS)
    # # 建立字根資料的主資料夾
    # path_is_exists(STEMMING_DATA_DIR)
    # # 產生文字處理與字根還原的資料
    # create_stemming_data(news_sources=SOURCES,news_events=NEWS_EVENTS,output_path=STEMMING_DATA_DIR)

    # 輸入時間新聞來源，輸出的資料夾，分隔的時間區間
    # 輸出的檔案名稱為 arrange_day_{day}.json
    # 數字0就是指定要以多少天為分割，0代表每天各自分割, 15代表將所有的資料分割成15天
    ARRANGE_DATA_SOURCE = generate_time_data(STEMMING_DATA_DIR,STEMMING_DATA_DIR,0,SOURCES,NEWS_EVENTS)

    # 產生需要分析的資料集
    data_set_folder_name = os.path.basename(ARRANGE_DATA_SOURCE).replace('.json','')
    data_set_folder_path = os.path.join(ROOT_DIR,data_set_folder_name)
    generate_file_from_json(ARRANGE_DATA_SOURCE,data_set_folder_path)
if __name__ =='__main__':
    main()

