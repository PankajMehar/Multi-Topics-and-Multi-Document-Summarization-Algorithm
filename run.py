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

# 取得資料夾下所有檔案清單
def get_file_list(path,pattern=None):
    log('[get_file_list][start] path: %s, pattern: %s' % (path,pattern), lvl='i')
    file_list = []
    for dir, subdir, files in os.walk(path):
        for file in files:
            if pattern!=None:
                if re.match(pattern,file):
                    file_list.append(os.path.join(dir, file))
            else:
                file_list.append(os.path.join(dir,file))
    log('[get_file_list] list: %s' % str(file_list))
    log('[get_file_list][end] path: %s, pattern: %s' % (path,pattern), lvl='i')
    return file_list

# 輸入兩個時間，計算兩個時間共間隔了幾天
def diff_day(start_day,now):
    log('[diff_day][start]')
    diff = str(datetime.datetime.strptime(now, "%Y%m%d") - datetime.datetime.strptime(start_day, "%Y%m%d"))
    diff = int(re.match("\d+", diff).group(0))
    log('[run_days] start date: %s, end date: %s, diff: %s' % (start_day,now,diff))
    log('[run_days][end]')
    return diff

# 計算最近的日子，最久的日子，日子的差距
def run_days(file_list):
    log('[run_days][start]',lvl='i')
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
    j=0
    for i in story_list:
        dist = '%s%s%s_%s_%s.txt'%(current_dir,'/news_documents/day',i[2],story_name,j)
        copyfile(i[0],dist)
        j=j+1
        log('[create_document] story name: %s, dist: %s' % (story_name, dist))
    log('[create_document][end]', lvl='i')

# 將文件字串格式化
def format_document(story_list):
    # 設定worker的語言
    worker = DocToSG('english')
    for i in story_list:
        print(i[0])
        worker.load_document_common(i[0])

if __name__ =='__main__':
    # 先建立檔案資料夾
    path_is_exists(current_dir + '/news_documents/')

    # 取得各資料夾內檔案的清單，存到各變數中
    # 因為裡面的檔案命名都是以發生的時間，所以將要的檔案清單用正規表示法做限定
    crimea = get_file_list(current_dir+'/source/crimea',pattern = "\d+")
    hk = get_file_list(current_dir+'/source/hk',pattern = "\d+")
    sewol = get_file_list(current_dir+'/source/sewol',pattern = "\d+")

    # 開始計算所有主題內的新聞報導時間，包含開始、結束、報導的總時間(結束-開始)、各報導的檔案＋日期＋第n天報導的混合矩陣
    crimea_start, crimea_end, crimea_diff, crimea_matrix = run_days(crimea)
    hk_start, hk_end, hk_diff, hk_matrix = run_days(hk)
    sewol_start, sewol_end, sewol_diff, sewol_matrix = run_days(sewol)

    # 產生測試文件
    create_document(crimea_matrix,'cr')
    create_document(hk_matrix, 'hk')
    create_document(sewol_matrix, 'se')

    # 產生Sentence Group之類的....

    format_document(hk_matrix)