# -*- coding: utf-8 -*-
# @Time    : 2017/11/8 上午10:18
# @Author  : Yuhsuan
# @File    : main.py
# @Software: PyCharm Community Edition
import os
import re
import numpy as np
import datetime
from shutil import copyfile
from doc_to_vector import *
from log_module import log

current_dir = os.getcwd()

# 判斷資料夾是否存在
def path_is_exists(path):
    log('[path_is_exists][start] Path: %s' % path,lvl='i')
    if not os.path.exists(path):
        log('[path_is_exists] Create the folder "%s"' % path)
        os.makedirs(path)
    log('[path_is_exists][end] Path: "%s"' % path, lvl='i')

def generate_time_data(input,output,day,sources,news_events):
    log('[generate_time_data][start]', lvl='i')
    log('[generate_time_data] input: %s, output: %s, day: %s' % (input,output,day), lvl='i')

    # 將所有的檔案全部找出來
    log('[generate_time_data] find all files and merge to one list')
    all_list = []
    for source in sources:
        for news_event in news_events:
            pattern = '.*'+source+'.*'+news_event+'.*'+'\d+'
            file_list = get_file_list(input,pattern = pattern)
            all_list.extend(file_list)
    log('[generate_time_data] all_list:\n%s' % all_list)

    # 找出各事件所包含的資料,
    event_file_list = []
    for news_event in news_events:
        event_dic = {}
        event_dic['event_name'] = news_event

        # 記錄所有相同事件的檔案路徑
        temp_file_path = []

        for file_name in all_list:
            if news_event in file_name:
                temp_file_path.append(file_name)

        # 紀錄每一個路徑的日期
        temp_file_day = []
        for path in temp_file_path:
            file_name = os.path.basename(path)
            file_name = re.match("\d+", file_name).group(0)
            temp_file_day.append(file_name)

        # 開始時間
        start_day = min(list(set(temp_file_day)))
        # 結束時間
        end_day = max(list(set(temp_file_day)))
        # 總發生時間
        diff = diff_day(start_day, end_day)

        event_dic['start_day'] = start_day
        event_dic['end_day'] = end_day
        event_dic['diff_day'] = diff

        # 紀錄路徑，日期，相差時間，來源，事件名稱
        temp_result = []
        for i in range(len(temp_file_path)):
            # 路徑
            file_path = temp_file_path[i]
            # 日期
            file_day = temp_file_day[i]
            # 相差時間
            file_diff = diff_day(start_day,file_day)
            # 來源
            file_source = ''
            for source in sources:
                if source in temp_file_path[i]:
                    file_source = source
            # 事件
            file_event = news_event

            temp_result.append([file_path,file_day,file_diff,file_source,file_event])

        event_dic['file_info'] = temp_result

        # 將資料寫入
        event_file_list.append(event_dic)

    log('[generate_time_data] file info:\n %s' % event_file_list)
    log('[generate_time_data][end]', lvl='i')

# 取得資料夾下所有檔案清單
def get_file_list(path,pattern=None):
    log('[get_file_list][start] path: %s, pattern: %s' % (path,pattern), lvl='i')
    file_list = []
    for dir, subdir, files in os.walk(path):
        log('[get_file_list] dir: %s, subdir: %s, files: %s' % (dir,subdir,files))
        for file in files:
            if pattern!=None:
                if re.findall(pattern,os.path.join(dir,file)):
                    file_list.append(os.path.join(dir, file))
            else:
                file_list.append(os.path.join(dir,file))

    log(file_list)
    file_list.sort()
    log('[get_file_list] list: %s' % str(file_list))
    log('[get_file_list][end] path: %s, pattern: %s' % (path,pattern), lvl='i')
    return file_list

# 輸入兩個時間，計算兩個時間共間隔了幾天
def diff_day(start_day,now):
    log('[diff_day][start]')
    diff = str(datetime.datetime.strptime(now, "%Y%m%d") - datetime.datetime.strptime(start_day, "%Y%m%d"))
    diff = int(re.match("\d+", diff).group(0))
    log('[diff_day] start date: %s, end date: %s, diff: %s' % (start_day,now,diff))
    log('[diff_day][end]')
    return diff

# 計算最近的日子，最久的日子，日子的差距
def run_days(file_list):
    log('[run_days][start]',lvl='i')
    log('[run_days] file_list: %s' % file_list)
    day_list=[]
    tmp = []

    for path in file_list:
        file_name = os.path.basename(path)
        file_name = re.match("\d+",file_name).group(0)
        tmp.append(file_name)

    start_day = min(list(set(tmp)))
    end_day = max(list(set(tmp)))
    diff = diff_day(start_day,end_day)

    for path in file_list:
        file_name = os.path.basename(path)
        day = re.match("\d+",file_name).group(0)
        diff = diff_day(start_day,day)
        day_list.append([path,day,diff])

    log('[run_days] start_day: %s, end_day: %s, diff: %s,\n day_list: %s' % (start_day, end_day, diff, str(day_list)))
    log('[run_days][end]', lvl='i')
    return start_day, end_day, diff, day_list

