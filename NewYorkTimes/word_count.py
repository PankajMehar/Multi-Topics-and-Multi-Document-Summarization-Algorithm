# -*- coding: utf-8 -*-
# @Time    : 2018/6/23 下午 03:48
# @Author  : Yuhsuan
# @File    : word_count.py
# @Software: PyCharm

import os
import csv
import re

# all folders
folders = ['brexit',
           'catalan',
           'crimea',
           'gravitational',
           'hk',
           'missile',
           'sewol',
           'syria',
           'turkish']

def summary_files(folder_path):
    files = os.listdir(folder_path)
    file_list =[]
    for file in files:
        if re.match("\d+ \d+.txt",file):
            file_list.append(file)
    return file_list


def words(file):
    lines = []
    with open(file,"r",encoding="utf-8") as file:
        lines = file.readlines()

    line_count = 0
    word_count = 0
    for line in lines:
        if line != '\n':
            line_count +=1
            word_count = word_count + len(line.split(' '))
    return word_count, line_count

def main():
    for folder in folders:
        file_list = summary_files(folder)
        result = []
        total_words = 0
        total_lines = 0
        for file in file_list:
            word_count,line_count = words(os.path.join(folder,file))
            result_line = [file,word_count,line_count]
            total_words = total_words + word_count
            total_lines = total_lines + line_count
            result.append(result_line)
        with open("total_count.txt","a") as file:
            file.write("%s %s %s\n" % (folder,total_words,total_lines))

        with open(folder+".csv", 'w') as file:
            spamwriter = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerows(result)

if __name__ == '__main__':
    main()