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
    word_list = list(set(word_list))

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
    log("[text_to_vector]\n%s" % np.asarray(word_array))
    log("[text_to_vector][end]", lvl="i")
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
    log("[tf] \n%s" % np.asarray(tf_array))
    log("[tf][end]",lvl="i")

# 計算idf
def idf(array):
    log("[idf][start]",lvl="i")
    # 建立資料idf陣列資料
    idf_array = copy.deepcopy(array)
    # 建立暫存的資料做idf運算
    temp = copy.deepcopy(idf_array)
    # 總文件數
    file_count = len(array)
    word_count = len(array[0])
    # 先進行轉置
    temp = [[row[i] for row in temp] for i in range(len(temp[0]))]
    # 顯示暫存資料的內容，確定已經轉置
    log(np.asarray(temp))

    for word in range(word_count):
        word_in_file = 0
        for i in range(1,word):
            if word_count[word][i] > 0:
                word_in_file = word_in_file+1
        log(word_in_file,word_count)
        # idf_value = math.log10(word_in_file/word_count)
        idf_value = word_in_file
        for i in range(1,word):
            temp[i][word] = idf_value
    log("[idf] %s\n" % np.asarray(temp))
    log("[idf][end]", lvl="i")

# 計算tf_idf
def tf_idf(corpus_list):
    vector = text_to_vector(corpus_list)
    tf(vector)
    idf(vector)



def main():
    corpus =[
        ["This","is","the","first","document"],
        ["this","is","the","second","second","document"],
        ["and","the","third","one"],
        ["is","this","the","first","document"],
    ]

    tf_idf(corpus)

if __name__=="__main__":
    main()