# 產生新聞文件，並重新命名day_story_number
def create_document(story_list,story_name):
    log('[create_document][start]', lvl='i')
    log('[create_document] story_list: %s\n' % str(story_list))

    j=0 #用來記錄某一個matrix中，共有多少文件
    for i in story_list:
        dist = '%s%s%s_%s_%s.txt'%(current_dir,'/news_documents/day',i[2],story_name,j)
        copyfile(i[0],dist)
        j=j+1
        log('[create_document] story name: %s, dist: %s' % (story_name, dist))
    log('[create_document][end]', lvl='i')

# 將文件字串格式化
def format_document(story_list,path):
    log('[format_document][start]', lvl='i')
    # 設定worker的語言
    worker = DocToSG('english')
    for i in story_list:
        file = ''
        if type(i) is list:
            file = i[0]
        elif type(i) is str:
            file = i
        log('[format_document] process: %s' % str(file))
        worker.load_document_common(file,path)
    log('[format_document][end]', lvl='i')

if __name__ =='__main__':
    # 先建立檔案資料夾
    path_is_exists(current_dir + '/news_documents/')

    # 取得各資料夾內檔案的清單，存到各變數中
    # 因為裡面的檔案命名都是以發生的時間，所以將要的檔案清單用正規表示法做限定
    cnn_crimea = get_file_list(current_dir+'/CNN/crimea',pattern = "\d+")
    cnn_hk = get_file_list(current_dir+'/CNN/hk',pattern = "\d+")
    cnn_sewol = get_file_list(current_dir+'/CNN/sewol',pattern = "\d+")

    the_crimea = get_file_list(current_dir + '/theguardian/crimea', pattern="\d+")
    the_hk = get_file_list(current_dir + '/theguardian/hk', pattern="\d+")
    the_sewol = get_file_list(current_dir + '/theguardian/sewol', pattern="\d+")

    # 開始計算所有主題內的新聞報導時間，包含開始、結束、報導的總時間(結束-開始)、各報導的檔案＋日期＋第n天報導的混合矩陣
    cnn_crimea_start, cnn_crimea_end, cnn_crimea_diff, cnn_crimea_matrix = run_days(cnn_crimea)
    cnn_hk_start, cnn_hk_end, cnn_hk_diff, cnn_hk_matrix = run_days(cnn_hk)
    cnn_sewol_start, cnn_sewol_end, cnn_sewol_diff, cnn_sewol_matrix = run_days(cnn_sewol)

    the_crimea_start, the_crimea_end, the_crimea_diff, the_crimea_matrix = run_days(the_crimea)
    the_hk_start, the_hk_end, the_hk_diff, the_hk_matrix = run_days(the_hk)
    the_sewol_start, the_sewol_end, the_sewol_diff, the_sewol_matrix = run_days(the_sewol)

    # 將原本的檔案，依據各資料夾內的新聞時間做整理
    # 會把資料依據日期做排序(本來應該針對總體時間做時間上的設定)
    create_document(cnn_crimea_matrix,'cnn_cr')
    create_document(cnn_hk_matrix, 'cnn_hk')
    create_document(cnn_sewol_matrix, 'cnn_se')

    create_document(the_crimea_matrix, 'the_cr')
    create_document(the_hk_matrix, 'the_hk')
    create_document(the_sewol_matrix, 'the_se')

    # 產生Sentence Group之類的....
    format_document(cnn_crimea_matrix)
    format_document(cnn_hk_matrix)
    format_document(cnn_sewol_matrix)

    format_document(the_crimea_matrix)
    format_document(the_hk_matrix)
    format_document(the_sewol_matrix)

    # # 將news_documents第一天的資料轉換成文字矩陣
    # day_one_data = [
    #     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_cr_0.txt',
    #     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_cr_1.txt',
    #     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_hk_0.txt',
    #     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_se_0.txt',
    #     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_se_1.txt',
    #     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_cnn_se_2.txt',
    #     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_the_cr_0.txt',
    #     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_the_hk_0.txt',
    #     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_the_se_0.txt',
    #     '/Users/yuhsuan/Desktop/MEMDS/news_documents/day0_the_se_1.txt'
    # ]
    # # 將第一天的資料產生文字矩陣後，放在news_documents_r中
    # format_document(day_one_data)


    