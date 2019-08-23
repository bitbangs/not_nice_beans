import logging

#review use of for in dicts
logger = logging.getLogger(__name__)
class Graph():
    """undirected graph"""

    def __init__(self, root):
        self.adj_list = {root:set()}
        self.payloads = {root:None}

    def __repr__(self):
        return 'undirected graph w/ following adjacent list\n\t(%s)\nand payloads\n\t%s' % (self.adj_list, self.payloads)

    def AddVertex(self, new_node, connect_to = None):
        """connect_to can be a nothing, single vertex, or list, must already exist"""
        vertex, payload = new_node
        if vertex not in self.adj_list:
            self.adj_list[vertex] = set()
        if isinstance(connect_to, list):
            for existing_vert in connect_to:
                self.adj_list[existing_vert].add(vertex)
                self.adj_list[vertex].add(existing_vert)
        elif connect_to is not None:
            self.adj_list[vertex].add(connect_to)
            self.adj_list[connect_to].add(vertex)
        if vertex not in self.payloads:
            self.payloads[vertex] = payload
        logger.info('adds vertex %s', vertex)

    def RemoveVertex(self, victim_vert):
        del self.adj_list[victim_vert]
        for vert, adj in self.adj_list.items():
            adj.discard(victim_vert)
        del self.payloads[victim_vert]
        logger.info('removes vertex %s', victim_vert)

    def BFS(self, start_vert, payload_match):
        level = {start_vert: 0}
        parent = {start_vert: None}
        ii = 1
        frontier = self.adj_list[start_vert]
        while frontier:
            next = set()
            for uu in frontier:
                if self.payloads.get(uu) == payload_match:
                    for vv in self.adj_list[uu]:
                        if vv not in level and self.payloads.get(vv) == payload_match:
                            level[vv] = ii
                            parent[vv] = uu
                            next.add(vv)
            frontier = next
            ii += 1
        return parent

    def DFSVisit(self, start_vert, breadcrumbs):
        for vv in self.adj_list[start_vert]:
            if vv not in breadcrumbs:
                breadcrumbs[vv] = start_vert
                self.DFSVisit(vv, breadcrumbs)

    def DFS(self, start_vert):
        breadcrumbs = {start_vert: None}
        self.DFSVisit(start_vert, breadcrumbs)
        return breadcrumbs