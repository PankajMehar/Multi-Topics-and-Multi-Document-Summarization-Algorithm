# -*- coding: utf-8 -*-
# @Time    : 2017/9/11 上午11:07
# @Author  : Yuhsuan
# @File    : news_data.py
# @Software: PyCharm Community Edition

from newspaper import Article,fulltext
import requests
from lxml import html

def news_extract(news_url):
    article = Article(news_url, fetch_images=False,)
    article.download()
    article.parse()
    # article.build()
    text = article.text
    authors = article.authors
    date = article.publish_date
    title = article.title
    article.nlp()
    summary = article.summary
    print(text)
    print("========================================================")
    print(summary)
    print("========================================================")
    # print(article.meta_data)
    #
    # print(title)
    # print(authors)


source = 'http://edition.cnn.com/2014/03/27/sport/brooklyn-nets-owner-russia/index.html'
news_extract(source)


url = 'http://newspaper-demo.herokuapp.com/articles/show?url_to_clean='+source
res = requests.get(url=url)
tree = html.fromstring(res.content)
txt = tree.xpath('/html/body/section/div/div/table/tbody/tr[3]/td[2]/text()')
print(txt)
