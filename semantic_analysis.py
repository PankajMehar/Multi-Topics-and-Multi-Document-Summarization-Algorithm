# -*- coding: utf-8 -*-
# @Time    : 2018/3/2 下午 03:09
# @Author  : Yuhsuan
# @File    : semantic_analysis.py
# @Software: PyCharm
import json
import re
import os
import time
import pandas as pd
from log_module import log
from doc_to_vector import *
from term_weighting import tf_pdf, cosines, tf_idf, simple

# 畫圖的原件
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

from Pajek import pajek


def main():
    # step1()
    # step2()
    step3()


def step1():
    # 產生各群組的資料，並在最後產生出group_number.json的資料
    DATA = news_data_transformer()


def step2():
    # 根據各群組的資料進行相似度比較, 最後產生group_' + str(group_day) + '_%s.json檔案
    for group_day in range(19):
        DATA = {}
        with open("group_" + str(group_day) + ".json") as file:
            DATA = json.load(file)
        log('group_day: %s' % group_day, lvl='w')
        relation = relation_analysis(DATA, group_day, "tf_pdf")
        # relation = relation_analysis(DATA, group_day, "tf_idf")
        # relation = relation_analysis(DATA, group_day, "simple")


def step3():
    # 根據group_' + str(group_day) + '_%s.json的資料組合
    # 用來產生main_path.json的資料
    for file_number in range(19):
        relation = {}
        with open('group_data/%s/group_%s_tf_pdf.json' % (file_number, file_number), 'r', encoding='utf8') as file:
            relation = json.load(file)
        print(relation)
        log("load file finish")
        res = {}
        for i in range(1, 100):
            directory = os.path.dirname(__file__)
            directory = "/group_data/%s/pajek/" % file_number
            log("get_relation_and_draw start")
            get_relation_and_draw(relation, i / 100, str(i), file_number)
            log("get_relation_and_draw end")
            time.sleep(3)

            data = ""
            file_path = os.path.join(os.path.dirname(__file__), 'group_data/%s/%s.net' % (file_number, i))
            with open(file_path, "r") as file:
                data = file.readlines()
            print(data)
            if "*vertices 0\n" not in data:
                log("pajek start")
                res_ = pajek(str(i), EXE_FILE="C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\pajek\\Pajek.exe",
                             FOLDER="C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\group_data\\%s\\" % file_number).run()
                log("pajek end")
                res[i] = res_
                log(i, lvl='w')
                log(res, lvl='w')
            else:
                log("No result", lvl='w')
                res[i] = {}
                log(i, lvl='w')
                log(res, lvl='w')

        with open("group_data/%s/main_path.json" % file_number, "w") as file:
            json.dump(res, file)

    # # res = ['d0_sg0', 'd3_sg20', 'd0_sg1', 'd0_sg4', 'd0_sg5', 'd0_sg6', 'd0_sg9', 'd0_sg10', 'd0_sg11', 'd0_sg12', 'd0_sg13', 'd0_sg16', 'd0_sg18', 'd0_sg19', 'd0_sg20', 'd0_sg22', 'd0_sg26', 'd0_sg28', 'd0_sg31', 'd0_sg32', 'd0_sg33', 'd0_sg34', 'd0_sg35', 'd0_sg38', 'd0_sg39', 'd0_sg40', 'd0_sg41', 'd4_sg39', 'd6_sg21', 'd8_sg11', 'd14_sg72', 'd15_sg4', 'd16_sg1', 'd16_sg2', 'd16_sg3', 'd16_sg9', 'd16_sg30', 'd16_sg6', 'd16_sg7', 'd16_sg11', 'd16_sg13', 'd16_sg15', 'd16_sg16', 'd16_sg18', 'd16_sg19', 'd16_sg21', 'd16_sg26', 'd16_sg28', 'd16_sg14', 'd16_sg29', 'd16_sg5', 'd16_sg0', 'd16_sg20', 'd16_sg27']
    for file_number in range(0, 19):
        main_path = {}

        with open("group_data/%s/main_path.json" % file_number, "r") as file:
            main_path = json.load(file)

        ref_path = "group_data/%s/group_%s.json" % (file_number, file_number)

        # 確認是否有特定路徑，沒有就建立一個，並將資料儲存在裡面
        main_path_summary_folder = "main_path_summary/"
        main_path_summary_folder = os.path.join(os.path.dirname(__file__), main_path_summary_folder)
        # print(main_path_summary_folder)
        if not os.path.exists(main_path_summary_folder):
            os.mkdir(main_path_summary_folder)

        for i in range(1, 100):
            if main_path[str(i)]:
                res = main_path[str(i)]
                summary = system_summary(res, ref_path)
                # print(summary)
                log("%s,%s" % (file_number, i), lvl="w")
                summary_path = "main_path_summary/%s_%s.txt" % (file_number, i)
                with open(summary_path, 'w', encoding='utf8') as file:
                    file.write(summary)
                # time.sleep(3)


