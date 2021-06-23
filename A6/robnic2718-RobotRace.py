from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from player_base import Player
import random
from robnic_toolbox import (load_map_memory, move_costs, 
                            MapMemory, Astar, 
                            save_moves_to_make, load_moves_to_make, 
                            save_moves_prev_turn, load_moves_prev_turn)



class ROBNIC(Player):
    def __init__(self):
        self.player_name = "Nicolas"
        self.seen_tiles = []
        self.moves_to_make = []
        save_moves_to_make(self.moves_to_make)
        self.moves_prev_turn = (None,[],None)
        save_moves_prev_turn(self.moves_prev_turn)
        self.round = 0
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
        self.round += 1
        if random.random() <= 0.25:
            print("I can already feel the gold … I want more …")

    def decide_on_moves(self, status):
        moves_this_turn = []

        pos_players_in_reach = []
        for op in status.others:
            if op is not None:
                pos_players_in_reach.append((op.x, op.y))
        
        for _d in self.directions:
            for tile_next2me in self.coor_dir_update((status.x, status.y), _d):
                if tile_next2me in pos_players_in_reach:
                    return []

        print("\n\n\nMoves_to_make:",self.moves_to_make)
        make_all_moves = False
        for pos in self.update_coors((status.x,status.y), self.moves_to_make):
            if pos == self.gold_pos:
                make_all_moves = True
        
        if len(self.moves_to_make) <= 15:
            if not make_all_moves:
                moves_this_turn = [self.moves_to_make.pop()]
                if status.gold > 35 and random.random() <= 0.9 and self.moves_to_make != []:
                    moves_this_turn.append(self.moves_to_make.pop())
                    if status.gold > 45 and random.random() <= 0.9 and self.moves_to_make != []:
                        moves_this_turn.append(self.moves_to_make.pop())
                        if status.gold > 60 and random.random() <= 0.9 and self.moves_to_make != []:
                            moves_this_turn.append(self.moves_to_make.pop())
                            if status.gold > 80 and random.random() <= 0.9 and self.moves_to_make != []:
                                moves_this_turn.append(self.moves_to_make.pop())
                                if status.gold > 120 and random.random() <= 0.8 and self.moves_to_make != []:
                                    moves_this_turn.append(self.moves_to_make.pop())
                                    if status.gold > 150 and random.random() <= 0.8 and self.moves_to_make != []:
                                        moves_this_turn.append(self.moves_to_make.pop())
                                        if status.gold > 200 and random.random() <= 0.8 and self.moves_to_make != []:
                                            moves_this_turn.append(self.moves_to_make.pop())
                                            if self.moves_to_make != [] and random.random() <= 0.6:
                                                moves_this_turn.append(self.moves_to_make.pop())
                                                if random.random() <= 0.5 and self.moves_to_make != []:
                                                    moves_this_turn.append(self.moves_to_make.pop())
            else:
                numMoves = 0
                for n_ in range(len(self.moves_to_make)):
                    if (n_ >= 4 and status.gold <= 100) or (n_ >= 6 and status.gold <= 220) or n_ >= 8:
                        break
                    if status.gold > move_costs(n_):
                        numMoves += 1
                for _ in range(numMoves):
                    moves_this_turn.append(self.moves_to_make.pop())
        else:
            moves_this_turn = [self.moves_to_make.pop()]
            if random.random() <= 0.9 and status.gold > 40 and self.moves_to_make != []:
                moves_this_turn.append(self.moves_to_make.pop())
            if random.random() <= 0.9 and status.gold > 60 and self.moves_to_make != []:
                moves_this_turn.append(self.moves_to_make.pop())

        return moves_this_turn

    def move(self, status):
        
        myPos = (status.x,status.y)
        # Load objects from pickle file
        self.moves_prev_turn = load_moves_prev_turn()
        self.moves_to_make = load_moves_to_make()  

        # Check whether any moves have been cancelled 
        # and if so add them back to the moves_to_make
        numMoves = 0
        if self.moves_prev_turn[1] != [] and myPos != self.moves_prev_turn[0]:
            for pos in self.update_coors(self.moves_prev_turn[0], self.moves_prev_turn[1]):
                numMoves += 1
                if myPos == pos:
                    break
         
        if status.health >= 30:
            moves_this_turn = self.decide_on_moves(status)
        if status.health < 30:
            moves_this_turn = []
            
        # Remember current moves and previous position for next turn
        self.moves_prev_turn = (myPos, moves_this_turn, numMoves)
        # Save objects to pickle file
        save_moves_prev_turn(self.moves_prev_turn)
        save_moves_to_make(self.moves_to_make)
        
        return moves_this_turn
        

    def set_mines(self, status):
        
        # Since knowledge of the tiles the robot will move on is required
        # before the mines are set, the moves to make are computed before and inside
        # the set_mines function, because it is called before the move function
        
        # Load objects from pickle file
        self.myMemory = load_map_memory()
        self.moves_to_make = load_moves_to_make()
        self.moves_prev_turn = load_moves_prev_turn()

        # If goldPot has been relocated then empty self.moves_to_make and newly compute path
        if ((self.round-1) / status.params.goldPotTimeOut) == 0:
            self.moves_to_make = []

        if len(self.seen_tiles) != self.map_width * self.map_height:
            self.myMemory.update(status, self.seen_tiles)

        if self.moves_to_make == [] or self.moves_prev_turn[2] >= 1:
            myPos = (status.x,status.y)
            min_approxDist2gold = min([self.approx_distance(myPos,gp) for gp in status.goldPots.keys()])
            self.gold_pos = [item[0] for item in status.goldPots.items() if self.approx_distance(myPos,item[0]) == min_approxDist2gold][0]
            tile_approxDist = [(tile, self.approx_distance(tile, self.gold_pos)) for tile in self.myMemory.free_tiles(myPos)]
            tile_approxDist.sort(key=lambda x:x[1])
    
            for tile in tile_approxDist:
                # Initialize pathfinder
                pathfinder = Astar(self.myMemory, myPos, tile[0])
                self.moves_to_make = pathfinder.optimize()
            
                if self.moves_to_make != []:
                    break
        
        set_mine = False
        myPos = (status.x, status.y)
        for op in status.others:
            if op != None:
                set_mine = True
                
        tiles_for_mines = []
        if set_mine and random.random() <= 0.9 and status.gold >= 100:
            for _d in self.directions:
                tiles_for_mines.append(self.coor_dir_update(myPos, _d))
        if tiles_for_mines == []:
            set_mine = False
                
        # Extract positions robot will walk on to remove them
        # as possible coordinates for mine setting
        pos_to_remove = set()
        if set_mine:
            for p in self.update_coors(myPos, self.moves_to_make[-2:][::-1]):
                pos_to_remove = pos_to_remove.union([p])
        
            for tile in tiles_for_mines:
                if self.myMemory[tile] == '#':
                    pos_to_remove = pos_to_remove.union([tile])
        
        # Remove tiles the robot will walk over from tiles_for_mines list
        tiles_for_mines = list(set(tiles_for_mines) - pos_to_remove)
        
        mine_pos = []
        if tiles_for_mines != []:
            mine_pos.append(random.choice(tiles_for_mines))
        
        # Save objects to pickle file
        self.myMemory.local_save()
        save_moves_to_make(self.moves_to_make)
        save_moves_prev_turn(self.moves_prev_turn)

        return mine_pos



players = [ROBNIC()]