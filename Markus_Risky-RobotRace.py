#!/usr/bin/env python3
import random
import sys
import ast
import os 
import networkx as nx
import copy

from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player


class MyPathFindingPlayer(Player):

	def __init__(self,*,RISK=True):
		self.RISK=RISK
	
	def reset(self, player_id, max_players, width, height):
		self.player_name = "Markus_Risky"
		self.ourMap = Map(width, height)
		
	def round_begin(self, r):
		#deletes remembered map from previous run
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

	def move(self, status):
		ourMap = self.ourMap

		#opens saved map file and converts string to dict, unless the file does not exist in which case it is initiated
		try:
			with open("memory_map.txt", "r") as file:
				contents = file.read()
				memory_map = ast.literal_eval(contents)
			file.close()
		except FileNotFoundError:
			memory_map = {}
			for x in range(ourMap.width):
				for y in range(ourMap.height):
					memory_map[(x, y)] = str(status.map[x, y].status)


		#we know the goldpot-location and that goldpots can only be place on empty tiles
		gLoc = next(iter(status.goldPots))
		memory_map[gLoc]="."
		curpos = (status.x,status.y)
		steps = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
		
		#is there a way of determining whether another player is within our vision and get his coordinates?
		#vision = [(x, y) for x in [-2, -1, 0, 1, 2] for y in [-2, -1, 0, 1, 2]]
		
		print(curpos)
		for x in range(ourMap.width):
			for y in range(ourMap.height):
				if abs(curpos[0] - x) <= 2 and abs(curpos[1] - y) <= 2:
					memory_map[(x, y)] = str(status.map[x, y].status)

		with open("memory_map.txt", "w") as file:
			file.write(str(memory_map))
		file.close()

		#adds nodes to the graph and adds an edge if 2 nodes in the graph are adjacent (can be reached with 1 step)
		#This risky robot assumes that all tiles are good to go except the ones which are known to be walls 
		G = nx.Graph()
		for pos, info in memory_map.items():
			if info != "#":
				G.add_node(pos)

		for node in G.nodes():
			for step in steps:
				if (node[0] + step[0], node[1] + step[1]) in G.nodes():
					G.add_edge(node,(node[0] + step[0], node[1] + step[1]))

		#print("Nodes: " + str(G.nodes))
		#print("Edges: " + str(G.edges))
		
		#if no best path can be found the position with min-distance to goldpot is defined as sink for shortest path algorithm
		if nx.has_path(G, source=curpos, target=gLoc):
			bestpath = nx.shortest_path(G, source=curpos, target=gLoc)
		else:
			distances = {}
			for node in G.nodes():
				distances[node]= abs(node[0]-gLoc[0])**(node[0]-gLoc[0]) + abs(node[1]-gLoc[1])**abs(node[1]-gLoc[1])

			#removes gLoc from dict since it cannot be reached
			minkey = min(distances, key=distances.get)
			del distances[minkey]
			minkey = min(distances, key=distances.get)

			while nx.has_path(G, source=curpos, target=minkey) == False:
				del distances[minkey]
				minkey = min(distances, key=distances.get)
			bestpath = nx.shortest_path(G, source=curpos, target=minkey)

		#makes 5 unless goldpot is closer, in order not to spend too much gold
		length = len(bestpath)
		bestpath = bestpath[1:]
		#print(bestpath)
		numMoves = 5
		if numMoves > length:
			numMoves = length
			
		return self._as_directions(curpos,bestpath[:numMoves])

players = [ MyPathFindingPlayer()]
