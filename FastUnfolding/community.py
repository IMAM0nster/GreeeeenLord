# -*-coding:utf-8-*-
k__author__ = 'fyy'
import networkx


# Community类是对于社区的包装
class Community:
    def __init__(self, cid, node):
        self.cid = cid
        self.modularity = 0
        nodes = set()
        nodes.add(node)
        self.nodes = nodes

    # 这个函数会计算此时的模块化程度
    def new_modularity(self, graph):
        in_weight_tmp = 0.0
        tot_weight_tmp = 0.0
        for n in self.nodes:
            for neighbors in graph.neighbors(n):
                if graph.node[neighbors]['cid'] == self.cid:
                    in_weight_tmp += graph[n][neighbors]['weight']
                tot_weight_tmp += graph[n][neighbors]['weight']
        in_weight_tmp /= 2
        tot_weight_tmp /= 2
        modularity_tmp = in_weight_tmp/2 - (tot_weight_tmp / 2) * (tot_weight_tmp / 2)
        return modularity_tmp

    def update_modularity(self, new_modularity):
        self.modularity = new_modularity

    def remove_node(self, node_id):
        if node_id not in self.nodes:
            return
        self.nodes.remove(node_id)

    def add_node(self, node_id):
        if node_id in self.nodes:
            return
        # graph.node[node_id]['cid'] = self.cid
        self.nodes.add(node_id)