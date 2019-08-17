# import sys
# import os
from tqdm import tqdm
from time import sleep
from .utils import Graph
class Algorithm(object):
    def __init__(self, graph):
        if isinstance(graph, Graph):
            self.graph = graph
        else:
            raise Exception("the type of Graph to Algo is not defined")
        if self.graph.check_initial_status():
            pass
        else:
            print("launch the initialization process")
            self.graph.init_graph()
        self.algo_name = "algo base object"


class SLPA(Algorithm):
    def __init__(self, graph, n_iteration = 10):
        super().__init__(graph)
        self.algo_name = "SLPA"
        self.n_iteration = n_iteration

    def compute(self):
        vertex_list = self.graph.get_vertex_list()
        with tqdm([i+1 for i in range(self.n_iteration)], total= self.n_iteration) as t:
            for iter in t:
                self.compute_phase(vertex_list, iter, t)

    def compute_phase(self, vertex_list,current_iter, t):
        for i,vertex_index in enumerate(vertex_list):
            listening_vertex = self.graph.get_vertex_by_id(vertex_index)
            neighbors = self.graph.get_neighbor_by_id(vertex_index)
            t.set_description_str(
                "current iter: [{}/{}], vertex id: {}, # neighbors: {}".format(current_iter, self.n_iteration, vertex_index, len(neighbors)))
            t.set_postfix_str(" percentage: {:.2f} %".format((i+1) / self.graph.vertex_num * 100))
            candidate_list = []
            for neighbor_index in neighbors:
                speaking_vertex = self.graph.get_vertex_by_id(neighbor_index)
                speaking_result = speaking_vertex.speaking_rule()
                for community_index in speaking_result:
                    candidate_list.append(community_index)
            listening_vertex.listeninng_rule(candidate_list)
            # sleep(0.05)
        pass






