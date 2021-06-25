#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
import sys
from shortestpaths import AllShortestPaths
import tempfile
import numpy as np

class CuriositySuddenDeathVersion(Player):

    def __init__(self, *, random=True):
        self.random = random

    def reset(self, player_id, max_players, width, height):
        self.player_name = "Curiosity"
        self.ourMap = Map(width, height)
        self.numMoves = 3
        self.memoryFile=tempfile.gettempdir()+'/Lorenzo360-RobotRace-Mem3.npy'
        self.saveMemory()
        self.minProfit=20

    def round_begin(self, r):
        pass

    def _as_direction(self, curpos, nextpos):
        for d in D:
            diff = d.as_xy()
            if (curpos[0] + diff[0], curpos[1] + diff[1]) == nextpos:
                return d
        return None

    def _as_directions(self, curpos, path):
        return [self._as_direction(x, y) for x, y in zip([curpos] + path, path)]

    def update_map(self,status):
        for x in range(self.ourMap.width):
            for y in range(self.ourMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    self.ourMap[x, y].status = status.map[x, y].status
                    if status.map[x, y].status == TileStatus.Mine:
                        self.ourMap[x, y].status = TileStatus.Wall

    def get_shortest_path_to_gold(self,curpos,status,map):

        assert len(status.goldPots) > 0
        gLoc = next(iter(status.goldPots))
        #goldInPot = list(status.goldPots.values())[0]

        ## determine next move d based on shortest path finding
        paths = AllShortestPaths(gLoc,map)
        bestpath = paths.shortestPathFrom(curpos)
        bestpath = bestpath[1:]
        bestpath.append(gLoc) #Necessary because shortest Path apparently does not include gold position
        #Note AllShortestPath will also provid path for unkown parts of the map that are outside visibility -> just greedy direction after visibility ends
        #Note: The status object is updated in self.update_map so that it contains map information that was saved to temp file
        return bestpath

    def should_I_move(self,bestpath,status):
        distance = len(bestpath)
        # cost = status.params.cost
        ## don't move if the pot is too far away
        if self.numMoves > 0 and distance / self.numMoves > status.goldPotRemainingRounds:
            return False
        else:
            return True
    def how_many_moves_should_I_make(self,bestpath,status):
        max_steps=0
        for i,coordinate in enumerate(bestpath):
            max_steps = i
            if self.ourMap[coordinate].status==TileStatus.Unknown:
                break

        # Visualize Path
        #for i, coordinate in enumerate(bestpath):
        #    self.ourMap[coordinate].status = TileStatus.Mine
        #self.ourMap[bestpath[max_steps]].status = TileStatus.Mine
        #print(self.ourMap)
        #sys.stdout.flush()
        nsteps=max_steps+1
        distance=len(bestpath)
        # Find optimal number of steps
        while nsteps>0 and ((status.gold-self.cost_estimate(distance, nsteps)) < 0 or \
                self.profit_estimate(status,self.cost_estimate(distance, nsteps), nsteps) < self.minProfit):
            nsteps=nsteps-1

        #Further optimization of step size
        if nsteps>3:
            max_profit = self.profit_estimate(status, self.cost_estimate(distance, nsteps), nsteps)
            new_nsteps=nsteps
            maxsteps=nsteps
            for i in range(3,maxsteps):
                profit=self.profit_estimate(status,self.cost_estimate(distance, i), i)
                if profit>max_profit and (distance / i < status.goldPotRemainingRounds):
                    max_profit=profit
                    #print("Found better deal")
                    new_nsteps=i
                #print("Profit:" + str(max_profit)+" vs. "+ str(profit))
            #Compromise on speed and step size
            nsteps=round((nsteps+new_nsteps)/2)
        return nsteps

    def cost_estimate(self,distance,num_moves):
        cost= sum ([i+1 for i in range(0,num_moves)])
        #print("Cost estimate")
        #print((distance / num_moves) * cost)
        return (distance / num_moves) * cost
    def profit_estimate(self,status,cost2getthere,num_moves):
        #print("Profit estimate:")
        #print(status.params.initialGoldPotAmount-cost2getthere-num_moves)
        return status.params.initialGoldPotAmount-cost2getthere-num_moves
    def move(self, status):
        #Update map from temp file
        self.refreshMemory(status)
        self.update_map(status)
        self.saveMemory()
        #print(self.ourMap)
        # Find best path and develop move strategy
        curpos = (status.x, status.y)
        self.other_players_are_walls(status,self.ourMap) # This changed map is not saved, it is just used for best path calculation
        bestpath = self.get_shortest_path_to_gold(curpos,status,self.ourMap)
        self.numMoves=self.how_many_moves_should_I_make(bestpath,status)

        if self.should_I_move(bestpath,status):
            return self._as_directions(curpos, bestpath[:self.numMoves])
        else:
            return []

    def other_players_are_walls(self, status,map):
        if status.others!= []:
            for state in status.others:
                if state is not None:
                    map[state.x, state.y].status = TileStatus.Wall


    def refreshMemory(self,status):
        with open(self.memoryFile, 'rb') as f:
            self.ourMap=np.load(f,allow_pickle=True)[0]

    def saveMemory(self):
        with open(self.memoryFile, 'wb') as f:
            np.save(f, [self.ourMap],allow_pickle=True)

    def air_strike(self, status):
        self.refreshMemory(status)
        self.update_map(status)
        targets=[]
        if status.others!= []:
            for state in status.others:
                if state is not None and ((status.x-state.x)**2+(status.y-state.y)**2)**0.5>1.5 and  \
                        state.health>0 and state.gold+1000>status.gold: # Assuming bomb radius=1
                    targets.append((state.x, state.y))
        if status.gold > (1000 - status.params.airstrikecost*len(targets)):
            return targets
        else:
            return []

players = [CuriositySuddenDeathVersion()]
