#!/usr/bin/env python3
import random
import sys
import math

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player

from shortestpaths import AllShortestPaths

class MyPathFindingPlayer(Player):

        def __init__(self,*,random=True):
                self.random=random

        def reset(self, player_id, max_players, width, height):
                self.player_name = "Markus_2move"
                self.ourMap = Map(width, height)

        def round_begin(self, r):
                pass

        def _as_direction(self,curpos,nextpos):
                for d in D:
                        diff = d.as_xy()
                        if (curpos[0] + diff[0], curpos[1] + diff[1]) ==  nextpos:
                                return d
                return None

        def _as_directions(self,curpos,path):
                return [self._as_direction(x,y) for x,y in zip([curpos]+path,path)]

        def move(self, status):
                ourMap = self.ourMap
                for x in range(ourMap.width):
                        for y in range(ourMap.height):
                                if status.map[x, y].status != TileStatus.Unknown:
                                        ourMap[x, y].status = status.map[x, y].status
                curpos = (status.x,status.y)
                assert len(status.goldPots) > 0
                gLoc = next(iter(status.goldPots))
                goldInPot=list(status.goldPots.values())[0]
                
                
                path_to_gold = (gLoc[0] - curpos[0], gLoc[1]-curpos[1])
                #print("Path to Gold: " + str(path_to_gold))
                #print("Gold: " + str(gLoc))
                #print("Me: " + str(curpos))
                
                #list of all possible steps in range 1 and 2 of the player
                step = [(0, 0), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
                steps = [(0, 0), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (2, 2), (2, 1), (2, 0), (2, -1), (2, -2), (1, 2), (1, -2), (0, 2), (0, -2), (-1, 2), (-1, -2), (-2, 2), (-2, 1), (-2, 0), (-2, -1), (-2, -2)]
                
                
                best_distance = math.sqrt((abs(path_to_gold[0]))**2 + (abs(path_to_gold[1]))**2)
                best_move = (0, 0)
                dist = sys.maxsize
                next_pos = [curpos]
                wide = ourMap.width
                high = ourMap.height
                
                #checks if we are next to gold-pot
                for s in step:
                	if s == path_to_gold:
                		next_pos = [gLoc]
                		return self._as_directions(curpos,next_pos)
                	
                
                #iterated through all 2-step combinations to find th valid moves which minimize the distance to the gold-pot
                for i in range(len(steps)):
                	for s in step:
                		for t in step:
                			if (s[0] + t[0], s[1] + t[1]) == steps[i]:
                				if 0 <= curpos[0]+steps[i][0] < wide and 0 <= curpos[1]+steps[i][1] < high:
                					if status.map[(curpos[0] + steps[i][0], curpos[1] + steps[i][1])].status == TileStatus.Empty:
                						possible_move = [(curpos[0] + steps[i][0], curpos[1] + steps[i][1])]
                						dist = math.sqrt((abs(path_to_gold[0] - steps[i][0]))**2 + (abs(path_to_gold[1] - steps[i][1]))**2)
                						if 0 <= curpos[0]+s[0] < wide and 0 <= curpos[1]+s[1] < high:
                							if dist < best_distance and status.map[(curpos[0] + s[0], curpos[1] + s[1])].status == TileStatus.Empty:
                								next_pos = [(curpos[0] + s[0], curpos[1] + s[1])]
                								best_distance = dist
                								best_move = steps[i]
                						elif 0 <= curpos[0]+t[0] < wide and 0 <= curpos[1]+t[1] < high:
                							if dist < best_distance and status.map[(curpos[0] + t[0], curpos[1] + t[1])].status == TileStatus.Empty:
                								next_pos = [(curpos[0] + t[0], curpos[1] + t[1])]
                								best_distance = dist
                								best_move = steps[i]
                
                
                next_pos.append((curpos[0] + best_move[0], curpos[1] + best_move[1]))
                
                #print("Next: " + str(next_pos))
                #print(next_pos[:numMoves])
                return self._as_directions(curpos,next_pos)

players = [ MyPathFindingPlayer()]
