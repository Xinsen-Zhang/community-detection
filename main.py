from OverlappingCommunity.utils import Graph as g
graph = g("./data/Edge_new.csv")
graph.init_graph()
print(graph.vertex_num)
print(graph.edge_num)
vertices = graph.get_vertices()
for vertex_index, vertex in vertices.items():
    print("vertex index: {}, initial communities: {}".format(vertex_index, vertex.get_community_num()))

