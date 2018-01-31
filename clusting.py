# -*- coding: utf-8 -*-
# @Time    : 2018/1/31 下午 10:53
# @Author  : Yuhsuan
# @File    : clusting.py
# @Software: PyCharm
import json

def data(json_file_path):
    dict = {}
    with open(json_file_path,'r') as openfile:
        dict = json.load(openfile)
    return dict

def identify_group(dict):
    # 先建立最大群組的資料
    clust_temp = {}
    for i in range(1,len(dict['file_list'])+1):
        clust_temp[i]=[i]

    # 將所有有關聯的資料列表出來
    temp = []
    for i in range(len(dict['cos'])):
        if dict['cos'][i] >0.25:
            temp.append(dict['process_day'][i])

    for relation in temp:
        # 定位第一個元件的位置
        pos1=0
        for i in range(1,len(dict['file_list'])+1):
            if relation[0] in clust_temp[i]:
                pos1 = i
        # 定位第二個元件的位置
        pos2=0
        for i in range(1,len(dict['file_list'])+1):
            if relation[1] in clust_temp[i]:
                pos2 = i

        if pos1 != pos2:
            clust_temp[pos1].extend(clust_temp[pos2])
            clust_temp[pos1]=list(set(clust_temp[pos1]))
            clust_temp[pos2]=[]

    group={}
    # 將暫存的資料找出來看誰不是空的就新加進去
    for i in range(1,len(clust_temp)+1):
        if len(clust_temp[i])>0:
            group[len(group)] = clust_temp[i]

    return group

def main(json_file_path):
    dict = data(json_file_path)
    for i in dict['daily_data']:
        print(identify_group(i))

if __name__ == "__main__":
    json_file_path = 'C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\analysis_temp.json'
    main(json_file_path)