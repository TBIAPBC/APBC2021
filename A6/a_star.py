import pickle
import numpy as np
from game_utils import Direction as D

def load_map_memory():
    with open("robnics_memory.pickle", "rb") as memory_file:
        return pickle.load(memory_file)



class MapMemory(object):
    def __init__(self, numRows, numCols):
        # initialize map full of yet unknown tiles
        self.map = [['_']*numCols for _ in range(numRows)]
    
    def __getitem__(self, coor):
        if len(coor) != 2:
            raise IndexError("Too few / many indices for array: array is 2D")
        return self.map[coor[0]][coor[1]]
    
    def __setitem__(self, coor, obj):
        if len(coor) != 2:
            raise IndexError("Too few / many indices for array: array is 2D")
        self.map[coor[0]][coor[ 1]] = obj
        
    def local_save(self):
        with open("robnics_memory.pickle", "wb") as memory_file:
            pickle.dump(self, memory_file)



class PQueue(object):
    """PriorityQueue"""
    def __init__(self):
        self.queue = []
        
    def empty(self):
        if self.queue == []:
            return True
        return False
    
    def _get(self):
        if self.empty():
            return []
        self.queue.sort(key=lambda x:x[0], reverse=True)
        return self.queue.pop()
    
    def _put(self, cost_node_tuple):
        self.queue.append(cost_node_tuple)
        
    def __contains__(self, coor):
        if not self.empty():
            for node in [n for p,n in self.queue]:
                if node.coor == coor:
                    return True
        return False
    
    def get_node(self, other_node):
        for idx, node in enumerate([n for p,n in self.queue]):
            if node == other_node:
                return node, idx
        return None, None



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
    def __init__(self, _map, start, goal, dir_costs=tuple([1 for _ in range(8)])):
        self.start = Node(coor=start)
        self.goal = Node(coor=goal)
        self.open_queue = PQueue()
        self.closed_dict = dict()
        # cost of walking into specific direction -> default=1
        self.dir_costs = dir_costs
        self.different_dir_costs = False if (dir_costs == tuple([1 for _ in range(8)])) else True
        self._map = _map
        self.directions = [D.up, D.down, D.left, D.right, 
                           D.up_left, D.up_right, D.down_left, D.down_right]
        self.coor_dirs = [d.as_xy() for d in self.directions]
    
    def approx_distance(self, coor):
        dx, dy = [abs(x1-x2) for x1,x2 in zip(coor, self.goal.coor)]
        return dx + dy - min(dx, dy)
    
    def set_costs(self, _node, dir_idx):
        _node.g = _node.parent.g + self.dir_costs[dir_idx]
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
        
        return shortest_path[::-1]
            
    def optimize(self):
        # Add start node to queue
        self.open_queue._put((self.start.f, self.start))
        
        while not self.open_queue.empty():
            # Get lowest cost node
            current_node = self.open_queue._get()[1]
            # Mark it as closed
            self.closed_dict[current_node.coor] = None

            if current_node == self.goal:
                return self.get_path(current_node)
            
            pos = current_node.coor
            for d in self.directions:
                neighbor_coor = tuple([x+y for x,y in zip(pos, d.as_xy())])
                
                if not self.is_walkable(neighbor_coor) or neighbor_coor in self.closed_dict:
                    continue
                
                neighbor_node = Node(current_node, neighbor_coor)
                # If node not in open list add it to the open list
                if not neighbor_coor in self.open_queue:
                    dir_idx = self.coor_dirs.index(neighbor_node - current_node)
                    self.set_costs(neighbor_node, dir_idx)
                    self.open_queue._put((neighbor_node.f, neighbor_node))
                else:
                    # If node in open list, check whether its path is cheaper
                    if self.different_dir_costs:
                        same_node, idx_node = self.open_queue.get_node(neighbor_node)
                        if same_node.g < neighbor_node.g:
                            self.open_queue.queue[idx_node].parent = current_node
                            dir_idx = self.coor_dirs.index(same_node - current_node)
                            self.open_queue.queue[idx_node].g = current_node.g + self.dir_costs[dir_idx]
                            self.open_queue.queue[idx_node].f = self.open_queue.queue[idx_node].g + same_node.h
        
        return [] # return empty list if no feasible path to goal exists

## Run simple example to test code

# Intialize instance of map memory
mem_ = MapMemory(10,10)


# Initialize random map
for r in range(10):
    for c in range(10):
        char = np.random.choice(['#','.'], p=[0.3,0.7])
        mem_[r,c] = char


# Intialize instance of pathfinder
pathfinder = Astar(mem_, start=(0,1), goal=(4,5))

# Show directions
print(pathfinder.directions)

# Show coordinate changes for each direction
print(pathfinder.coor_dirs)

# Show randomly generate map
print(mem_.map)

# Return optimal path from start to goal, if it exists
# otherwise return empty list
pathfinder.optimize()