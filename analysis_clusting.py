# -*- coding: utf-8 -*-
# @Time    : 2018/3/17 下午 03:54
# @Author  : Yuhsuan
# @File    : analysis_clusting.py
# @Software: PyCharm
import json
import os
import re
import pandas as pd
from log_module import log
from sklearn import metrics


def main():
    answer_file = "arrange_day_0/answer.json"
    answer = {}
    with open(answer_file, 'r') as file:
        answer = json.load(file)

    res = []
    # for i in range(1, 100):
    for i in [17]:
        pre = process_file("arrange_day_0/final_group_file_reference/{}_tfidf.json".format(i))
        log(i, lvl='i')
        res.append(metrics_value(answer, pre))
    df = pd.DataFrame(res)
    # print(df)
    # df.to_csv("arrange_day_0/res_cos.csv", sep=',', encoding='utf-8')


# 計算正確的GROUP
def correct_group():
    path = "arrange_day_0/file_reference.json"
    temp = {}
    source_data = {
        'missile': [],
        'turkish': [],
        'catalan': [],
        'brexit': [],
        'gravitational': [],
        'hk': [],
        'sewol': [],
        'syria': [],
        'crimea': []
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

    with open(path, 'r') as file:
        temp = json.load(file)

    # print(temp)
    for i in temp:
        pattern = '.*day\d+_.*_(.*)_\d+.txt'
        m = re.match(re.compile(pattern), i[1])
        i = i[1]
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

    answer = "arrange_day_0/answer.json"
    # with open(answer, 'w') as file:
    #     json.dump(source_data, file)


# 處理檔案
def process_file(file_path):
    data = {}
    with open(file_path, 'r') as file:
        data = json.load(file)

    # 暫時寄放的，用來記錄每一個Group所屬於的分群與編號
    temp = []

    for group in data:
        # 先判斷裡面的資料應該屬於哪個比較的GROUP
        source_data = {
            'missile': [],
            'turkish': [],
            'catalan': [],
            'brexit': [],
            'gravitational': [],
            'hk': [],
            'sewol': [],
            'syria': [],
            'crimea': []
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

        for i in data[group]:
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
                pass

        log("source_data: %s" % source_data)

        # 按照分類的數量大小進行合併
        lisr = []
        for i in source_data:
            lisr.append([i, len(source_data[i])])
        df = pd.DataFrame(lisr, columns=['type', 'number'])
        df.sort_values(by=['number'], ascending=[False], inplace=True)
        lisr = df['type'].values.tolist()

        les = []
        for i in lisr:
            les.extend(source_data[i])
        temp.append({lisr[0]: les})
    log("temp: %s" % temp)
    group_number = 0
    log("=============================================\n")
    for i in temp:
        log("group %s is: %s" %(group_number,i))
        group_number=group_number+1

    log("=============================================\n")
    system_group = {}

    check_list = ['missile', 'turkish', 'catalan', 'brexit', 'gravitational', 'hk', 'sewol', 'syria', 'crimea']
    for event_num in range(len(check_list)):
        temp_group_list = []
        for i in temp:
            if check_list[event_num] in i:
                temp_group_list.append(i)
        log("temp_group_list: %s" % temp_group_list)
        if len(temp_group_list) == 0:
            system_group[check_list[event_num]] = []
        elif len(temp_group_list) == 1:
            system_group[check_list[event_num]] = temp_group_list[0][check_list[event_num]]
        else:
            # 最多正確的資料
            number = []
            number_count = []
            number_max = []
            for i in range(len(temp_group_list)):
                log("event_num: %s" % event_num)
                number.append(i)
                number_count.append(temp_group_list[i][check_list[event_num]].count(event_num + 1))
                number_max.append(len(temp_group_list[i][check_list[event_num]]))

            select_one = ""
            for j in number:
                if max(number_count) == number_count[j]:
                    select_one = j
            log('{} {} {}'.format(number, number_count, number_max))
            log("select_one: %s" % select_one)
            system_group[check_list[event_num]] = temp_group_list[select_one][check_list[event_num]]
        log("system_group: %s" % system_group)
        log("\n\n")
    return system_group


# 計算相關預測數值
def metrics_value(real_data, system_data):
    check_list = ['missile', 'turkish', 'catalan', 'brexit', 'gravitational', 'hk', 'sewol', 'syria', 'crimea']
    item_number = 1
    res = []
    for event in check_list:
        real_count = len(real_data[event])
        system_count = len(system_data[event])

        # 如果系統的資料比較少
        if real_count > system_count:
            add = [0 for i in range(real_count - system_count)]
            system_data[event].extend(add)
        elif real_count < system_count:
            add = [0 for i in range(system_count - real_count)]
            real_data[event].extend(add)
        else:
            pass

        log(real_data[event])
        log(system_data[event])

        if item_number not in system_data[event]:
            accuracy = 0.0
            precision = 0.0
            recall = 0.0
            f1_score = 0.0
        else:
            log("xxxx")
            accuracy = metrics.accuracy_score(real_data[event], system_data[event])
            precision = metrics.precision_score(real_data[event], system_data[event], average='micro')
            recall = metrics.recall_score(real_data[event], system_data[event], average='micro')
            f1_score = metrics.f1_score(real_data[event], system_data[event], average='micro')
        log('{},{},{},{},{}'.format(event, accuracy, precision, recall, f1_score), lvl='i')
        res.extend([accuracy, precision, recall, f1_score])
        item_number = item_number + 1
    return res


if __name__ == "__main__":
    main()