# 補救資料
def rescue_data():
    for file_number in range(0, 18):
        file_path = os.path.join(os.path.dirname(__file__), 'group_data/%s/main_path.json' % (file_number))
        if not os.path.exists(file_path):
            res = {}
            for i in range(1, 100):
                file_path = os.path.join(os.path.dirname(__file__), 'group_data/%s/%s.paj' % (file_number, i))
                if os.path.exists(file_path):
                    p = pajek(str(i), EXE_FILE="C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\pajek\\Pajek.exe",
                              FOLDER="C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\group_data\\%s\\" % file_number)
                    p.analysis_main_path()
                    res[i] = p.MAIN_PATH
                else:
                    res[i] = []

            print(res)

            with open("group_data/%s/main_path.json" % file_number, "w") as file:
                json.dump(res, file)


# 將原始資料做整理成方便使用的格式
def news_data_transformer():
    # 最後分群，依照原始檔案路徑的資料
    final_group_file_path = "arrange_day_0/final_group_file/17.json"
    # 最後分群，依照參考檔案路徑的資料
    final_group_file_reference_path = "arrange_day_0/final_group_file_reference/17.json"

    final_group_file = {}
    final_group_file_reference = {}

    with open(final_group_file_path, "r") as file:
        final_group_file = json.load(file)

    with open(final_group_file_reference_path, "r") as file:
        final_group_file_reference = json.load(file)

    log(final_group_file)

    # 計算有多少個群組
    len_group = len(final_group_file)

    res = []
    # 開始做整理資料格式
    for group_number in range(len_group):
        # 將取得的資料暫存的list
        temp_data_list = []
        for list_number in range(len(final_group_file[str(group_number)])):
            # 定義各欄位資料
            # 原始的檔案路徑
            source_file = ""
            # 參考的檔案路徑
            reference_file = ""
            # 計算後屬於第幾天的資料
            day_number = ""
            # 原始檔案的來源是屬於哪個新聞媒體
            news_srouce = ""
            # 原始檔案的來源是屬於哪個新聞事件
            news_event = ""
            # 發生的時間
            news_event_date = ""
            # 參考檔案中的最後一個第幾天的新聞事件
            news_numer_in_day = ""

            log(final_group_file[str(group_number)][list_number])

            source_file = final_group_file[str(group_number)][list_number].replace(
                "C:/Users/Yuhsuan/Desktop/MEMDS\stemming_data\\",
                "/Users/yu_hsuan_chen/PycharmProjects/MEMDS/").replace("\\", "/")
            reference_file = final_group_file_reference[str(group_number)][list_number]

            log(source_file)
            log(reference_file)

            m1 = re.match(re.compile("(\d+) \d+.txt"), os.path.basename(source_file))
            news_event_date = m1.group(1)
            m2 = re.match(re.compile(".*day(\d+)_(.*)_(.*)_(\d+).txt"), reference_file)
            news_srouce = m2.group(2)
            news_event = m2.group(3)
            day_number = m2.group(1)
            news_numer_in_day = m2.group(4)
            temp_data_list.append(
                [int(group_number), int(day_number), source_file, reference_file, news_srouce, news_event,
                 news_event_date, news_numer_in_day])
        print("group: %s\n%s" % (group_number, temp_data_list))
        print(temp_data_list)

        res.extend(temp_data_list)
    # 儲存dataframe資料並排序
    df = pd.DataFrame(res, columns=["group", "day_number", "source_file", "reference_file", "news_srouce", "news_event",
                                    "news_event_date", "news_numer_in_day"])
    df.sort_values(by=['group', 'day_number'], ascending=[True, True], inplace=True)
    # df.to_csv('data_group_info.csv', sep=',', encoding='utf-8')

    log("開始處理各群組", lvl='W')

    for process_group in range(19):
        log("Group %s" % process_group, lvl='W')
        day_number = list(df.loc[df['group'] == process_group]['day_number'])
        source_file = list(df.loc[df['group'] == process_group]['source_file'])

        # 用來記錄共有多少筆資料
        file_number = len(day_number)

        # 用來記錄群組22內的資料結構-------下面
        GROUP = {}
        GROUP['group_number'] = process_group
        GROUP['source'] = {}
        GROUP['steamming'] = {}
        GROUP['tf_pdf_group_info'] = []
        GROUP['daily_sentence_group_count'] = []
        GROUP['sentence_group'] = []

        last_sg_number = 0
        worker = DocToSG('english')
        for num in range(file_number):
            lines = []
            file = open(source_file[num], 'r', encoding='utf8')
            lines = file.readlines()
            file.close()

            # 計算共讀出多少行數
            line_number = len(lines)
            # sg = "d%s_sg%s" % (day_number[num], i)

            if num == 0:
                for i in range(line_number):
                    sg = "d%s_sg%s" % (day_number[num], i)
                    GROUP['sentence_group'].append(sg)
                    GROUP['source'][sg] = lines[i]
                    GROUP['steamming'][sg] = worker.ProcessText(lines[i]).split(" ")
                    # 為了tf-pdf的日子加上這個屬性
                    GROUP['tf_pdf_group_info'].append(day_number[num])
                last_sg_number = line_number
            if num > 0 and day_number[num] != day_number[num - 1]:
                for i in range(line_number):
                    sg = "d%s_sg%s" % (day_number[num], i)
                    GROUP['sentence_group'].append(sg)
                    GROUP['source'][sg] = lines[i]
                    GROUP['steamming'][sg] = worker.ProcessText(lines[i]).split(" ")
                    # 為了tf-pdf的日子加上這個屬性
                    GROUP['tf_pdf_group_info'].append(day_number[num])
                last_sg_number = line_number
            if num > 0 and day_number[num] == day_number[num - 1]:
                for i in range(line_number):
                    sg = "d%s_sg%s" % (day_number[num], last_sg_number + i)
                    GROUP['sentence_group'].append(sg)
                    GROUP['source'][sg] = lines[i]
                    GROUP['steamming'][sg] = worker.ProcessText(lines[i]).split(" ")
                    # 為了tf-pdf的日子加上這個屬性
                    GROUP['tf_pdf_group_info'].append(day_number[num])
                last_sg_number = line_number + last_sg_number

        items = list(set(GROUP['tf_pdf_group_info']))
        for i in items:
            count = 0
            for j in GROUP['tf_pdf_group_info']:
                if i == j:
                    count = count + 1
            GROUP['daily_sentence_group_count'].append(count)
        print(GROUP)
        with open('group_' + str(process_group) + '.json', 'w', encoding='utf8') as file:
            json.dump(GROUP, file)

    # # 用來記錄群組22內的資料結構-------上面
    return GROUP


