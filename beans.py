import random

class Grid():
    def __init__(self, pix_box, grid_size):
        self.xx_offset, self.yy_offset, self.xx_max, self.yy_max = pix_box
        self.grid_width, self.grid_height = grid_size
        self.cell_width = int((self.xx_max - self.xx_offset) / self.grid_width)
        self.cell_height = int((self.yy_max - self.yy_offset) / self.grid_height)
        self.grid_lines = []
        for yy in range(0, self.grid_height):
            self.grid_lines.append(((self.xx_offset, self.yy_offset + (yy * self.cell_height)),(self.xx_max, self.yy_offset + (yy * self.cell_height))))
        for xx in range(0, self.grid_width):
            self.grid_lines.append(((self.xx_offset + (xx * self.cell_width), self.yy_offset),((self.xx_offset + (xx * self.cell_width), self.yy_max))))

    def __repr__(self):
        return 'Grid(scale:%s, offset:%s)' % (self.scale, self.offset)

    def ToGrid(self, pixel_coordinate):
        xx, yy = pixel_coordinate
        xx = int((xx - self.xx_offset)/(self.xx_max - self.xx_offset) * self.grid_width)
        yy = int((yy - self.yy_offset)/(self.yy_max - self.yy_offset) * self.grid_height)
        return (xx, yy)

    def ToPixels(self, grid_coordinate):
        xx, yy = grid_coordinate
        xx = int((xx - 0)/(self.grid_width) * (self.xx_max - self.xx_offset) + self.xx_offset + (self.cell_width / 2))
        yy = int((yy - 0)/(self.grid_height) * (self.yy_max - self.yy_offset) + self.yy_offset + (self.cell_height / 2))
        return (xx, yy)

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

bean_colors = [(120, 0, 0), (0, 120, 0), (0, 0, 120), (120, 0, 120)]
class Bean():
    """one color"""
    def __init__(self, coordinate):
        self.color = bean_colors[random.randint(0, len(bean_colors) - 1)]
        self.coordinate = coordinate

    def __repr__(self):
        return 'Bean(coordinate:%s)' % (self.coordinate)

orientations = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
class MovingBean():
    """two beans and their orientation"""
    def __init__(self):
        self.beans = Bean([2, 0]), Bean([2, 1]) #improve to named tuple
        self.orientation = 0

    def __repr__(self):
        return 'MovingBean(beans:%s, orientation:%s)' % (repr(self.beans), self.orientation)

    def Move(self, direction):
        pivot_bean, spin_bean = self.beans
        pivot_bean.coordinate = [pivot_bean.coordinate[0] + direction[0], pivot_bean.coordinate[1] + direction[1]] #need to check collisions
        spin_bean.coordinate = [spin_bean.coordinate[0] + direction[0], spin_bean.coordinate[1] + direction[1]] #need to check collisions
        #need to check if settling

    def Spin(self):
        self.orientation = (self.orientation + 1) % 4
        pivot_bean, spin_bean = self.beans
        xx, yy = orientations[self.orientation]
        pivot_bean.coordinate = [pivot_bean.coordinate[0] + xx, pivot_bean.coordinate[1] + yy]

    #def Settle(self):
        #determine if beans drop
        #put beans on graph
