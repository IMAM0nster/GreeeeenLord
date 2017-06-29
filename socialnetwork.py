# -*-coding:utf-8-*-
__author__ = 'fyy'
import networkx as nx
import matplotlib.pyplot as plt
from hupudb import *
from FastUnfolding import FastUnfolding


# 测试代码，将所有的数据放入内存，在测试数据较小的情况下是可行的
def build_network_from_db():
    hoop_db = HoopDB()
    data = hoop_db.get_all_comments()
    comments = data[0]
    total = data[1]
    graph = nx.Graph()
    for comment in comments:
        target_user = comment["target_url"]
        author_user = comment["author_url"]
        if target_user == author_user:
            total -= 1
            continue
        # 将边和点加入图中
        graph.add_nodes_from([target_user, author_user], cid=-1)
        if (target_user, author_user) in graph.edges() or (author_user, target_user) in graph.edges():
            graph[target_user][author_user]['weight'] += 1.0
        else:
            graph.add_edge(target_user, author_user, weight=1.0)
    for edge in graph.edges():
        graph[edge[0]][edge[1]]["weight"] /= total
    return graph


def get_communities_result():
    graph = build_network_from_db()
    finish = False
    fast_unfolding = FastUnfolding(graph)
    while fast_unfolding.modularity_optimization():
        continue
    graph_copy = graph.copy()
    graph, finish = fast_unfolding.community_aggregation()
    fast_unfolding = FastUnfolding(graph)
    while not finish:
        while fast_unfolding.modularity_optimization():
            continue
        fast_unfolding.update_community(graph_copy, graph)
        graph, finish = fast_unfolding.community_aggregation()
        fast_unfolding = FastUnfolding(graph)
    while fast_unfolding.modularity_optimization():
        continue
    return graph_copy


# def draw_communities(communities, graph):
#     pos = nx.random_layout(graph)
#     # size = nx.number_of_nodes(graph)
#     count = 0
#     for community in communities:
#         node_list = list(community.nodes)
#         if not len(node_list):
#             continue
#         nx.draw_networkx_nodes(graph, pos, node_list, node_size=200, node_color='r')
#         count += 1
#     nx.draw_networkx_edges(graph, pos, alpha=0.5)
#     plt.show()

def nodes_and_links(graph):
    index_refer = dict()
    # nodes = graph.nodes()
    index = 0
    node_file = open("graph.txt", "w")
    node_file.write('{"nodes": [')
    for node in graph.nodes():
        index_refer[node] = index
        index += 1
        string = '{"category": ' + unicode(graph.node[node]["cid"]) + ', "name": "' + node + '"}'
        node_file.write(str(string))
        if index != nx.number_of_nodes(graph):
            node_file.write(',')
    node_file.write('],')
    node_file.write('"links": [')
    index = 0
    for link in graph.edges():
        index += 1
        string = '{"source": ' + unicode(link[0]) + ', "target": ' + \
                 unicode(link[1]) + '}'
        node_file.write(str(string))
        if index != nx.number_of_edges(graph):
            node_file.write(',')
    node_file.write(']}')

print "测试社区发现"
g = get_communities_result()
nodes_and_links(g)
print "测试完毕"




