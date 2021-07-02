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
import pickle
import tempfile
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
            self.G_viz= nx.Graph()
            self.maxMoves=5
            self.move_limit=10
            self.temp_file=tempfile.NamedTemporaryFile()
            self.write_memory()
            
            
            
        def up_date_map(self,status):
        #constructing the graph 
        # scaning visibel map 
            for x in range(self.ourMap.width):
                for y in range(self.ourMap.height):
                    # print(status.map[x, y])
                    if status.map[x, y].status == TileStatus.Empty:
                        
                            inspected_tile=(x,y)
                            # .... and adding empty tiles as nodes 
                            self.G_viz.add_node(inspected_tile)
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
                                        self.G_viz.add_edge(inspected_tile,other_node)
            #memory=pickle.dump(memoryG,open( "graph_memory", "wb" ))


       


        def find_path(self,status):
            my_pos=(status.x,status.y)
            gpos=self.find_gold(status)
           
            
            # if there is a path in the visibel map calculate shortest path and move with default/ high speed
            if (nx.has_path(self.G, my_pos, gpos)) == True:
                path=nx.shortest_path(self.G, my_pos, gpos)
                #print(path)
            else:
                # other wise move slower 
                 self.maxMoves=3
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
            #print(status.map)
            
            print(self.status.others)
            
            for x in range(self.ourMap.width):
                for y in range(self.ourMap.height):
                    # print(status.map[x, y])
                    if status.map[x, y].status != TileStatus.Unknown:
                        self.ourMap[x, y].status = status.map[x, y].status
            
            # up date and save memory 
            self.read_memory()
            self.up_date_map(status)
        
            self.write_memory()
            
            
            
            path=self.find_path(status)
            #self.maxMoves=self.speed(path,status)
           
            
            #print(path)
            if self.status.gold < 16 :
                if len(path)+1 > 6:
                    self.maxMoves=1
                else: 
                    self.maxMoves=5
            # select the first maxMoves = curentspeed, tile sfrom the list
            if len(path)+1 < self.maxMoves:
                self.maxMoves=len(path)+1 
                
            path=path[0:self.maxMoves+1]
            #print(path)
            
            moves=self.path_to_movment(status,path)
            
            self.predict_others()
            
            #if self.cost_movment(self.distance(my_pos,gpos)) > status.goldPots[gpos]+status.goldPots[gpos]*0.2:
                #return []
            
            if self.distance(my_pos,gpos) > (status.goldPotRemainingRounds*self.maxMoves):
               return []

            return moves
        
        def predict_others():
            pass
        
        def distance (self,pos1,pos2):
            dist = math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])
            return dist

        def path_to_movment(self,status,path):
            if len(path) == 0:
                return (0,0)
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
            
        def cost_movment(self,n):
            #n=len(moves)
            cost_m=(n**2+n)/2
            return cost_m
        
        def speed(self,path,status):
            gpos=self.find_gold(status)
            my_pos=(status.x,status.y)
            #steps=int()
            # precentage of gold pot vaule to pay for movement
            gold_pr=0.5
            gold=status.goldPots[gpos]/2
            if (nx.has_path(self.G, my_pos, gpos)) == True:
                l=len(path)
                
                # optimize step number
                steps=self.opt_cost(l, gold,gold_pr)
                    
                if (nx.has_path(self.G_viz, my_pos, gpos)) == True:
                    return round(steps*1.5)
                else:
                    return steps
                
            else:
                l=self.distance(my_pos,gpos)
                
                steps=self.opt_cost(l,gold,gold_pr)
                
                return 3 #round(steps*0.4)
                
        def opt_cost(self,l,gold,gold_pr):
            prev=[]
            l=round(l)
            
            for i in range(1,11):
                    rest=l%i
                    
                    m=int(l/i)
                    cost1=(i**2+i)/2 
                    
                    if rest > 0:
                        ex_cost=cost1*(m-1)+(rest**2+rest)/gold_pr
                    else:
                        ex_cost=cost1*m
                    
                    prev.append(ex_cost)
                    
                    if i == l:
                        return i
                    if ex_cost >= gold:
                        #number_steps=ex_cost
                        if abs(prev[i-2]-gold) > abs(ex_cost-gold):
                            steps=i-1
                            return steps
                            #break
                        else:
                            steps=i
                            return steps
                            #break
                    if i == 10:
                        return i
                    
        def round_begin(self, r):
            pass

        def read_memory(self):
            with open( self.temp_file.name,"rb") as f_in:
                self.G=pickle.load(f_in)
            #return memoryG
        
        def write_memory(self):
            with open( self.temp_file.name,"wb") as f_out:
                pickle.dump(self.G,f_out)
                
players=[rob()]
