#!/usr/bin/env python3
"""
"Markus_Final": "Markus_Final-RobotRace" can be used in the runRobotRace.py file 
"""
import ast
import os 
import networkx as nx
import math

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player


class MyPathFindingPlayer(Player):

	def __init__(self):
		None
	
	def reset(self, player_id, max_players, width, height):
		self.player_name = "Markus_Final"
		self.ourMap = Map(width, height)
		
	def round_begin(self, r):
		#deletes remembered map from previous run before round 1
		if r == 1:
			if os.path.exists("memory_map.txt"):
				os.remove("memory_map.txt")
		pass

	def _as_direction(self,curpos,nextpos):
		for d in D:
			diff = d.as_xy()
			if (curpos[0] + diff[0], curpos[1] + diff[1]) ==  nextpos:
				return d
		return None

	def _as_directions(self,curpos,path):
		return [self._as_direction(x,y) for x,y in zip([curpos]+path,path)]
	
	
	def load_map(self, status):
		ourMap = self.ourMap
		#opens saved map file
		try:
			with open("memory_map.txt", "r") as file:
				contents = file.read()
				memory_map = ast.literal_eval(contents)
			file.close()
			return memory_map
		#creates it if it does not exist and enters the status of tiles
	
		except FileNotFoundError:
			memory_map = {}
			for x in range(ourMap.width):
				for y in range(ourMap.height):
					memory_map[(x, y)] = str(status.map[x, y].status)
			return memory_map
	
	
	#updates map by adding status of previously unknown tiles and changing "Player" tiles back to empty -> then saves updated file
	def update_map(self, memory_map, curpos, status):
		ourMap = self.ourMap
		gLoc = next(iter(status.goldPots))
		
		#updates map from last round
		for x in range(ourMap.width):
			for y in range(ourMap.height):
				if memory_map[(x, y)] == "P":
					memory_map[(x, y)] == "."
				if memory_map[(x, y)] == "_":
					memory_map[(x, y)] = str(status.map[x, y].status)

		#checks for other players positions in visibility
		for o in status.others:
			if o != None:
				memory_map[(o.x, o.y)]= "P"
		
		#saves the map as dict-string
		with open("memory_map.txt", "w") as file:
			file.write(str(memory_map))
		file.close()
		return memory_map


	#creates 2 networkx-graphs: "safe" uses only the nodes which are known empty tiles, "risky" additionally uses unknown tiles
	def make_nx_Graph(self, new_map):
		G_safe = nx.Graph()
		G_risky = nx.Graph()	
		steps = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
		
		for pos, info in new_map.items():
			if info == ".":
				G_safe.add_node(pos)
		for node in G_safe.nodes():
			for step in steps:
				if (node[0] + step[0], node[1] + step[1]) in G_safe.nodes():
					G_safe.add_edge(node,(node[0] + step[0], node[1] + step[1]))
		
		for pos, info in new_map.items():
			if info != "#" and info != "P":
				G_risky.add_node(pos)
		for node in G_risky.nodes():
			for step in steps:
				if (node[0] + step[0], node[1] + step[1]) in G_risky.nodes():
					G_risky.add_edge(node,(node[0] + step[0], node[1] + step[1]))
		return G_safe, G_risky
	


	#finds the best paths: safe, risky and incomplete
	def best_path(self, G_safe, G_risky, curpos, gLoc):
		
		#checks if path with known non-wall tiles can be found and finds it
		if nx.has_path(G_safe, source=curpos, target=gLoc):
			Path_Status = "Safe"
			bestpath = nx.shortest_path(G_safe, source=curpos, target=gLoc)
		#checks if path containing unknown tiles can be found and finds it
		elif nx.has_path(G_risky, source=curpos, target=gLoc):
			Path_Status = "Risky"
			bestpath = nx.shortest_path(G_risky, source=curpos, target=gLoc)
		#otherwise just determines possible path to known tile closest to gLoc
		else: 
			Path_Status = "Incomplete"
			distances = {}
			for node in G_safe.nodes():
				distances[node]= abs(node[0]-gLoc[0])**2 + abs(node[1]-gLoc[1])**2

			#removes gLoc and takes position with min-distance 
			minkey = min(distances, key=distances.get)
			del distances[minkey]
			minkey = min(distances, key=distances.get)
			
			#loops through best positions until one with a path is found 
			while nx.has_path(G_safe, source=curpos, target=minkey) == False:
				del distances[minkey]
				minkey = min(distances, key=distances.get)
			bestpath = nx.shortest_path(G_safe, source=curpos, target=minkey)
		return bestpath, Path_Status
	
	#determines costs for x amount of steps
	def movement_cost(self, length):
		cost = sum([i for i in range(1, length)])
		return cost
	
	
	#determines number of moves to be made in the turn
	def num_moves(self, bestpath, memory_map, Path_Status, status):
		gLoc = next(iter(status.goldPots))
		numMoves = 10
		l = len(bestpath)
		
		#takes only steps until an unknown tile is reached
		for i in range(len(bestpath)):
			if memory_map[bestpath[i]] == "_":
				bestpath = bestpath[:i]
				break	
		
		#checks if less moves are necessary to reach the gold pot
		if numMoves > len(bestpath):
			numMoves = len(bestpath)
		gold = status.gold
		
		#the moves in 1 turn can cost 10% of our gold maximum to avoid being stuck at ~0 gold except if maximum 5 moves are needed to reach the gold pot and we have the necessary money
		if Path_Status != "Safe" or self.movement_cost(l-1) > gold or l > 6:
			while self.movement_cost(numMoves) > gold*0.1:
				numMoves -= 1
		
		#does not move if it has less than 15 gold and the pot is more than map/2 steps away
		if gold < 15 and max(l, abs(bestpath[0][0]-gLoc[0]), abs(bestpath[0][1]-gLoc[1])) > self.ourMap.height/2:  
			numMoves = 0

		return numMoves

	
	#determines moves by creating best path and 
	def move(self, status):
		#loads map file
		ourMap = self.ourMap
		memory_map = self.load_map(status=status)
		
		#determines gLoc and fills its "empty" status into map 
		gLoc = next(iter(status.goldPots))
		memory_map[gLoc]="."
		
		#updates map with new information
		curpos = (status.x,status.y)
		new_map = self.update_map(memory_map, curpos, status=status)
		
		#creates safe and risky graphs with networkx
		G_safe, G_risky = self.make_nx_Graph(new_map)
		
		#determines shortest path with networkx 
		bestpath, Path_Status = self.best_path(G_safe, G_risky, curpos, gLoc)
		#determines "optimal" number of moves
		numMoves = self.num_moves(bestpath, memory_map, Path_Status, status=status)
		bestpath = bestpath[1:]
		return self._as_directions(curpos,bestpath[:numMoves])

players = [ MyPathFindingPlayer()]
