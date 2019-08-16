from OverlappingCommunity.utils import Graph as g
graph = g("./data/Edge_new.csv")
graph.init_graph()
print(graph.vertex_num)
print(graph.edge_num)
print(graph.get_neighbor_by_id("1"))
