# -*-coding:utf-8-*-
__author__ = 'fyy'
import networkx as nx
import matplotlib.pyplot as plt
from hupudb import *
from FastUnfolding import FastUnfolding


def build_network_from_db():
    hoop_db = HoopDB()
    data = hoop_db.get_all_comments()
    comments = data[0]
    total = data[1]
    graph = nx.Graph()
    for comment in comments:
        target_user = comment["target_url"]
        author_user = comment["author_url"]
        # 自己回复自己的帖子不在分析范围之内
        if target_user == author_user:
            continue
        # 将边和点加入图中
        graph.add_nodes_from([target_user, author_user], cid=-1)
        if (target_user, author_user) in graph.edges() or (author_user, target_user) in graph.edges():
            graph[target_user][author_user]['weight'] += 1.0/total
        else:
            graph.add_edge(target_user, author_user, weight=1.0/total)
    return graph


def get_communities_result():
    graph = build_network_from_db()
    finish = False
    fast_unfolding = FastUnfolding(graph)
    while not finish:
        while fast_unfolding.modularity_optimization():
            continue
        graph, finish = fast_unfolding.community_aggregation()
        fast_unfolding = FastUnfolding(graph)
    while fast_unfolding.modularity_optimization():
        continue
    return graph, fast_unfolding.communities


def draw_communities(communities, graph):
    pos = nx.random_layout(graph)
    size = nx.number_of_nodes(graph)
    count = 0
    for community in communities:
        node_list = list(community.nodes)
        if not len(node_list):
            continue
        nx.draw_networkx_nodes(graph, pos, node_list, node_size=200, node_color='r')
        count += 1
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    plt.show()

print "测试社区发现"
comment_graph, hoop_communities = get_communities_result()
draw_communities(hoop_communities, comment_graph)
print "测试完毕"