def relation_analysis(GROUP, group_day, similarity):
    # TFPDF中用來記錄屬於哪個日子用的list
    corpus_list = []

    for i in GROUP['steamming']:
        corpus_list.append(GROUP['steamming'][i])
    # print(corpus_list)
    log('處理%s' % similarity, lvl='w')

    if similarity == "tf_pdf":
        vect = tf_pdf(corpus_list, GROUP['tf_pdf_group_info'])
    elif similarity == "tf_idf":
        vect = tf_idf(corpus_list)
    elif similarity == "simple":
        vect = simple(corpus_list)
    else:
        vect = simple(corpus_list)

    # 開始針對下一天的資料進行相似度的比較
    log('開始針對下一天的資料進行相似度的比較', lvl='w')
    daily_sentence_group_count = GROUP['daily_sentence_group_count']
    # 先選取要比較的數量,reference_count是前一天的數量,compare_count是後一天的數量

    count_len = len(daily_sentence_group_count)
    last_day_count = 0
    compare_count = 0
    relation = []
    log('start cosing analysis', lvl='w')
    for i in range(count_len):
        log("i: %s, count_len: %s" % (i, count_len), lvl='w')

        if i == count_len - 1:
            pass
        else:
            log("%s * %s" % (daily_sentence_group_count[i], daily_sentence_group_count[i + 1]), lvl='w')
            compare_count = compare_count + daily_sentence_group_count[i]
            reference_count = compare_count + daily_sentence_group_count[i + 1]
            for j in range(1 + last_day_count, 1 + compare_count):
                for k in range(1 + compare_count, 1 + reference_count):
                    res = cosines(vect[j], vect[k])
                    # log("%s,%s,%s" % (GROUP['sentence_group'][j-1],GROUP['sentence_group'][k-1], res), lvl='w')
                    relation.append([GROUP['sentence_group'][j - 1], GROUP['sentence_group'][k - 1], res])
            log("last_day_count: %s, compare_count: %s, reference_count: %s" % (
                1 + last_day_count, 1 + compare_count, 1 + reference_count), lvl='w')
            last_day_count = compare_count

    # log("\n\n\n\n", lvl="i")
    # log(relation,lvl="i")

    relation_json = {}
    relation_json['relation'] = relation

    with open('group_' + str(group_day) + '_%s.json' % similarity, 'w', encoding='utf8') as file:
        json.dump(relation_json, file)

    return relation_json


