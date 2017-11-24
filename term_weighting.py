# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 下午11:25
# @Author  : Yuhsuan
# @File    : term_weighting.py
# @Software: PyCharm Community Edition

import numpy as np

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

    print(np.asarray(word_array))
    tf(word_array)
    return word_array

# 計算tf
def tf(array):
    # 建立資料tf資料陣列
    tf_array=array

    for raw in range(1,len(array)):
        word_cout = sum(array[raw])
        for i in range(len(array[raw])):
            tf_array[raw][i] = array[raw][i]/word_cout
    print(np.asarray(tf_array))

# 計算idf
def idf(array):
    idf_array = array


# 計算tf_idf
def tf_idf(corpus_list):
    res = text_to_vector(corpus_list)
    print(res)

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


