#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: milan
"""
import math
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

class SemiRandBot(Player):
    def reset(self, player_id, max_players, width, height):
        self.player_name = "Ron"
        self.mymap = Map(width, height)
        
    def round_begin(self, r):
        pass
    
    def map_update(self, status):
        for x in range(self.mymap.width):
            for y in range(self.mymap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    self.mymap[x, y].status = status.map[x, y].status
    
    def move(self, status):
        
        self.map_update(status)
        
        coor = (status.x, status.y)
        # get distance to nearest pot of gold
        diff = (math.inf, math.inf)
        gold = (math.inf, math.inf)
        for next_gold in status.goldPots:
            diffx = next_gold[0] - coor[0]
            diffy = next_gold[1] - coor[1]
            if diffx <= diff[0] and diffy <= diff[1]:
                gold = next_gold
                diff = (diffx, diffy)
        
        
        if diff in [(x,y) for x in [-1, 0, 1] for y in [-1, 0, 1]]:
            r = 1
        else:
            r = 2
        a = 0
        b = 0
        moves = []
        visited = []
        for i in range(0, r):
            
            if diff[0] < 0:
                a = -1
            elif diff[0] > 0:
                a = 1
            else:
                a = 0
        
            if diff[1] < 0:
                b = -1
            elif diff[1] > 0:
                b = 1
            else:
                b = 0
            
            ideal = (a, b)
            
            #look at options and if possible select ideal direction
            options = []
            for d in D:
                xy = d.as_xy()
                coord = (xy[0] + coor[0], xy[1] + coor[1])
                if (coord[0] >= 0 and coord[0] < self.mymap.width) and (coord[1] >= 0 and coord[1] < self.mymap.height):
                    field = self.mymap[coord]
                    if field.status == TileStatus.Empty and coord not in visited:
                        options.append((d, coord))
                        if xy == ideal:
                            moves.append(d)
                            visited.append(coor)
                            coor = coord
                            diff = (diff[0] - xy[0], diff[1] - xy[1])
            
            #if ideal direction was not possible first try a semi random one, if that fails go into a random one
            if len(moves) == i:
                cand = []
                for c in options:
                    possible = c[0].as_xy()
                    if possible[0] == ideal[0] or possible[1] == ideal[1]:
                        cand.append(c)

                if len(cand) == 0:
                    cand = options
                
                rand_dir = random.choice(cand)
                visited.append(coor)
                coor = rand_dir[1]
                direct = rand_dir[0].as_xy()
                diff = (diff[0] - direct[0], diff[1] - direct[1])
                moves.append(rand_dir[0])
                
        return moves
            
    #def set_mines(self, status):
        #pass

players = [SemiRandBot()]