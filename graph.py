#review use of for in dicts
class Graph():
    """undirected graph"""

    def __init__(self, root):
        self.adj_list = {root:set()}

    def __repr__(self):
        return 'undirected graph w/ following adjacent list\n\t(%s)' % self.adj_list

    def AddVertex(self, new_vert, connect_to = None):
        self.adj_list[new_vert] = set()
        if isinstance(connect_to, list):
            for vert in connect_to:
                self.adj_list[vert].add(new_vert)
                self.adj_list[new_vert].add(vert)
        elif connect_to is not None:
            self.adj_list[new_vert].add(connect_to)
            self.adj_list[connect_to].add(new_vert)

    def RemoveVertex(self, victim_vert):
        del self.adj_list[victim_vert]
        for vert, adj in self.adj_list.items():
            adj.discard(victim_vert)

    def BFS(self, start_vert):
        level = {start_vert: 0}
        parent = {start_vert: None}
        ii = 1
        frontier = [start_vert]
        while frontier:
            next = []
            for uu in frontier:
                for vv in self.adj_list[uu]:
                    if vv not in level:
                        level[vv] = ii
                        parent[vv] = uu
                        next.append(vv)
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