# -*- coding: utf-8 -*-
# @Time    : 2018/2/21 下午 03:18
# @Author  : Yuhsuan
# @File    : clusting_tree_analysis.py
# @Software: PyCharm
import json
import re

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

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
    nodes = []
    nodes_brexit = []
    nodes_catalan = []
    nodes_crimea = []
    nodes_gravitational = []
    nodes_hk = []
    nodes_missile = []
    nodes_sewol = []
    nodes_syria = []
    nodes_turkish = []

    edges = []

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

        # 用來記錄有多少節點的資料
        for i in range(len(single_day["file_info"])):
            pattern = re.compile(".*_(.*)_\d+.txt")
            m = re.match(pattern,single_day["file_info"][i])
            theme = m.group(1)
            if theme == "brexit":
                nodes_brexit.append(str(single_day["day"])+"-"+str(i))
            elif theme == "catalan":
                nodes_catalan.append(str(single_day["day"])+"-"+str(i))
            elif theme == "crimea":
                nodes_crimea.append(str(single_day["day"])+"-"+str(i))
            elif theme == "gravitational":
                nodes_gravitational.append(str(single_day["day"])+"-"+str(i))
            elif theme == "hk":
                nodes_hk.append(str(single_day["day"])+"-"+str(i))
            elif theme == "missile":
                nodes_missile.append(str(single_day["day"])+"-"+str(i))
            elif theme == "sewol":
                nodes_sewol.append(str(single_day["day"])+"-"+str(i))
            elif theme == "syria":
                nodes_syria.append(str(single_day["day"])+"-"+str(i))
            elif theme == "turkish":
                nodes_turkish.append(str(single_day["day"])+"-"+str(i))
            # nodes.append(str(single_day["day"])+"-"+str(i))

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
                    if process_group[i][0] == source_group and tf_idf[i]>=threshold:
                        if single_day_compare_result[source_group] == "":
                            edges.append((str(single_day["day"])+"-"+str(source_group),str(compare_daily_data["day"])+"-"+str(process_group[i][1])))
                            single_day_compare_result[source_group] = "Source Day: %s, Source Group: %s, Compare Day: %s, Compare Group: %s" % (single_day["day"],source_group,compare_daily_data["day"],process_group[i][1])

        log(single_day_compare_result,lvl="i")

    nodes.append(nodes_brexit)
    nodes.append(nodes_catalan)
    nodes.append(nodes_crimea)
    nodes.append(nodes_gravitational)
    nodes.append(nodes_hk)
    nodes.append(nodes_missile)
    nodes.append(nodes_sewol)
    nodes.append(nodes_syria)
    nodes.append(nodes_turkish)

    # 透過關聯找出分群
    node_list = []
    for i in nodes:
        node_list.extend(i)

    clust_temp = {}
    for i in range(len(node_list)):
        clust_temp[i]=[node_list[i]]

    for relation in edges:
        # 定位第一個元件的位置
        pos1=0
        for i in range(len(node_list)):
            if relation[0] in clust_temp[i]:
                pos1 = i
                break
        # 定位第二個元件的位置
        pos2=0
        for i in range(len(node_list)):
            if relation[1] in clust_temp[i]:
                pos2 = i
                break

        if pos1 != pos2:
            clust_temp[pos1].extend(clust_temp[pos2])
            clust_temp[pos2]=[]
    print(clust_temp)

    clust_res = {}
    id = 0
    for i in range(len(clust_temp)):
        if clust_temp[i]!=[]:
            clust_res[id]=clust_temp[i]
            id=id+1

    for i in range(len(clust_res)):
        clust_res[i].sort()
    print(clust_res)
    return nodes,edges

def draw_tree(nodes, edges):
    # pos = nx.get_node_attributes(G, 'pos')
    # print(pos)
    # nodes = [(1,0),"1-1","1-2","2-1","2-3"]
    # edges = [((1,0),"1-1"),((1,0),"2-3")]
    # labels = nodes
    # G.add_nodes_from(nodes,labels=labels)
    # G.add_edges_from(edges)
    #
    # pos = {}
    # for i in nodes:
    #     # pos[i] = [int(i[0]),int(i[2])]
    #     if type(i) is tuple:
    #         pos[i] = [i[0],i[1]]
    #     else:
    #         pos[i] = [(i[0]), (i[2])]
    # pos = nx.get_node_attributes(G, 'pos')
    # pos = nx.spring_layout(G)
    # nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_nodes(G, pos)
    # nx.draw_networkx_labels(G, pos)

    G = nx.Graph()

    pos = {}

    pattern = "(\d+)\-(\d+)"
    pattern = re.compile(pattern)

    # print("mcolors: %s" % mcolors)
    colors = list(dict(**mcolors.CSS4_COLORS))
    for node in range(len(nodes)):
        color = colors[node*2-2]
        G.add_nodes_from(nodes[node])

        for i in nodes[node]:
            m = re.match(pattern,i)
            if int(m.group(1))%2 == 1:
                pos[i] = [int(m.group(1)),int(m.group(2))*2-0.3]
            else:
                pos[i] = [int(m.group(1)), int(m.group(2))+0.5]

        point = nx.draw_networkx_nodes(G,pos,nodelist=nodes[node],node_color=color)
        point.set_edgecolor('#000000')

    # print(pos)
    G.add_edges_from(edges)

    nx.draw_networkx_edges(G,pos)
    nx.draw_networkx_labels(G,pos)
    # nx.draw(G, pos,with_labels=True)

    fig = plt.gcf()
    fig.set_size_inches(100,20)
    plt.axis('off')
    plt.savefig('file.jpg', dpi=100)
    plt.show()
    plt.cla()

def main(json_file_path,threshold):
    SOURCE_DATA = read_json(json_file_path)
    nodes, edges = analysis_connection(SOURCE_DATA,threshold)
    draw_tree(nodes, edges)

if __name__ == "__main__":
    json_file_path = "C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\clusting_tree_values.json"
    threshold = 0.2
    main(json_file_path,threshold)
