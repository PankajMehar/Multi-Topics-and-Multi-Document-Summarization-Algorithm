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
    print(temp)
    for relation in temp:
        # 定位第一個元件的位置
        pos1=0
        for i in range(1,len(dict['file_list'])+1):
            if relation[0] in clust_temp[i]:
                pos1 = i
                break
        # 定位第二個元件的位置
        pos2=0
        for i in range(1,len(dict['file_list'])+1):
            if relation[1] in clust_temp[i]:
                pos2 = i
                break

        if pos1 != pos2:
            clust_temp[pos1].extend(clust_temp[pos2])
            clust_temp[pos2]=[]
    # print(clust_temp)

    group={}
    # 先寫入是哪天的資料
    group['day'] = dict['day']
    group['file_list'] = dict['file_list']
    # 將暫存的資料找出來看誰不是空的就新加進去\
    group['group']={}
    for i in range(1,len(clust_temp)+1):
        if len(clust_temp[i])>0:
            group['group'][len(group['group'])] = clust_temp[i]

    # 計算各點的權重
    group['group_weight']={}
    for i in range(len(group['group'])):

        if len(group['group'][i])==1:
            group['group_weight'][i]=group['group'][i]
        else:
            res = [[],[],[]]
            for node in group['group'][i]:
                weight = 1
                count = 0
                for j in range(len(dict['cos'])):
                    # print(node,group['group'][i])
                    if node in dict['process_day'][j] and dict['cos'][j]>0.25:
                        count=count+1
                        weight = weight * dict['cos'][j]
                res[0].append(node)
                res[1].append(weight)
                res[2].append(count)
            # 比較res中誰最大
            # print('res: %s' % res)
            # 確認count中誰最大
            temp=[]
            for x in range(len(res[2])):
                if max(res[2])==res[2][x]:
                    temp.append(x)
            # print('temp: %s' % temp)

            # 判斷temp中是否有多個資料
            if len(temp)==1:
                group['group_weight'][i]=[res[0][temp[0]]]
            else:
                # 判斷weight中誰大
                temp2 = []
                for y in range(len(res[1])):
                    if max(res[1])==res[1][y]:
                        temp2.append(y)
                # print('temp2: %s' % temp2)
                group['group_weight'][i] = [res[0][temp2[0]]]
                # print(group['group_weight'][i])
    # 將對應的gorup檔案列出來
    # print(group['group_weight'])
    group['group_file'] = {}
    for file_number in group['group_weight']:
        highest_file_number = group['group_weight'][file_number][0]
        # print('highest_file_number: %s' % highest_file_number)
        group['group_file'][file_number] = group['file_list'][highest_file_number-1]
        # print(file_number,group['group_file'][file_number])

    return group

def main(json_file_path,json_output_path):
    dict = data(json_file_path)
    res = []
    for i in dict['daily_data']:
        # print(identify_group(i))
        res.append(identify_group(i))

    with open (json_output_path,'w') as fp:
        # json.dump(res, fp, indent=4, sort_keys=True)
        json.dump(res, fp)
if __name__ == "__main__":
    json_file_path = 'C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\analysis_temp.json'
    json_output_path = 'C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\first_clusting_result.json'
    main(json_file_path,json_output_path)