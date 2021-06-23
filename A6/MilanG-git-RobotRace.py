#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: milan
"""
import math
import random
import networkx as nx
import tempfile
import pickle

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

        if diff in [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]:
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

            # look at options and if possible select ideal direction
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

            # if ideal direction was not possible first try a semi random one, if that fails go into a random one
            if len(moves) == i:
                cand = []
                for c in options:
                    possible = c[0].as_xy()
                    if possible[0] == ideal[0] or possible[1] == ideal[1]:
                        cand.append(c)

                if len(cand) == 0:
                    cand = options

                if cand != []:
                    rand_dir = random.choice(cand)
                    visited.append(coor)
                    coor = rand_dir[1]
                    direct = rand_dir[0].as_xy()
                    diff = (diff[0] - direct[0], diff[1] - direct[1])
                    moves.append(rand_dir[0])

        return moves

    # def set_mines(self, status):
        # pass


class Pathfinding_Bot(Player):
    # TODO: add dynamic step size,
    #       add setting of mines
    def reset(self, player_id, max_players, width, height):
        self.player_name = "Gnium"
        self.tmap = Map(width, height)
        self.moves = [D.up, D.left, D.down, D.right, D.up,
                      D.up_left, D.down_left, D.down_right, D.up_right]
        self.directions = [(0,  1), (0, -1), (-1,  0), (1,  0),
                           (-1,  1), (1,  1), (-1, -1), (1, -1)]
        self.graph = nx.DiGraph()
        self.storage = tempfile.NamedTemporaryFile()
        self.temp = self.storage.name
        self.maxmoves = 5
        self.vis_tiles = []
        self.vis_dir = {}
        self.write_mem()

    def round_begin(self, r):
        pass

    def move(self, status):
        gLoc = next(iter(status.goldPots))

        currPos = (status.x, status.y)

        # read, update and save graph
        self.read_mem()
        self.map_update(status)
        self.write_mem()
        
        # determine the shortest path
        moves = []
        path = []
        
        #is a player nearby? --> predict path and remove nodes to treat as wall
        self.predict_others(status, gLoc, currPos)
        
        #TODO: implement strategy for moving
        
        # gold location is in graph and has neigbours, i.e. was/is visible
        if nx.has_path(self.graph, currPos, gLoc):
            path = nx.shortest_path(self.graph, currPos, gLoc, method = "bellman-ford")


        # else get closer to gold pot using pythagoras as distance measure
        else:
            # find closest point in visibility range, that is accessible
            self.distance(gLoc)
            for node, dist in sorted(self.vis_dir.items(), key=lambda x: x[1]):
                if nx.has_path(self.graph, currPos, node):
                    path = nx.shortest_path(self.graph, currPos, node, method = "bellman-ford")
                if path != []:
                    break

        rad = min(len(path)-1, self.maxmoves)
        for i in range(rad):
            if status.map[path[i+1][0], path[i+1][1]].status == TileStatus.Empty:
                direction = self._as_direction(path[i], path[i+1])
                moves.append(direction)
            else:
                break

        return moves

    def set_mines(self, status):
        pass

    def distance(self, gLoc):
        for tile in self.vis_tiles:
            if self.graph.__contains__(tile):
                dist = math.sqrt((gLoc[0] - tile[0])**2 + (gLoc[1] - tile[1])**2)
                self.vis_dir[tile] = dist

    def _as_direction(self, curpos, nextpos):
        for d in D:
            di = d.as_xy()
            if (curpos[0] + di[0], curpos[1] + di[1]) == nextpos:
                return d
        return None
    
    def predict_others(self, status, gLoc, currPos):
        if status.others != []:
            for p in status.others:
                if p is not None:
                    pLoc = (p.x, p.y)
                    if self.graph.__contains__(pLoc):
                        pred_direct = [(x, y) for x in [-2,0,2] for y in [-2,0,2] if((x,y) != (0,0))]
                        predPos = {}
                        for d in pred_direct:
                            tile = (pLoc[0]+d[0], pLoc[1]+d[1])
                            if (tile[0] >= 0 and tile[0] < self.tmap.width) and (tile[1] >= 0 and tile[1] < self.tmap.height):
                                if status.map[tile].status == TileStatus.Empty:
                                    pdist = math.sqrt((gLoc[0] - tile[0])**2 + (gLoc[1] - tile[1])**2)
                                    if tile not in predPos:
                                        predPos[tile] = pdist
                        pPath = []
                        for pt, pd in sorted(predPos.items(), key=lambda x: x[1]):
                            if self.graph.__contains__(pt):
                                if nx.has_path(self.graph, pLoc, pt):
                                    pPath = nx.shortest_path(self.graph, pLoc, pt, method = "bellman-ford")
                                if pPath != []:
                                    break
                        for pMove in pPath:
                            if self.graph.__contains__(pMove) and pMove != gLoc and pMove != currPos:
                                self.graph.remove_node(pMove)
    
    def map_update(self, status):
        vis = status.params.visibility
        for x in range(self.tmap.width):
            for y in range(self.tmap.height):
                if status.map[x, y].status == TileStatus.Empty:
                    # get the tiles that are at the edge of visibility
                    if (x == status.x + vis) or (x == status.x - vis) or (y == status.y + vis) or (y == status.y - vis):
                        self.vis_tiles.append((x, y))

                    self.graph.add_node((x, y))
                    for dir in self.directions:
                        nx = x + dir[0]
                        ny = y + dir[1]
                        if (nx >= 0 and nx < self.tmap.width) and (ny >= 0 and ny < self.tmap.height):
                            if status.map[nx, ny].status == TileStatus.Empty:
                                self.graph.add_edge((x, y), (nx, ny))

    def write_mem(self):
        with open(self.temp, "wb") as temp:
            pickle.dump(self.graph, temp)

    def read_mem(self):
        with open(self.temp, "rb") as temp:
            temp.seek(0)
            self.graph = pickle.load(temp)
           

players = [Pathfinding_Bot()]  # [SemiRandBot(), Pathfinding_Bot()]
