# -*- coding: utf-8 -*-
# @Time    : 2017/9/11 上午11:07
# @Author  : Yuhsuan
# @File    : news_data.py
# @Software: PyCharm Community Edition

# 根據某個檔案內的所有新聞路徑將其資料抓取出來後存擋

from newspaper import Article
import os
import time
import datetime
from log_module import log

# 根據提供的網址，下載檔案
def news_extract(news_url,name=None,source=None):
    log('[news_extract][start]')
    log('[news_extract] name: %s, source: %s, url: %s' % (name,source,news_url))
    try:
        if name == None:
            name = 'test'

        if source == None:
            source = 'test'

        log('[news_extract] URL: %s' % news_url)
        article = Article(news_url, fetch_images=False,)
        log('[news_extract] downloading')
        article.download()
        for i in range(10):
            try:
                article.parse()
                break
            except:
                time.sleep(5)
        log('[news_extract] parsing')
        article.parse()
        time.sleep(3)
        log('[news_extract] inserting')
        # article.build()
        new_content = article.text
        new_content = new_content.strip().split('\n\n')
        text = '\n'.join(new_content)
        text = text.strip()

        authors = article.authors
        date = article.publish_date
        date  = datetime.datetime.strftime(date, '%Y%m%d %H%M%S')
        title = article.title

        if title =='':
            log('[news_extract] Error found: the new has no title, skip this one.', lvl='W')
            log('[news_extract][end]\n')
            return False

        # 避免重複的日期
        file_name = date
        for i in range(40):
            if not os.path.exists(os.curdir+'/%s/%s/' % (source,name)+file_name+'.txt'):
                break
            else:
                fname = file_name.split(' ')
                number = int(fname[1])+1
                file_name = '%s %s' % (fname[0],str(number).zfill(6))

        with open(os.curdir+'/%s/%s/' % (source,name) +file_name+'.txt','a+') as file:
            file.writelines(text)

        result = []
        result.append(file_name)
        result.append(title)
        result.append(news_url)
        log('[news_extract] result: %s' % result)
        log('[news_extract][end]\n')
        return result
    except Exception as e:
        log('[news_extract] Error found: %s skip this one. \nMessage: %s' % (news_url,e),lvl='W')
        log('[news_extract][end]\n')
        return False

# 產生檔案文件
def news_creater(sources,file_list):
    url = []
    temp = []

    # file_list = ['hk','sewol','crimea','test']
    # file_list = ['brexit','catalan','crimea','gravitational','hk','missile','sewol','syria','turkish']
    # sources = ['CNN','NewYorkTimes','Theguardian']

    for folder in file_list:
        for source in sources:
            url=[]
            temp=[]
            if os.path.exists(os.curdir+'/%s/%s/%s_title.txt' % (source,folder,folder)):
                log('pass %s,%s' % (source,folder))
                pass
            else:
                log('start: %s,%s\n' % (source, folder))
                with open(os.curdir+'/%s/%s/%s_title_temp_full.txt' % (source,folder,folder)) as urls:
                    for line in urls.readlines():
                        # print(line)
                        url.append(line.strip())

                # 避免資料中本身有重複的網址
                url = list(set(url))
                log('There are %s urls' % len(url),lvl='I')

                for i in url:
                    log(i)
                    res = news_extract(i,name=folder,source = source)
                    if res != False:
                        temp.append(res)
                temp.sort()
                log('Total: %s, Without Error: %s' % (len(url),len(temp)), lvl='I')
                log('Create news title list file.', lvl ='I')
                for lines in temp:
                    with open(os.curdir+'/%s/%s/%s_title.txt' % (source,folder,folder),'a+') as file:
                        file.writelines(lines[0]+'   '+lines[1]+'   '+lines[2]+'\n')

# 單獨執行時，直接使用的主程式進入點
def main():
    sources = ['CNN', 'NewYorkTimes', 'Theguardian']
    file_list = ['brexit','catalan','crimea','gravitational','hk','missile','sewol','syria','turkish']
    news_creater(sources=sources,file_list=file_list)

if __name__ == '__main__':
    main()