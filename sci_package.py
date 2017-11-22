# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 下午11:28
# @Author  : Yuhsuan
# @File    : sci_package.py
# @Software: PyCharm Community Edition

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# test sentence
corpus = [
    'This is the first document.',
    'This is the second second document.',
    'And the third one.',
    'Is this the first document?',
]
#文字轉換為向量
vectorizer = CountVectorizer()
transformer=TfidfTransformer()
# 計算詞頻
tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))

word = vectorizer.get_feature_names()
print(word)
print(tfidf.toarray())
weight=tfidf.toarray()
for i in range(len(weight)):
  print("第",i,"個文件")
  for j in range(len(word)):
    print(word[j],weight[i][j])