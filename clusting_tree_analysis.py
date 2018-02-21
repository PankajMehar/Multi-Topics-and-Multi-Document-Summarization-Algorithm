# -*- coding: utf-8 -*-
# @Time    : 2018/2/21 下午 03:18
# @Author  : Yuhsuan
# @File    : clusting_tree_analysis.py
# @Software: PyCharm
import json

import networkx as nx
import matplotlib.pyplot as plt

from log_module import log

def read_json(json_file_path):
    dict = {}
    with open(json_file_path, "r") as openfile:
        dict = json.load(openfile)
    return dict

def analysis_connection(SOURCE_DATA,threshold):
    # 會先依據每天的資料中，往後找到有關連性的群組
    # 比如第一天有三個群組，第一個群組會根據門檻值去尋找有符合的第一個關聯
    # 找到後就跳出換第二個群
    for single_day in SOURCE_DATA["daily_data"]:
        # 顯示處理第幾天的資料
        log("第幾天的資料: %s" % single_day["day"])
        # 用來記錄共有多少個要比對的資料
        file_info_len = len(single_day["file_info"])
        compare_day = single_day["compare_day"]
        compare_day_len = len(compare_day)
        log("共有幾個群組資料: %s" % file_info_len)
        # 用來儲存比對出來的資料
        single_day_compare_result = ["" for i in range(file_info_len)]

        # 從第一個群組開始找相對應符合門檻的資料
        for source_group in range(file_info_len):
            for compare_daily_data in compare_day:
                compare_file_info_len = len(compare_daily_data["file_info"])
                process_group = compare_daily_data["process_group"]
                process_group_len = len(compare_daily_data["process_group"])

                cos = compare_daily_data["cos"]
                tf_idf = compare_daily_data["tf_idf"]
                tf_pdf = compare_daily_data["tf_pdf"]

                for i in range(process_group_len):
                    if process_group[i][0] == source_group and cos[i]>=threshold:
                        if single_day_compare_result[source_group] == "":
                            single_day_compare_result[source_group] = "Source Day: %s, Source Group: %s, Compare Day: %s, Compare Group: %s" % (single_day["day"],source_group,compare_daily_data["day"],process_group[i][1])

        log(single_day_compare_result,lvl="i")

def draw_tree():
    G = nx.Graph()

    nodes = ["1-0","1-1","1-2","2-1","2-3"]
    edges = [("1-0","1-1"),("1-0","2-3")]
    labels = nodes
    G.add_nodes_from(nodes,labels=labels)
    G.add_edges_from(edges)

    pos = {}
    for i in nodes:
        # pos[i] = [int(i[0]),int(i[2])]
        pos[i] = [(i[0]), (i[2])]
    # pos = nx.get_node_attributes(G, 'pos')
    # pos = nx.spring_layout(G)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    print(pos)
    # nx.draw(G, pos,with_labels=True)

    plt.axis('off')
    plt.show()
    plt.cla()

def main(json_file_path,threshold):
    SOURCE_DATA = read_json(json_file_path)
    RES = analysis_connection(SOURCE_DATA,threshold)

if __name__ == "__main__":
    json_file_path = "C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\clusting_tree_values.json"
    threshold = 0.5
    # main(json_file_path,threshold)
    draw_tree()