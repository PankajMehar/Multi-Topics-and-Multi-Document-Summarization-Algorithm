# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 下午11:25
# @Author  : Yuhsuan
# @File    : term_weighting.py
# @Software: PyCharm Community Edition

import numpy as np
import copy
import math
from log_module import log

# 轉換成字詞向量
def text_to_vector(corpus_list):
    log("[text_to_vector][start]",lvl="i")
    # 產生獨立字詞
    word_list = []
    for i in range(len(corpus_list)):
        word_list = word_list+corpus_list[i]
    # 轉成小寫文字
    word_list = [word.lower() for word in word_list]
    # 將文字按照順序排序
    word_list = sorted(list(set(word_list)))

    # 建立空的array給字詞計算的結果
    word_array = []
    word_array.append(word_list)

    # 從第一列資料開始比對
    for raw in range(len(corpus_list)):
        temp=[]
        # 先挑第一個字出來比對
        for word in range(len(word_list)):
            # 將原本的資料通通轉小寫,避免後面發生大小寫判別問題
            corpus_list[raw] = [word.lower() for word in corpus_list[raw]]
            temp.append(corpus_list[raw].count(word_list[word]))
        word_array.append(temp)
    log("[text_to_vector]\n%s" % np.asarray(word_array), lvl="i")
    log("[text_to_vector][end]\n", lvl="i")
    return word_array

# 計算tf
def tf(array):
    log("[tf][start]",lvl="i")
    # 建立資料tf資料陣列
    tf_array=copy.deepcopy(array)

    for raw in range(1,len(tf_array)):
        word_cout = sum(tf_array[raw])
        for i in range(len(tf_array[raw])):
            tf_array[raw][i] = tf_array[raw][i]/word_cout
    log("[tf] \n%s" % np.asarray(tf_array), lvl="i")
    log("[tf][end]\n",lvl="i")

    return tf_array

# 計算idf
def idf(array):
    log("[idf][start]",lvl="i")
    # 建立資料idf陣列資料
    idf_array = copy.deepcopy(array)
    # 建立暫存的資料做idf運算
    temp = copy.deepcopy(idf_array)
    # 總文件數
    file_count = len(idf_array)-1
    word_count = len(idf_array[0])
    # 先進行轉置
    # temp = [[row[i] for row in temp] for i in range(len(temp[0]))]
    # 顯示暫存資料的內容，確定已經轉置
    log(np.asarray(temp))

    for word in range(word_count):
        word_in_file = 0
        for i in range(1,file_count+1):
            if int(idf_array[i][word]) > 0:
                word_in_file = word_in_file+1

        for j in range(1,file_count+1):
            # normal
            temp[j][word] = abs(np.log10(file_count/(1+word_in_file)))

    log("[idf] \n%s" % np.asarray(temp), lvl="i")
    log("[idf][end]\n", lvl="i")
    return temp

# 計算pdf
def pdf(array,group):
    log("[pdf][start]",lvl="i")
    log("array: %s" % array)
    log("group: %s" % group)
    # 檢查哪些是同一個群組的
    # 根據不同的Group將字詞資料做合併
    group_item = list(set(group))
    log(group_item)
    # 合併的Group array
    group_array = []
    group_array.append(array[0])
    # 計算出各group的數量存成group_doc_count
    group_doc_count = []
    for i in group_item:
        temp_group_list = np.zeros(len(array[0]))
        temp_group_count = 0
        for number in range(len(group)):
            if i == group[number]:
                temp_group_count = temp_group_count+1
                temp_group_list = np.add(temp_group_list,array[number+1])
        temp_group_list = temp_group_list.tolist()
        group_array.append(temp_group_list)
        group_doc_count.append(temp_group_count)
        log((temp_group_list,temp_group_count))
    log("group_array: %s" % group_array)
    log("group_doc_count: %s" % group_doc_count)

    # 開始計算各pdf值
    pdf_array = []
    pdf_array.append(array[0])
    log("pdf_array: %s" % pdf_array)

    # 先計算分母
    denominator = []
    for i in range(1,len(group_array)):
        m_sum = 0
        for j in group_array[i]:
            m_sum = m_sum + pow(j,2)
        m_sum = np.sqrt(m_sum)
        denominator.append(1/m_sum)

    log("denominator: %s"% denominator)

    temp = []
    for j  in range(len(group_array[1])):
        # 計算出來的PDF
        pdf = 0
        for i in range(len(group_item)):
            pdf = pdf+(denominator[i] * np.exp(group_array[i+1][j]/group_doc_count[i]))
            log("pdf: %s, %s * np.exp( %s / %s )" % (pdf,denominator[i],group_array[i+1][j],group_doc_count[i]))
        log("word: %s, pdf: %s" % (group_array[0][j],pdf))
        temp.append(pdf)
    pdf_array.append(temp)

    log("[pdf] \n%s" % np.asarray(pdf_array), lvl="i")
    log("[pdf][end]\n",lvl="i")
    return pdf_array

