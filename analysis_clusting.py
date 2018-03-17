# -*- coding: utf-8 -*-
# @Time    : 2018/3/17 下午 03:54
# @Author  : Yuhsuan
# @File    : analysis_clusting.py
# @Software: PyCharm
import json
import os
import re

def main():
    answer_file = r"C:\Users\Yuhsuan\Desktop\MEMDS\arrange_day_0\answer.json"
    answer = {}
    with open(answer_file,'r') as file:
        answer = json.load(file)

# 計算正確的GROUP
def correct_group():
    path = r"C:\Users\Yuhsuan\Desktop\MEMDS\arrange_day_0\file_reference.json"
    temp = {}
    source_data = {
        'missile':[],
        'turkish':[],
        'catalan':[],
        'brexit':[],
        'gravitational':[],
        'hk':[],
        'sewol':[],
        'syria':[],
        'crimea':[]
    }

    missile = source_data['missile']
    turkish = source_data['turkish']
    catalan = source_data['catalan']
    brexit = source_data['brexit']
    gravitational = source_data['gravitational']
    hk = source_data['hk']
    sewol = source_data['sewol']
    syria = source_data['syria']
    crimea = source_data['crimea']

    with open(path,'r') as file:
        temp = json.load(file)

    # print(temp)
    for i in temp:
        pattern = '.*day\d+_.*_(.*)_\d+.txt'
        m = re.match(re.compile(pattern),i[1])
        i=i[1]
        if 'missile' in i:
            missile.append(1)
        elif "turkish" in i:
            turkish.append(2)
        elif "catalan" in i:
            catalan.append(3)
        elif "brexit" in i:
            brexit.append(4)
        elif "gravitational" in i:
            gravitational.append(5)
        elif "hk" in i:
            hk.append(6)
        elif "sewol" in i:
            sewol.append(7)
        elif "syria" in i:
            syria.append(8)
        elif "crimea" in i:
            crimea.append(9)
        else:
            break

    answer = r"C:\Users\Yuhsuan\Desktop\MEMDS\arrange_day_0\answer.json"
    with open(answer,'w') as file:
        json.dump(source_data,file)

# 處理檔案
def process_file(file_path):


if __name__ == "__main__":
    main()