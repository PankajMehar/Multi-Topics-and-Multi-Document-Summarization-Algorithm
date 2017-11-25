# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 下午11:25
# @Author  : Yuhsuan
# @File    : term_weighting.py
# @Software: PyCharm Community Edition

import numpy as np
from log_module import log

# 轉換成字詞向量
def text_to_vector(corpus_list):
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
    return word_array

# 計算tf
def _tf(array):
    # 建立資料tf資料陣列
    tf_array=array

    log("tf_array:\n" + str(tf_array))
    log("array:\n" + str(array))

    for raw in range(1,len(tf_array)):
        word_cout = sum(tf_array[raw])
        for i in range(len(tf_array[raw])):
            # 這行會導致變數被污染
            tf_array[raw][i] = tf_array[raw][i]/word_cout
    # print(np.asarray(tf_array))
    log("tf_array:\n"+str(tf_array))
    log("array:\n"+str(array))

# 計算idf
def _idf(array):
    # 建立資料idf陣列資料
    idf_array = array
    # 總文件數
    file_count = len(array)
    # 先進行轉置
    array = [[row[i] for row in array] for i in range(len(array[0]))]
    print(np.asarray(idf_array))

# 計算tf_idf
def tf_idf(corpus_list):
    vector = text_to_vector(corpus_list)
    log(vector)
    print("=======================\n")
    _tf(vector)
    # print("=======================\n")
    # idf(vector)



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