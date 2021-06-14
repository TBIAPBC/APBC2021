#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 12:41:05 2021

@author: lino
"""
import math
from matplotlib import pyplot as plt
import random
import  networkx as nx
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
from game_utils import GameParameters



class rob(Player):
        def reset(self, player_id, max_players, width, height):
            self.player_name = "Robert"
            #self.moves = [D.up, D.left, D.down, D.right, D.up, D.up_left, D.down_left, D.down_right, D.up_right]
            self.ourMap = Map(width, height)
            self.width =width
            self.height=height
            self.move_dict={(0,1): D.up, (-1,0):D.left,( 0, -1):D.down, (1,0):D.right, (-1,  1):D.up_left, (1,  1):D.up_right, (-1,  -1):D.down_left, (1,  -1):D.down_right}
            self.G = nx.Graph()
            self.maxMoves=4
        

        def find_path(self,status):
            my_pos=(status.x,status.y)
            gpos=self.find_gold(status)
            
            # constructing the graph 
            # scaning visibel map 
            for x in range(self.ourMap.width):
                for y in range(self.ourMap.height):
                    # print(status.map[x, y])
                    if status.map[x, y].status == TileStatus.Empty:
                        
                            inspected_tile=(x,y)
                            # .... and adding empty tiles as nodes 
                            self.G.add_node(inspected_tile)
                            
                            for d in [(0,1),(-1,0),(1,-1)]:
                                other_node=(x+d[0],y+d[1])
                                if other_node[0] > self.width-1:
                                    continue
                                elif other_node[1] > self.height-1:  
                                    continue
                                    
                                elif other_node[0] < 0 or other_node[1] < 0:
                                    continue
                                else:
                                    # adding edeges between nodes if they neighbour each other 
                                    if status.map[other_node[0],other_node[1]].status == TileStatus.Empty:
                                       
                                        self.G.add_edge(inspected_tile,other_node)
                                        
           
            # if there is a path in the visibel map calculate shortest path and move with default/ high speed
            if (nx.has_path(self.G, my_pos, gpos)) == True:
                path=nx.shortest_path(self.G, my_pos, gpos)
                #print(path)
            else:
                # other wise move slower 
                 self.maxMoves=2
                 close_node=my_pos
                 for node in self.G.nodes():
                     if node == gpos:
                         continue
                     #... and search for the path to the empty tile closest to the goldpot 
                     if self.distance(pos1=close_node, pos2=gpos) > self.distance(node,gpos):
                         if (nx.has_path(self.G, my_pos, node)) == True:
                             close_node=node
                         else:
                             continue
                 path=nx.shortest_path(self.G, my_pos, close_node)
                 #print(path)
            
            # return list of tile cordinates from start to target node
            return path
        
        def move (self, status):
            my_pos=(status.x,status.y)
            gpos=self.find_gold(status)
            print(status.map)
            
                        
            for x in range(self.ourMap.width):
                for y in range(self.ourMap.height):
                    # print(status.map[x, y])
                    if status.map[x, y].status != TileStatus.Unknown:
                        self.ourMap[x, y].status = status.map[x, y].status
            
            
            path=self.find_path(status)
            
            # select the first maxMoves = curentspeed, tile sfrom the list
            path=path[0:self.maxMoves+1]
            
            moves=self.path_to_movment(status,path)
                
            if self.distance(my_pos,gpos) > (status.goldPotRemainingRounds*self.maxMoves):
                return []

            return moves
        
        def distance (self,pos1,pos2):
            dist = math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])
            return dist

        def path_to_movment(self,status,path):
            moves = []
            #get the direction and convert them with help of the dict to direction strings 
            for i in range(len(path)-1):
                
                x=path[i+1][0]-path[i][0]
                y=path[i+1][1]-path[i][1]
                
                moves.append(self.move_dict[(x,y)])
                return moves
            
        def find_gold(self,status):
            assert len(status.goldPots) > 0
            g_pos= next(iter(status.goldPots))
            return g_pos
            
        
        def round_begin(self, r):
            pass

players=[rob()]