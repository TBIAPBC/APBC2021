import random

from copy import deepcopy
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from player_base import Player
from robnic_toolbox import (load_map_memory, move_cost, 
                            MapMemory, Astar)



class ROBNIC(Player):
    def __init__(self):
        self.player_name = "Nicolas"
        self.seen_tiles = []
        self.moves_to_make = []
        self.directions = [D.up, D.down, D.left, D.right, 
                           D.up_left, D.up_right, D.down_left, D.down_right]
    

    def reset(self, player_id, max_players, width, height):
        self.player_id = player_id
        self.map_width = width
        self.map_height = height
        self.max_players = max_players
        self.myMemory = MapMemory(self.map_width, self.map_height)
        self.myMemory.local_save()
        

    def coor_dir_update(self, pos, _dir):
        xy = _dir.as_xy()
        return tuple([x1+x2 for x1,x2 in zip(pos,xy)])
        

    def update_coors(self, pos, _dir):
        for _d in _dir:
            pos = tuple([x1+x2 for x1,x2 in zip(pos, _d.as_xy())])
            yield pos
        

    def approx_distance(self, pos, goal):
        dx, dy = [abs(x1-x2) for x1,x2 in zip(pos, goal)]
        return dx + dy - min(dx, dy)


    def round_begin(self, r):
        if random.random() <= 0.2:
            print("I can already feel the gold … I want more …")

    def decide_on_moves(self, status):
        moves_this_turn = []
        myGold = deepcopy(status.gold)

        make_all_moves = False
        for pos in self.update_coors((status.x,status.y), self.moves_to_make):
            if pos == self.gold_pos:
                make_all_moves = True

        if not make_all_moves or len(self.moves_to_make) > int(self.map_width*0.5)-1:
            for m in range(4):
                prob = 1
                if self.moves_to_make != [] and random.random() <= prob and int(myGold/move_cost(m+1)) > 4:
                    moves_this_turn.append(self.moves_to_make.pop())
                    prob *= 0.9

        if myGold <= 80:
            if self.moves_to_make != []:
                moves_this_turn.append(self.moves_to_make.pop())
            if self.moves_to_make != [] and random.random() <= 0.3:
                moves_this_turn.append(self.moves_to_make.pop())

        if make_all_moves:
            for m in range(6):
                if move_cost(m+1) > min(0, myGold - 60):
                    break
                moves_this_turn.append(self.moves_to_make.pop())

        surrounding_tiles = []
        if status.health <= 85:
            for uc in self.update_coors((status.x, status.y), self.directions):
                surrounding_tiles.append(uc)

            surrounding_tiles = [st for st in surrounding_tiles if self.myMemory[st] == '.']

        if surrounding_tiles != []:
            moves_this_turn = [random.choice(surrounding_tiles)]

        return moves_this_turn


    def move(self, status):
         
        if status.health >= 30:
            moves_this_turn = self.decide_on_moves(status)
        if status.health < 30:
            moves_this_turn = []
        
        return moves_this_turn
    

    def compute_path(self, status, other_player_pos):

        myPos = (status.x,status.y)
        min_approxDist2gold = min([self.approx_distance(myPos,gp) for gp in status.goldPots.keys()])
        self.gold_pos = [item[0] for item in status.goldPots.items() 
                         if self.approx_distance(myPos,item[0]) == min_approxDist2gold][0]
        tile_approxDist = [(tile, self.approx_distance(tile, self.gold_pos)) 
                           for tile in self.myMemory.free_tiles(myPos)]
        tile_approxDist.sort(key=lambda x:x[1])

        for tile in tile_approxDist:
            # Initialize pathfinder
            pathfinder = Astar(self.myMemory, myPos, tile[0])
            self.moves_to_make = pathfinder.optimize(other_player_pos)
            
            if self.moves_to_make != []:
                break

        if tile_approxDist[0][0] == self.gold_pos:
            return True
        return False # return Boolean value, whether gold is in sight

    def path_to_set_mine(self, status, other_player_pos):
        
        paths = [] 
        for sop in status.others:
            if sop is not None:
                pathf = Astar(self.myMemory, (sop.x, sop.y), self.gold_pos)
                paths.append((pathf.start.coor, pathf.optimize(other_player_pos)))

        len_paths = [len(p[1]) for p in paths]
        pos, path = paths[len_paths.index(min(len_paths))]

        tiles = []
        for uc in self.update_coors(pos, path[::-1]):
            tiles.append(uc)

        return tiles

    def set_mines(self, status):
        
        # Load objects from pickle file
        self.myMemory = load_map_memory()

        if len(self.seen_tiles) != self.map_width * self.map_height:
            self.myMemory.update(status, self.seen_tiles)

        other_player_pos = []
        for sop in status.others:
            if sop is not None:
                other_player_pos.append((sop.x, sop.y))

        # Get the optimal path -> save to self.moves_to_make
        set_mine = self.compute_path(status, other_player_pos)

        mine_pos = []

        if other_player_pos != [] and set_mine:
            tiles_for_mine = self.path_to_set_mine(status, other_player_pos)

            myPos = (status.x, status.y)
            all_distances = [self.approx_distance(myPos, t) for t in tiles_for_mine]
        
            if int(status.gold/min(all_distances)) >= 30:
                mine_pos = tiles_for_mine[all_distances.index(min(all_distances))]

        # Save objects to pickle file
        self.myMemory.local_save()

        return mine_pos



players = [ROBNIC()]