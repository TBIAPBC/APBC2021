#!/usr/bin/env python3
import random

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
import numpy as np
import sys
import tempfile

class greedy(Player):
    def reset(self, player_id, max_players, width, height):
        self.player_name = "CheapTrick"
        self.ourMap = Map(width, height)
        self.width=width
        self.height=height
        self.moves = [D.right, D.up_right, D.up, D.up_left, D.left, D.down_left, D.down, D.down_right]
        self.move_vector=[0, 1, -1, 2, -2, 3, -3, 4]
        self.visited=np.zeros((width, height))
        self.goldpos=(-1, -1)
        self.maxMovesPerRound=3
        self.maxMovementDistance=(self.width+self.height)/1.5
        self.memoryFile=tempfile.gettempdir()+'/Lorenzo360-RobotRace-Mem.npy'
        self.saveMemory()

    def move(self, status):
        #print("?" * 80)
        #print("Status for %s" % self.player_name)
        #print(status.map)
        self.refreshMemory(status)

        directions=[]
        curPos = (status.x, status.y)
        if self.distance2gold(status, curPos=curPos)>self.maxMovementDistance:
            return directions

        for j in range(0,self.maxMovesPerRound):
            foundNewDir = False
            directionIndex=self.get_greedy_direction(status, curPos=curPos)
            self.visited[curPos[0], curPos[1]] = 1
            #print("Dir gold")
            #print(str(self.moves[directionIndex]))

            for i in range(0,len(self.moves)):
                direction=self.moves[(directionIndex+self.move_vector[i])%len(self.moves)]
                NextPosCandidate = (curPos[0]+D.as_xy(direction)[0],curPos[1]+D.as_xy(direction)[1])
                if 0<= NextPosCandidate[0] < self.width and 0 <= NextPosCandidate[1] < self.height:
                    if status.map[NextPosCandidate[0],NextPosCandidate[1]].status == TileStatus.Empty and \
                            self.visited[NextPosCandidate[0],NextPosCandidate[1]] == 0:
                        self.visited[NextPosCandidate[0],NextPosCandidate[1]] = 1
                        directions.append(direction)
                        foundNewDir=True
                        curPos=NextPosCandidate
                        break
            if not foundNewDir or NextPosCandidate == next(iter(status.goldPots)):
                break
        #print(directions)
        #print("SUM:"+str(np.sum(self.visited)))
        #sys.stdout.flush()
        self.saveMemory()
        return directions

    def distance2gold(self,status,curPos):
        goldPos = next(iter(status.goldPots))
        goldVector = (goldPos[0] - curPos[0], goldPos[1] - curPos[1])
        return goldVector[0]+goldVector[1]

    def get_greedy_direction(self,status,curPos):
        goldPos = next(iter(status.goldPots))
        goldVector = (goldPos[0] - curPos[0], goldPos[1] - curPos[1])
        if goldVector[0]>0 and goldVector[1]==0:
            return self.moves.index(D.right)
        elif goldVector[0]>0 and goldVector[1]>0:
            return self.moves.index(D.up_right)
        elif goldVector[0] == 0 and goldVector[1] > 0:
            return self.moves.index(D.up)
        elif goldVector[0] < 0 and goldVector[1] > 0:
            return self.moves.index(D.up_left)
        elif goldVector[0]<0 and goldVector[1]==0:
            return self.moves.index(D.left)
        elif goldVector[0]<0 and goldVector[1]<0:
            return self.moves.index(D.down_left)
        elif goldVector[0]==0 and goldVector[1]<0:
            return self.moves.index(D.down)
        else:
            return self.moves.index(D.down_right)

    def update_map(self,status):
        # Scan map for information
        for x in range(self.ourMap.width):
            for y in range(self.ourMap.height):
                if status.map[x, y].status != TileStatus.Unknown:
                    self.ourMap[x, y].status = status.map[x, y].status

    def refreshMemory(self,status):
        with open(self.memoryFile, 'rb') as f:
            self.goldpos=tuple(np.load(f))
            self.visited = np.load(f)
        if self.goldpos != next(iter(status.goldPots)):
            self.goldpos = next(iter(status.goldPots))
            self.visited = np.zeros((self.width, self.height))
    def saveMemory(self):
        with open(self.memoryFile, 'wb') as f:
            self.goldpos = np.save(f, self.goldpos)
            self.visited = np.save(f, self.visited)

    def round_begin(self, r):
        pass

    def set_mines(self, status):
        return []

players = [greedy()]