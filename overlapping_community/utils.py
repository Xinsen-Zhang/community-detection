import codecs
from tqdm import tqdm
from random import randint

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
        self.vertex_list = []
        self.is_initialized = False

    def init_graph(self):
        try:
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
                        self.is_initialized = True
            print("graph object initialization success")
            # TODO logging
            pass
        except Exception as e:
            self.is_initialized = False
            print("graph object initialization failed")
            # TODO logging
            pass

        self.vertex_num = len(self.vertices)
        for vertex_index in self.vertices.keys():
            self.vertex_list.append(vertex_index)
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

    def get_vertex_list(self):
        return self.vertex_list

    def get_neighbor_by_id(self, vertex_id):
        return self.neighbor_map.get(vertex_id, [])

    def get_vertex_by_id(self, vertex_id):
        return self.vertices.get(vertex_id, Vertex(vertex_id))

    def check_initial_status(self):
        return self.is_initialized

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

    def speaking_rule(self):
        '''
        :return: 一个列表
        '''
        speaking_result = self.speaking_by_max_popularity()
        if type(speaking_result) == list:
            return speaking_result
        else:
            return [speaking_result]

    def speaking_by_max_popularity(self):
        num = len(self.communities)
        if num == 1:
            return self.communities[0]
        else:
            return self.communities[randint(0, num - 1)]

    def listeninng_rule(self, candidate_list):
        self.listening_by_max_popularity(candidate_list)

    def listening_by_max_popularity(self, candidate_list):
        count_map = {}
        for candidate in candidate_list:
            count = count_map.get(candidate, 0)
            count += 1
            count_map[candidate] = count
        result = sorted(count_map.items(), key= lambda x: x[1], reverse= True)
        max_count = result[0]
        community = max_count[0]
        self.add_community(community)
