# -*-coding:utf-8-*-
__author__ = 'fyy'
from community import Community
import networkx


# FastUnfolding 类实现了fastunfolding算法
class FastUnfolding:
    def __init__(self, graph):
        self.graph = graph
        self.modularity = 0
        communities = list()
        for n in graph.nodes():
            graph.node[n]['cid'] = len(communities)
            community = Community(len(communities), n)
            communities.append(community)
        self.communities = communities

    # 比较两个社区的模块化变化程度之和是否大于0
    # 是则更新两个社区的模块化程度
    # 否则返回False
    def __increasing(self, community_1, community_2):
        community_1_new_modularity = community_1.new_modularity(self.graph)
        community_2_new_modularity = community_2.new_modularity(self.graph)
        community_1_differ = community_1_new_modularity - community_1.modularity
        community_2_differ = community_2_new_modularity - community_2.modularity
        delta_modularity = community_1_differ + community_2_differ
        if delta_modularity > 0:
            self.modularity += delta_modularity
            community_1.update_modularity(community_1_new_modularity)
            community_2.update_modularity(community_2_new_modularity)
            return True
        else:
            return False

    @staticmethod
    def update_community(graph_copy, new_graph):
        for node in graph_copy.nodes():
            graph_copy.node[node]["cid"] = new_graph.node[graph_copy.node[node]["cid"]]["cid"]

    def modularity_optimization(self):
        # 标记变量，表示是否能够继续增大模块化程度
        increasing = False
        for node in self.graph.nodes():
            for neighbor in self.graph.neighbors(node):
                # node_community = self.communities[self.graph.node[node]['cid']]
                # neighbor_community = self.communities[self.graph.node[neighbor]['cid']]
                if self.graph.node[node]['cid'] == self.graph.node[neighbor]['cid']:
                    continue
                self.communities[self.graph.node[node]['cid']].remove_node(node)
                self.communities[self.graph.node[neighbor]['cid']].add_node(node)
                # 将节点加入邻居所在社区，若比较前后模块化插值的结果为False
                # 放弃该操作
                # 若为True，则将increasing标记为True
                if not self.__increasing(self.communities[self.graph.node[node]['cid']],
                                         self.communities[self.graph.node[neighbor]['cid']]):
                    self.communities[self.graph.node[node]['cid']].add_node(node)
                    self.communities[self.graph.node[neighbor]['cid']].remove_node(node)
                else:
                    self.graph.node[node]['cid'] = self.graph.node[neighbor]['cid']
                    increasing = True
        return increasing

    def community_aggregation(self):
        # origin_communities_num = len(self.communities)
        # if origin_communities_num == 2:
        #     return self.graph
        new_graph = networkx.Graph()
        total_weight = 0.0

        for community in self.communities:
            if len(community.nodes) == 0:
                continue
            new_graph.add_node(community.cid, cid=-1)

        for node in self.graph.nodes():
            node_cid = self.graph.node[node]['cid']
            for neighbor in self.graph.neighbors(node):
                neighbor_cid = self.graph.node[neighbor]['cid']
                if neighbor_cid == node_cid:
                    continue
                weight = self.graph[node][neighbor]['weight']
                total_weight += weight
                if (node_cid, neighbor_cid) in new_graph.edges() or (neighbor_cid, node_cid) in new_graph.edges():
                    new_graph[node_cid][neighbor_cid]["weight"] += weight
                else:
                    new_graph.add_edge(node_cid, neighbor_cid, weight=weight)

        # for node, neighbors in new_graph.adjacency_iter():
        #     for neighbor, attr in neighbors.items():
        #         attr['weight'] /= total_weight
        for edge in new_graph.edges():
            new_graph[edge[0]][edge[1]]["weight"] /= total_weight
        community_number = networkx.number_of_nodes(new_graph)
        # for community_a in new_graph.nodes():
        #     for community_b in new_graph.nodes():
        #         if community_a == community_b:
        #             continue
        #         tmp_node_set = set()
        #         tmp_node_set |= self.communities[community_a].nodes
        #         tmp_node_set |= self.communities[community_b].nodes
        #         weight = 0.0
        #         for node_a in tmp_node_set:
        #             for node_b in tmp_node_set:
        #                 if (node_a, node_b) in self.graph.edges() or (node_b, node_a) in self.graph.edges():
        #                     weight += self.graph[node_a][node_b]["weight"]
        #         new_graph.add_edge(community_a, community_b, weight=weight)
        # community_number = new_graph.number_of_nodes()
        print community_number
        return new_graph, community_number < 20 or community_number == len(self.communities)