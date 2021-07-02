import pickle
import tempfile
from random import random
from copy import deepcopy
from game_utils import TileStatus
from game_utils import Direction as D


def load_map_memory():
    with open(tempfile.gettempdir()+"robnics_memory.pickle", "rb") as f:
        return pickle.load(f)


def move_cost(n):
    return (n*n + n)/2



class MapMemory(object):
    def __init__(self, width, height):
        # Initialize map full of yet unknown tiles
        self.map = dict()
        for x in range(width):
            for y in range(height):
                self.map[(x,y)] = '_'
        self.width = width # x
        self.height = height # y
        self.directions = [D.up, D.down, D.left, D.right, 
                           D.up_left, D.up_right, D.down_left, D.down_right]
    

    def __getitem__(self, coor):
        if len(coor) != 2:
            raise IndexError("Coordinates must be a 2-sized tuple.")
        return self.map[coor]
    

    def __setitem__(self, coor, obj):
        if len(coor) != 2:
            raise IndexError("Coordinates must be a 2-sized tuple.")
        self.map[coor] = obj
        

    def local_save(self):
        with open(tempfile.gettempdir()+"robnics_memory.pickle", "wb") as f:
            pickle.dump(self, f)
    

    # Used for checking functionality
    # not actually required for the game
    def __str__(self):
        rows = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += self.map[(x,y)] + " "
            rows.append(row)
        
        map_string = ""
        for r in rows[::-1]:
            map_string += r + '\n'
            
        return map_string
    

    def coor_dir_update(self, pos, _dir, n):
        xy = _dir.as_xy()
        xy = tuple([n*x for x in xy])
        return tuple([x1+x2 for x1,x2 in zip(pos,xy)])
    

    def free_tiles(self, myPos):
        return [item[0] for item in self.map.items() if item[1] == '.' and item[0] != myPos]
    
    def is_in_map(self, coor):
        x, y = coor
        if x > self.width-1 or x < 0:
            return False
        if y > self.height-1 or y < 0:
            return False
        return True

    # Update the MapMemory by adding previously unseen tiles
    def update(self, status, seen_tiles):
        # Initialize starting position in MapMemory
        self.map[status.x,status.y] = '.'
        
        coors_inSight = []
        v = status.params.visibility
        myPos = (status.x, status.y)
        # Get all tiles' coordinates that are visible
        for _d in self.directions[:4]:
            for _n in range(1, v+1):
                coor_ = self.coor_dir_update(myPos, _d, _n)
                if self.is_in_map(coor_):
                    coors_inSight.append(coor_)

        for _d_lr in self.directions[2:4]:
            for _n in range(1, v+1):
                pos = self.coor_dir_update(myPos, _d_lr, _n)
                for _d_ud in self.directions[:2]:
                    for _n_ in range(1, v+1):
                        coor_ = self.coor_dir_update(pos, _d_ud, _n_)
                        if self.is_in_map(coor_):
                            coors_inSight.append(coor_)

        # Extract coors previously not seen
        new_coors_inSight = list(set(coors_inSight) - set(seen_tiles))
        
        status_free = [TileStatus.Empty, TileStatus.Mine]
        # Update map
        for tile_coor in new_coors_inSight:
            _tileStatus = status.map[tile_coor].status
            if _tileStatus in status_free:
                self.map[tile_coor] = '.'
            if _tileStatus == TileStatus.Wall:
                self.map[tile_coor] = '#'
            if _tileStatus == TileStatus.Unknown:
                raise("The MapMemory cannot be updated with unknown tiles.")
        
        # Add seen tiles to list of seen tiles
        seen_tiles += new_coors_inSight



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
        # cost of walking into specific direction -> default=1
        self.dir_costs = dir_costs
        self.different_dir_costs = False if (dir_costs == tuple([1 for _ in range(8)])) else True
        self._map = _map
        self.directions = [D.up, D.down, D.left, D.right, 
                           D.up_left, D.up_right, D.down_left, D.down_right]
        self.coor_dirs = [d.as_xy() for d in self.directions]
        self.optimal_path = None
    

    def approx_distance(self, coor):
        dx, dy = [abs(x1-x2) for x1,x2 in zip(coor, self.goal.coor)]
        return dx + dy - min(dx, dy)
    

    def set_costs(self, _node, dir_idx):
        _node.g = _node.parent.g + self.dir_costs[dir_idx]
        _node.h = self.approx_distance(_node.coor)
        _node.f = _node.g + _node.h
        

    def is_walkable(self, coor, constraints):
        if coor in constraints:
            return False

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
    

    def possible_directions(self, coor):
        # Corners of the map
        if coor[0] == 0 and coor[1] == 0:
            return [D.up, D.up_right, D.right]
        if coor[0] == 0 and coor[1] == self._map.height-1:
            return [D.right, D.down_right, D.down]
        if coor[0] == self._map.width-1 and coor[1] == 0:
            return [D.up, D.left, D.up_left]
        if coor[0] == self._map.height-1 and coor[1] == self._map.width-1:
            return [D.down, D.down_left, D.left]
        
        help_list = []
        # Sides of the map
        if coor[0] == 0:
            help_list = [D.left, D.up_left, D.down_left]
        if coor[0] == self._map.width-1:
            help_list = [D.right, D.up_right, D.down_right]
        if coor[1] == 0:
            help_list = [D.down, D.down_left, D.down_right]
        if coor[1] == self._map.height-1:
            help_list = [D.up, D.up_left, D.up_right]
            
        return [d for d in self.directions if d not in help_list]
    

    def get_optimal_path(self):
        return self.optimal_path
            

    def optimize(self, constraints):
        open_queue = PQueue()
        closed_dict = dict()
        
        if self._map[self.start.coor] == '#' or self._map[self.goal.coor] == '#':
            raise ValueError("Initial/Final position cannot be on a wall \'#\'.")
        
        # Add start node to queue
        open_queue._put((self.start.f, self.start))
        
        while not open_queue.empty():
            # Get lowest cost node
            current_node = open_queue._get()[1]
            # Mark it as closed
            closed_dict[current_node.coor] = None

            if current_node == self.goal:
                self.optimal_path = self.get_path(current_node)
                return self.get_optimal_path()
            
            pos = current_node.coor
            for d in self.possible_directions(pos):
                neighbor_coor = tuple([x+y for x,y in zip(pos, d.as_xy())])
                
                if not self.is_walkable(neighbor_coor, constraints) or neighbor_coor in closed_dict:
                    continue
                
                neighbor_node = Node(current_node, neighbor_coor)
                # If node not in open list add it to the open list
                if not neighbor_coor in open_queue:
                    dir_idx = self.coor_dirs.index(neighbor_node - current_node)
                    self.set_costs(neighbor_node, dir_idx)
                    open_queue._put((neighbor_node.f, neighbor_node))
                else:
                    # If node in open list, check whether its path is cheaper
                    same_node, idx_node = open_queue.get_node(neighbor_node)
                    if same_node.g < neighbor_node.g:
                        open_queue.queue[idx_node].parent = current_node
                        dir_idx = self.coor_dirs.index(same_node - current_node)
                        open_queue.queue[idx_node].g = current_node.g + self.dir_costs[dir_idx]
                        open_queue.queue[idx_node].f = open_queue.queue[idx_node].g + same_node.h
        
        return [] # return empty list if no feasible path to goal exists