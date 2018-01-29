# -*- coding: utf-8 -*-
# @Time    : 2018/1/29 下午 06:20
# @Author  : Yuhsuan
# @File    : relation_graph.py
# @Software: PyCharm

'''
讀取每個分析資料，並將其群組做視覺化
'''
import json

import networkx as nx
from networkx.algorithms import approximation
import matplotlib.pyplot as plt

from log_module import log

def data():
    json_file_path ='C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\arrange_day_0\\analysis_temp.json'

    dict = {}
    with open(json_file_path,'r') as openfile:
        dict = json.load(openfile)
    return dict

def threshold(dict):
    # print(dict['daily_data'][0])
    for days in [1]:
    # for days in range(len(dict['daily_data'])):
        data = dict['daily_data'][days]

        log('days: %s' % days)
        log('file_list:')
        for i in data['file_list']:
            log(i)

        nodes = [i+1 for i in range(len(data['file_list']))]
        labels = [i+1 for i in range(len(data['file_list']))]

        edges = []
        log('edges:')
        for i in range(len(data['process_day'])):
            if data['cos'][i] >= 0.25:
                edges.append(tuple(data['process_day'][i]))
                log('%s, %s, %s' % (tuple(data['process_day'][i]),data['real_data'][i],data['cos'][i]))
        G = nx.Graph()

        G.add_nodes_from(nodes,labels=labels)
        G.add_edges_from(edges)
        # G.add_edge(1,2)
        pos = nx.spring_layout(G)
        nx.draw(G,pos,with_labels=True)

        # log('max_clique: %s' % approximation.max_clique(G))
        #
        # log('k_components: %s' % approximation.k_components(G,min_density=0.98))
        # plt.savefig("C:\\Users\\Yuhsuan\\Desktop\\MEMDS\\pics\\day_%s.png" % days, dpi=75)
        plt.show()
        plt.cla()
        # print(approximation.k_components(G,min_density=0.98))

def byweight(dict):
    for days in [1]:
    # for days in range(len(dict['daily_data'])):
        data = dict['daily_data'][days]
        print(data)
        print('days: %s' % days)
        print('file_list:')
        for i in data['file_list']:
            print(i)

        nodes = [i+1 for i in range(len(data['file_list']))]
        labels = [i+1 for i in range(len(data['file_list']))]

        G = nx.Graph()
        G.add_nodes_from(nodes, labels=labels)

        pos = nx.spring_layout(G)
        print('edges:')
        for i in range(len(data['process_day'])):
            weight = data['cos'][i]
            print(data['process_day'][i])
            edges = data['process_day'][i]
            if weight>0.25:
                G.add_edge(edges[0],edges[1],weight=data['real_data'][i])

        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] ==True]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == False]

        nx.draw_networkx_edges(G, pos=pos, edgelist=elarge,
                               width=1)
        nx.draw_networkx(G, pos=pos, edgelist=esmall,
                               width=1, alpha=0.5, edge_color='b', style='dashed')
        nx.draw_networkx(G, pos=pos, node_size=100)
        nx.draw_networkx(G,pos=pos)
        plt.axis('off')
        plt.draw_if_interactive()
        plt.show()
        plt.cla()

def test():
    G = nx.Graph()

    G.add_edge('a', 'b', weight=0.6)
    G.add_edge('a', 'c', weight=0.2)
    G.add_edge('c', 'd', weight=0.1)
    G.add_edge('c', 'e', weight=0.7)
    G.add_edge('c', 'f', weight=0.9)
    G.add_edge('a', 'd', weight=0.3)

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge,
                           width=6)
    nx.draw_networkx_edges(G, pos, edgelist=esmall,
                           width=6, alpha=0.5, edge_color='b', style='dashed')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    plt.axis('off')
    plt.show()

if __name__=='__main__':
    byweight(data())
    threshold(data())
    # test()