# 單純要用來計算兩字詞的距離
def simple(corpus_list):
    log("[simple][start]", lvl="i")
    vector = text_to_vector(corpus_list)
    simple_vect = copy.deepcopy(vector)
    log("[simple][end]", lvl="i")
    return simple_vect

# 計算tf_idf
def tf_idf(corpus_list):
    log("[tf_idf][start]", lvl="i")
    vector = text_to_vector(corpus_list)
    tf_vect = tf(vector)
    idf_vect = idf(vector)

    tf_idf_vect = copy.deepcopy(vector)

    for i in range(1,len(tf_idf_vect)):
        for j in range(len(tf_idf_vect[i])):
            # log((i,j))
            tf_idf_vect[i][j] = tf_vect[i][j]*idf_vect[i][j]
            # log((tf_vect[i][j],idf_vect[i][j],tf_idf_veict[i][j]))

    log("[tf_idf] \n%s" % np.asarray(tf_idf_vect), lvl="i")
    log("[tf_idf][end]\n", lvl="i")
    return tf_idf_vect

# 計算tf_pdf
# corpus_list是原本的文字矩陣，group_info是記錄哪些文件是相同的
# group_info中的元素如果數字一樣代表是同一個Group
def tf_pdf(corpus_list,group_info):
    log("[tf_pdf][start]", lvl ="i")
    # 先判斷進來的矩陣與group資料是否相同
    if len(corpus_list)==len(group_info):
        vector = text_to_vector(corpus_list)
        tf_vect = tf(vector)
        pdf_vect = pdf(vector,group_info)

        tf_pdf_vect = copy.deepcopy(vector)

        for i in range(1,len(tf_pdf_vect)):
            for j in range(len(tf_pdf_vect[i])):
                tf_pdf_vect[i][j] = tf_vect[i][j]*pdf_vect[1][j]
                # log((tf_vect[i][j],pdf_vect[1][j],tf_pdf_vect[i][j]))

        log("[tf_pdf] \n%s" % np.asarray(tf_pdf_vect))
        log("[tf_pdf][end]\n", lvl="i")
        return tf_pdf_vect
    else:
        log("[tf_pdf] The document count is not match with group count, please check again.")
        empty = []
        log("[tf_pdf][end]\n", lvl="i")
        return empty


# 計算cosine
# 直接用tf*idf或tf*pdf，代入整個cosine
def cosines(list_a,list_b):
    log("[cosines][start]", lvl="i")
    if len(list_a)==len(list_b):
        # 分母
        top = 0
        # 左分子
        btn_left = 0
        # 右分子
        btn_right = 0

        log("%s, %s" % (list_a, list_b))
        for i in range(len(list_a)):
            top = top + (list_a[i]*list_b[i])
            btn_left = btn_left + pow(list_a[i],2)
            btn_right = btn_right + pow(list_b[i],2)
        cosine = top / (math.sqrt(btn_left)*math.sqrt(btn_right))
        log("[cosines] cosine: %s" % cosine,lvl='i')
        log("[cosines][end]", lvl="i")
        return cosine
    else:
        # 如果兩個list大小不一樣就回傳-1
        log("[cosines] length of lists are not the same.")
        log("[cosines][end]", lvl="i")
        return -1

def main():
    #一班陣列測試資料
    corpus_simaple = [
        ['a','a','b'],
        ['b','a','a']
    ]
    res = simple(corpus_simaple)
    print(res)

    for i in range(1,len(res)):
        for j in range(1,i):
            log("%s, %s" % (i,j))
            print(cosines(res[i],res[j]))

    # tf-idf測試資料
    corpus_tf_idf = [
        ["this", "is", "a", "a","sample"],
        ["this","is","another","another","example","example","example"],
    ]

    # tf-pdf測試資料
    corpus_tf_pdf = [
        ["cat","pet"],
        ["fish","pet"],
        ["cat","eat","fish"],
        ["fish","die"]
    ]
    group = [1,1,2,2]

    tf_idf(corpus_tf_idf)
    log('='*40,lvl='i')
    res = tf_pdf(corpus_tf_pdf,group)

    for i in range(1,len(res)):
        for j in range(1,i):
            log("%s, %s" % (i,j))
            cosines(res[i],res[j])

# 計算混淆矩陣
# http://blog.csdn.net/quiet_girl/article/details/70830796

if __name__=="__main__":
    main()