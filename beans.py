import logging
import random
from graph import Graph

logger = logging.getLogger(__name__)

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

bean_colors = [(120, 0, 0), (0, 120, 0), (0, 0, 120), (120, 0, 120)]
class Bean():
    """one color"""
    def __init__(self, coordinate):
        self.color = bean_colors[random.randint(0, len(bean_colors) - 1)]
        self.coordinate = coordinate
        self.has_settled = False

    def __repr__(self):
        return 'Bean(coordinate:%s, color:%s, settled:%s)' % (self.coordinate, self.color, self.has_settled)

orientations = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
class MovingBean():
    """two beans and their orientation"""
    def __init__(self):
        self.beans = Bean([2, 0]), Bean([2, 1]) #improve to named tuple
        self.orientation = 0
        self.has_settled = False
        logger.info('created moving bean pair %s', self.beans)

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
    def __init__(self, grid_width, grid_height):
        self.match_graph = Graph(None)
        self.color_map = {}
        self.column_heights = [0] * grid_width
        self.max_height = grid_height

    def __repr__(self):
        return 'SettledBeans(graph:%s)' % repr(self.match_graph)

    #bean settling
    def SettleDetect(self, moving_bean):
        settle_coordinates = []
        for xx in range(0, len(self.column_heights)):
            settle_coordinates.append([xx, self.max_height - self.column_heights[xx] - 1])

        pivot_bean, spin_bean = moving_bean.beans
        if settle_coordinates.count(pivot_bean.coordinate):
            pivot_bean.has_settled = True
        if settle_coordinates.count(spin_bean.coordinate):
            spin_bean.has_settled = True

        if pivot_bean.has_settled or spin_bean.has_settled:
            pivot_bean.has_settled = True #do we want this? think of drops as possibly just being gravity driven...
            spin_bean.has_settled = True #do we want this? comment above^
            moving_bean.has_settled = True
            logger.info('settle detect returns true: %s', moving_bean.beans)
            return True

        return False

    def Settle(self, moving_bean):
        def SettleBean(bean):
            settle_coordinate = (bean.coordinate[0], bean.coordinate[1])
            settle_coordinate_w = (bean.coordinate[0] - 1, bean.coordinate[1])
            settle_coordinate_s = (bean.coordinate[0], bean.coordinate[1] + 1)
            settle_coordinate_e = (bean.coordinate[0] + 1, bean.coordinate[1])
            neighbors = []

            if settle_coordinate_w in self.color_map:
                neighbors.append(settle_coordinate_w)
            if settle_coordinate_s in self.color_map:
                neighbors.append(settle_coordinate_s)
            if settle_coordinate_e in self.color_map:
                neighbors.append(settle_coordinate_e)
            self.match_graph.AddVertex((settle_coordinate, bean.color), neighbors)
            logger.info('adds to settled color map->%s:%s', settle_coordinate, bean.color)
            self.color_map[settle_coordinate] = bean.color

        pivot_bean, spin_bean = moving_bean.beans
        pivot_vertex = (pivot_bean.coordinate[0], pivot_bean.coordinate[1])
        spin_vertex = (spin_bean.coordinate[0], spin_bean.coordinate[1])
        self.match_graph.AddVertex((pivot_vertex, pivot_bean.color))
        self.match_graph.AddVertex((spin_vertex, spin_bean.color), pivot_vertex)

        SettleBean(pivot_bean)
        SettleBean(spin_bean)

        self.column_heights[pivot_bean.coordinate[0]] = self.column_heights[pivot_bean.coordinate[0]] + 1
        self.column_heights[spin_bean.coordinate[0]] = self.column_heights[spin_bean.coordinate[0]] + 1

    #bean matching
    def MatchDetect(self, moving_bean):
        def DetectMatches(bean):
            if bean.has_settled:
                connections = self.match_graph.BFS((bean.coordinate[0], bean.coordinate[1]), bean.color)
                logging.info('match detect bfs on bean %s has these color-matched connections: %s', bean, connections)
                if len(connections) > 3:
                    for coordinate in connections:
                        if coordinate in self.color_map:
                            logging.info('deletes from settled color map->%s:%s', coordinate, self.color_map[coordinate])
                            del self.color_map[coordinate]
                            self.column_heights[coordinate[0]] = self.column_heights[coordinate[0]] - 1
                            self.match_graph.RemoveVertex(coordinate)
                    return True
            return False

        pivot_bean, spin_bean = moving_bean.beans
        matched = False
        matched = DetectMatches(pivot_bean)
        if pivot_bean.color != spin_bean.color:
            matched = matched or DetectMatches(spin_bean)

        return matched

    #beans fall when matches remove beans under them
    #def FallDetect(self):
        """resolves floating beans caused by successful match"""
        #how do I get a floor been?  there isn't always one?
        #@@@
        #for vertex, adjacencies in self.match_graph.items(): #bfs from and floor so we get the lower hangers first
            #if vertex[1] + 1 < self.max_height and (vertex[0], vertex[1] + 1) not in adjacencies: #does everyone have a southern neighbor?
                #self.match_graph.RemoveVertex(vertex) #drop bean. so what does this mean to translate vertex to bean?
                #new_coordinate = (vertex[0], self.column_heights[vertex[0]])
                #self.match_graph.AddVertex(new_coordinate, self.color_map[vertex]) #move the vertex with payload to new location
                #del self.color_map[vertex] #delete from map
                #self.color_map[new_coordinate] = self.color_map[vertex] #keep the color
                #self.column_heights[vertex[0]] = self.column_heights[vertex[0]] + 1