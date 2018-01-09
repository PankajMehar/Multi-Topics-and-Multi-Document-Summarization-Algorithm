# -*- coding: utf-8 -*-
# @Time    : 2018/1/9 下午11:24
# @Author  : Yuhsuan
# @File    : generate_all_date.py
# @Software: PyCharm
# 將每天的資料進行文字處理存在news_documents中

from run import *

def main(sources,news_events):
    # 先建立檔案資料夾
    path_is_exists(current_dir + '/news_documents/')

    for source in sources:
        for news_event in news_events:

            # 取得各資料夾內檔案的清單，存到各變數中
            # 因為裡面的檔案命名都是以發生的時間，所以將要的檔案清單用正規表示法做限定
            file_list = get_file_list(current_dir + '/'+source+'/'+news_event, pattern="\d+")

            # 開始計算所有主題內的新聞報導時間，包含開始、結束、報導的總時間(結束-開始)、各報導的檔案＋日期＋第n天報導的混合矩陣
            start_time, end_time, diff_time, matrix = run_days(file_list)

            create_document(matrix, '%s_%s' % (source,news_event))
            format_document(matrix)

if __name__ == '__main__':
    sources = ['CNN', 'NewYorkTimes', 'Theguardian']
    news_events = ['brexit', 'catalan', 'crimea', 'gravitational', 'hk', 'missile', 'sewol', 'syria', 'turkish']

    main(sources,news_events)