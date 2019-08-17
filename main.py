from overlapping_community.utils import Graph as g
from overlapping_community.algo import SLPA

graph = g("./data/Edge_new.csv", init_type="vertex")
graph.init_graph()
slpa = SLPA(graph)
slpa.compute()