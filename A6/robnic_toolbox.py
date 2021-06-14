from game_utils import Directions as D
from queue import PriorityQueue



class PQueue(PriorityQueue):
    """Add functionality to PriorityQueue"""
    def __contains__(self, coor):
        if not self.queue.empty():
            for node in [n for p,n in self.queue]:
                if node.coor == coor:
                    return True
        return False
    
    def get_node(self, other_node):
        for node in [n for p,n in self.queue]:
            if node == other_node:
                return node
        return None



class Node(object):
    """Represent one tile of the map for A* search"""
    def __init__(self, parent=None, coor=None):
        self.parent = parent
        self.coor = coor # coordinates (x,y)
        self.f = 0 # total cost
        self.g = 0 # cost: start -> current node
        self.h = 0 # heuristic cost: current -> end node
    
    def __eq__(self, other_node):
        return self.coor == other_node.coor
    
    def __sub__(self, next_node):
        dx = self.coor[0] - next_node.coor[0]
        dy = self.coor[1] - next_node.coor[1]
        return (dx, dy)



class Astar(object):
    """Shortest path algorithm"""
    def __init__(self, _map, start, goal):
        self.start = Node(coor=start)
        self.goal = Node(coor=end)
        self.open_queue = PQueue()
        self.closed_nodes = dict()
        self._map = _map
        self.directions = [D.up, D.down, D.left, D.right, 
                           D.up_left, D.up_right, D.down_left, D.down_right]
        self.coor_dirs = [d.as_xy() for d in self.directions]
    
    def approx_distance(self, coor):
        dx, dy = [abs(x1-x2) for x1,x2 in zip(coor, self.goal.coor)]
        return dx + dy - min(dx, dy)
    
    def set_costs(self, _node):
        _node.g = _node.parent.g + 1
        _node.h = self.approx_distance(_node.coor)
        _node.f = _node.g + _node.h
        
    def is_walkable(self, coor):
        object_ = self._map[coor[0], coor[1]]
        if object_ == '.':
            return True
        return False
    
    def get_path(self, prev_node):
        shortest_path = []
        
        while True:
            next_node = prev_node.parent
            dir_idx = self.coor_dirs.index(prev_node-next_node)
            shortest_path.append(self.directions[dir_idx])
            prev_node = next_node
            if next_node == self.start:
                break
        
        return shortest_path
            
    def optimize(self):
        # Add start node to queue
        self.open_queue._put((self.start.f, self.start))
        
        while True:
            if self.open_queue.empty():
                return None
            
            # Get lowest cost node
            current_node = self.open_queue._get()
            # Mark it as closed
            self.closed_nodes[current_node.coor] = None

            if current_node == self.goal:
                return self.get_path(current_node)
            
            pos = current_node.position
            for d in self.directions:
                neighbor_coor = tuple([x+y for x,y in zip(pos, d.as_xy())])
                
                if not self.is_walkable(neighbor_coor) or neighbor_coor in self.closed_nodes:
                    continue
                
                if not neighbor_coor in self.open_queue:
                    neighbor_node = Node(current_node, neighbor_coor)
                    self.set_costs(neighbor_node)
                    self.open_queue._put((neighbor_node.f, neighbor_node))
                else:
                    #otherpath_node = self.open_queue.get_node(neighbor_node)
                    pass

