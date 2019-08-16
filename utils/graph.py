import codecs
from tqdm import tqdm

class Graph(object):
    def __init__(self, filepath, is_primary_key = False, is_overlapping = False):
        '''

        :param filepath: csv 文件的路径
        :param is_primary_key: 是否需要 primaryKey
        :param is_overlapping: 是否是重叠社区的检测
        '''
        self.filepath = filepath
        self.vertices = None
        self.is_primaryKey = is_primary_key
        self.is_overlapping = is_overlapping
        self.primary_key_map = {}

    def init_graph(self):
        f = self.open_csv()
        lines = self.get_lines(f)
        with tqdm(lines, total = len(lines)) as t:
            for line in t:
                from_index, to_index, primary_key = self.parse_line(line)
                if self.is_primaryKey:
                    self.primary_key_map[to_index] = primary_key
                from_vertex = self.vertices.get(from_index, Vertex(from_index, is_overlapping= self.is_overlapping))
        self.close_csv(f)

    def open_csv(self):
        f = codecs.open(self.filepath)
        return f
    def close_csv(self, f):
        f.close()
    def get_lines(self, f):
        return f.readlines()
    def parse_line(self, line):
        from_index, to_index, primaryKey = line.strip().split(",")
        return from_index, to_index, primaryKey
    def set_vertice(self, vertices = {}):
        self.vertices = vertices
    def add_vertex(self, vertex):
        self.vertices[vertex.get_id()] = vertex

class Vertex(object):
    def __init__(self, vertex_id, communities = [], is_overlapping = False, community = ""):
        self.verted_id = vertex_id
        self.communities = communities
        self.is_overlapping = is_overlapping
        self.community = community

    def set_communities(self, communities):
        self.communities = communities

    def set_community(self, community):
        self.community = community

    def add_community(self, community):
        self.communities.append(community)

    def get_id(self):
        return self.verted_id