def get_relation_and_draw(relation, threshold, file_name, file_number):
    edges = []
    nodes = []
    for i in relation['relation']:
        if i[2] >= threshold:
            edges.append((i[0], i[1]))
            nodes.append(i[0])
            nodes.append(i[1])
    # print(nodes,edges)
    G = nx.DiGraph()
    pos = {}

    pattern = "d(\d+)_sg(\d+)"
    pattern = re.compile(pattern)
    log("add_nodes")
    G.add_nodes_from(nodes)
    for node in nodes:
        m = re.match(pattern, node)
        pos[node] = [int(m.group(1)), int(m.group(2))]
    nx.draw_networkx_nodes(G, pos=pos, nodelist=nodes)
    # print(pos)
    # print(nodes)
    log("add edges")
    G.add_edges_from(edges)
    log("draw net")
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    log("write net")
    nx.write_pajek(G, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "group_data/" + str(file_number) + "/" + str(file_name) + ".net"))

    fig = plt.gcf()
    fig.set_size_inches(100, 20)
    plt.axis('off')
    log("save jpg")
    plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "group_data/" + str(file_number) + "/" + str(file_name) + ".png"), dpi=100)
    # plt.show()
    plt.cla()

    # 主路徑分析的操作方法
    # 1. Extract the largest component from the network:
    #     a. Network > Create partition > Component > Weak
    #     b. Operations > Network + Partition > Extract subnetwork > Choose cluster 1;
    # 2. Remove strong components from the largest component:
    #     a. Network > Create partition > Component > Strong
    #     b. Operations > Network + Partition > Shrink network > [use default values]
    # 3. Remove loops:
    #     a. Network > Create new network > Transform > Remove > Loops
    #
    # 4. Create main path (or critical path):
    #     a. Network > Acyclic network > Create weighted > Traversal > SPC
    #     b. Network > Acyclic network > Create (Sub)Network > Main Paths
    # The subsequent choice among the options of Main Path for “> Global Search > Standard”,


def system_summary(sg_list, ref_path):
    # 結果
    summary = ""

    # 比對用的檔案
    with open(ref_path, 'r', encoding='utf8') as file:
        relation = json.load(file)

    for group in sg_list:
        for source_group in relation['source']:
            if group == source_group:
                # print(relation['source'][source_group])
                summary = summary + relation['source'][source_group]
    # print(summary)
    return summary


if __name__ == "__main__":
    main()
