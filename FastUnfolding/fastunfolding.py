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
            community_1.modularity.update_modularity(community_1_new_modularity)
            community_2.modularity.update_modularity(community_2_new_modularity)
            return True
        else:
            return False

    def modularity_optimization(self):
        # 标记变量，表示是否能够继续增大模块化程度
        increasing = False
        for node in self.graph.nodes():
            for neighbor in self.graph.neighbors(node):
                node_community = self.communities[self.graph.node(node)['cid']]
                neighbor_community = self.communities[self.graph.node(neighbor)['cid']]
                node_community.remove_node(node)
                neighbor_community.add_node(node)
                # 将节点加入邻居所在社区，若比较前后模块化插值的结果为False
                # 放弃该操作
                # 若为True，则将increasing标记为True
                if not self.__increasing(node_community, neighbor_community):
                    node_community.add(node)
                    neighbor_community.remove(node)
                else:
                    increasing = True
        return increasing

    def community_aggregation(self):
        origin_communities_num = len(self.communities)
        if origin_communities_num == 2:
            return self.graph
        new_graph = networkx.Graph()
        for community in self.communities:
            if len(community.nodes) == 0:
                continue
            new_graph.add_node(community.id)
        for node in self.graph.nodes():
            node_cid = self.graph.node(node)['cid']
            for neighbor in self.graph.neighbors(node):
                neighbor_cid = self.graph.node(neighbor)['cid']
                weight = self.graph[node][neighbor]['weight']
                new_graph.add_edge(node_cid, neighbor_cid, weight=weight)
        return new_graph, networkx.number_of_nodes(new_graph) == origin_communities_num