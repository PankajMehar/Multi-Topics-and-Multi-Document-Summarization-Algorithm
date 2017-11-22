# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 下午11:25
# @Author  : Yuhsuan
# @File    : term_weighting.py
# @Software: PyCharm Community Edition

# 轉換成字詞向量
def text_to_vector(corpus_list):
    # 產生獨立字詞
    word_list = []
    for i in range(len(corpus_list)):
        word_list = word_list+corpus_list[i]
    # 轉成小寫文字
    word_list = [word.lower() for word in word_list]
    word_list = list(set(word_list))

    # # 比對第一筆資料
    # for i in range(len(corpus_list)):
    #     for j in range(len(corpus_list[i])):
    return word_list

# 計算tf
def tf():
    pass

# 計算idf
def idf():
    pass

# 計算tf_idf
def tf_idf(corpus_list):
    res = text_to_vector(corpus_list)
    print(res)

def main():
    corpus =[
        ["This","is","the","first","document"],
        ["This","is","the","second","second","document"],
        ["And","the","third","one"],
        ["Is","this","the","first","document"],
    ]

    tf_idf(corpus)

if __name__=="__main__":
    main()


