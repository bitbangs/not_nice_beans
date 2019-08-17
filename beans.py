from graph import Graph
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
        self.settle_coordinates = []
        for xx in range(0, self.grid_width):
            self.settle_coordinates.append([xx, self.grid_height - 1])

    def __repr__(self):
        return 'Grid(scale:%s, offset:%s)' % (self.scale, self.offset)

    #drawing
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

    def SettleDetect(self, moving_bean):
        pivot_bean, spin_bean = moving_bean.beans
        if self.settle_coordinates.count(pivot_bean.coordinate):
            pivot_bean.has_settled = True
            self.settle_coordinates.remove(pivot_bean.coordinate)
            self.settle_coordinates.append([pivot_bean.coordinate[0], pivot_bean.coordinate[1] - 1])
        if self.settle_coordinates.count(spin_bean.coordinate):
            spin_bean.has_settled = True
            self.settle_coordinates.remove(spin_bean.coordinate)
            self.settle_coordinates.append([spin_bean.coordinate[0], spin_bean.coordinate[1] - 1])
        if pivot_bean.has_settled and spin_bean.has_settled:
            moving_bean.has_settled = True

bean_colors = [(120, 0, 0), (0, 120, 0), (0, 0, 120), (120, 0, 120)]
class Bean():
    """one color"""
    def __init__(self, coordinate):
        self.color = bean_colors[random.randint(0, len(bean_colors) - 1)]
        self.coordinate = coordinate
        self.has_settled = False

    def __repr__(self):
        return 'Bean(coordinate:%s)' % (self.coordinate)

orientations = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
class MovingBean():
    """two beans and their orientation"""
    def __init__(self):
        self.beans = Bean([2, 0]), Bean([2, 1]) #improve to named tuple
        self.orientation = 0
        self.has_settled = False

    def __repr__(self):
        return 'MovingBean(beans:%s, orientation:%s)' % (repr(self.beans), self.orientation)

    def Move(self, direction):
        pivot_bean, spin_bean = self.beans
        if not pivot_bean.has_settled:
            pivot_bean.coordinate = [pivot_bean.coordinate[0] + direction[0], pivot_bean.coordinate[1] + direction[1]] #need to check collisions
        if not spin_bean.has_settled:
            spin_bean.coordinate = [spin_bean.coordinate[0] + direction[0], spin_bean.coordinate[1] + direction[1]] #need to check collisions

    def Spin(self):
        self.orientation = (self.orientation + 1) % 4
        pivot_bean, spin_bean = self.beans
        xx, yy = orientations[self.orientation]
        pivot_bean.coordinate = [pivot_bean.coordinate[0] + xx, pivot_bean.coordinate[1] + yy]

class SettledBeans():
    """any number of stationary beans"""
    def __init__(self):
        self.match_graph = Graph(None)
        self.color_map = {}

    def __repr__(self):
        return 'SettledBeans(graph:%s)' % repr(self.match_graph)

    def Settle(self, moving_bean):
        pivot_bean, spin_bean = moving_bean.beans
        pivot_settle_coordinate = (pivot_bean.coordinate[0], pivot_bean.coordinate[1])
        pivot_settle_coordinate_w = (pivot_bean.coordinate[0] - 1, pivot_bean.coordinate[1])
        pivot_settle_coordinate_s = (pivot_bean.coordinate[0], pivot_bean.coordinate[1] + 1)
        pivot_settle_coordinate_e = (pivot_bean.coordinate[0] + 1, pivot_bean.coordinate[1])
        neighbors = []
        #use color_map to determine neighbors
        if pivot_settle_coordinate_w in self.color_map:
            if self.color_map[pivot_settle_coordinate_w] == pivot_bean.color:
                neighbors.append(pivot_settle_coordinate_w)
        if pivot_settle_coordinate_s in self.color_map:
            if self.color_map[pivot_settle_coordinate_s] == pivot_bean.color:
                neighbors.append(pivot_settle_coordinate_s)
        if pivot_settle_coordinate_e in self.color_map:
            if self.color_map[pivot_settle_coordinate_e] == pivot_bean.color:
                neighbors.append(pivot_settle_coordinate_e)
        self.match_graph.AddVertex(pivot_settle_coordinate, neighbors)
        self.color_map[(pivot_bean.coordinate[0], pivot_bean.coordinate[1])] = pivot_bean.color

        spin_settle_coordinate = (spin_bean.coordinate[0], spin_bean.coordinate[1])
        spin_settle_coordinate_w = (spin_bean.coordinate[0] - 1, spin_bean.coordinate[1])
        spin_settle_coordinate_s = (spin_bean.coordinate[0], spin_bean.coordinate[1] + 1)
        spin_settle_coordinate_e = (spin_bean.coordinate[0] + 1, spin_bean.coordinate[1])
        neighbors = []
        #use color_map to determine neighbors
        if spin_settle_coordinate_w in self.color_map:
            if self.color_map[spin_settle_coordinate_w] == spin_bean.color:
                neighbors.append(spin_settle_coordinate_w)
        if spin_settle_coordinate_s in self.color_map:
            if self.color_map[spin_settle_coordinate_s] == spin_bean.color:
                neighbors.append(spin_settle_coordinate_s)
        if spin_settle_coordinate_e in self.color_map:
            if self.color_map[spin_settle_coordinate_e] == spin_bean.color:
                neighbors.append(spin_settle_coordinate_e)
        self.match_graph.AddVertex(spin_settle_coordinate, neighbors)
        self.color_map[(spin_bean.coordinate[0], spin_bean.coordinate[1])] = spin_bean.color

    def MatchDetect(self, moving_bean):
        pivot_bean, spin_bean = moving_bean.beans
        #self.match_graph.AddVertex(pivot_bean, spin_bean)