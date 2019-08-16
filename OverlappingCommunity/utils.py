import codecs
from tqdm import tqdm

class Graph(object):
    def __init__(self, filepath, is_primary_key = False, init_type= "edge"):

        '''
        :param filepath: csv 文件的路径
        :param is_primary_key: 是否需要 primaryKey
        :param init_type: edge 表示按照边进行初始化, vertex 表示按照点进行初始化
        '''

        self.filepath = filepath
        self.vertices = {}
        self.is_primaryKey = is_primary_key
        self.primary_key_map = {}
        self.vertex_num = 0
        self.edge_num = 0
        self.neighbor_map = {}
        self.init_type = init_type

    def init_graph(self):
        f = self.open_csv()
        lines = get_lines(f)
        close_csv(f)
        with tqdm(enumerate(lines), total=len(lines)) as t:
            for edge_index,line in t:
                from_index, to_index, primary_key = parse_line(line)
                if self.is_primaryKey:
                    self.primary_key_map[to_index] = primary_key
                vertices_ = [from_index, to_index]
                for i, vertex_index in enumerate(vertices_):
                    vertex = self.vertices.get(vertex_index, Vertex(vertex_index))
                    if self.init_type == "edge":
                        vertex.add_community(edge_index)
                    else:
                        communities = vertex.get_communities()
                        if len(communities)== 0:
                            vertex.add_community(vertex.get_id())
                    self.vertices[vertex_index] = vertex
                    neighbors = self.neighbor_map.get(vertex_index, [])
                    neighbors.append(vertices_[1-i])
                    self.neighbor_map[vertex_index] = neighbors

        self.vertex_num = len(self.vertices)
        for k,v in self.neighbor_map.items():
            self.edge_num += len(v)

    def open_csv(self):
        f = codecs.open(self.filepath)
        return f

    def set_vertices(self, vertices):
        self.vertices = vertices

    def add_vertex(self, vertex):
        self.vertices[vertex.get_id()] = vertex

    def get_vertices(self):
        return self.vertices

    def get_neighbor_by_id(self, vertex_id):
        return self.neighbor_map.get(vertex_id, [])

def parse_line(line):
    from_index, to_index, primary_key = line.strip().split(",")
    return from_index, to_index, primary_key


def get_lines(f):
    return f.readlines()


def close_csv(f):
    f.close()


class Vertex(object):
    def __init__(self, vertex_id):
        self.vertex_id = vertex_id
        self.communities = []

    def set_communities(self, communities):
        self.communities = communities

    def add_community(self, community):
        self.communities.append(community)

    def get_id(self):
        return self.vertex_id

    def get_communities(self):
        return self.communities

    def get_community_num(self):
        return len(self.communities)
