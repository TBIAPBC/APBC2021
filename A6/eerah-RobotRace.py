#!/usr/bin/env python3
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from player_base import Player
import networkx as nx
import pickle

class basic(Player):
	def __init__(self):
		self.gLoc_old=(0, 0)

	def reset(self, player_id, max_players, width, height):
		self.player_name = "eerah" # nameFromPlayerId(player_id)
		self.ourMap = Map(width, height)
		self.moves = [D.up, D.left, D.down, D.right, D.up, D.up_left, D.down_left, D.down_right, D.up_right]
		#print("Hi there! We are playing ",self.status.params.rounds," rounds.")

	def round_begin(self, r):
		print("Welcome to round ",r,"---",self.status.params.rounds-r+1," to go.")
		pass

	def _as_direction(self, curpos, nextpos):
		#checks which of the different directions to go up, down ... added to the current position results in the next position -
		#nextpos is the path suggested to go.
		for d in D:#iteration over directions
			diff = d.as_xy()
			if (curpos[0] + diff[0], curpos[1] + diff[1]) == nextpos:
				return d
		return None

	def _as_directions(self, curpos, path):
		return [self._as_direction(x, y) for x, y in zip([curpos] + path, path)]

	def set_mines(self, status):
		return []

	def get_weights_nodes(self, s, t, ourMap):
		x1, y1 = s
		x2, y2 = t
		compare=[str(ourMap[x1, y1]), str(ourMap[x2, y2])]
		if [".", "."] == compare or [".", "$"] == compare or ["$", "."] == compare:
			return 0
		else:
			return 100000

	def get_edge_types(self, s, t, ourMap):
		x1, y1 = s
		x2, y2 = t
		return str(ourMap[x1, y1])+str(ourMap[x2, y2])

	def move(self, status):
		ourMap = self.ourMap
		for x in range(ourMap.width):
			for y in range(ourMap.height):
				if status.map[x, y].status != TileStatus.Unknown:
					ourMap[x, y].status = status.map[x, y].status
		curpos = (status.x, status.y)

		gLoc = next(iter(status.goldPots))

		G = nx.grid_2d_graph(ourMap.width, ourMap.height)
		for s, t in G.edges():#s and t are nodes
			G[s][t]['weight'] = self.get_weights_nodes(s=s, t=t, ourMap=ourMap)
			G[s][t]['from_to'] = self.get_edge_types(s=s, t=t, ourMap=ourMap)

		#adding diagonal elements
		for x in range(ourMap.width-1):
			for y in range(0, ourMap.height-1):
				s=(x, y)
				t=(x+1, y+1)
				#print("{}, {}".format(s, t))
				G.add_edges_from([(s, t)], weight=self.get_weights_nodes(s=s, t=t, ourMap=ourMap), from_to=self.get_edge_types(s=s, t=t, ourMap=ourMap))
				s=(x+1, y)
				t=(x, y+1)
				G.add_edges_from([(s, t)], weight=self.get_weights_nodes(s=s, t=t, ourMap=ourMap), from_to=self.get_edge_types(s=s, t=t, ourMap=ourMap))

		bestpath=nx.shortest_path(G, source=curpos, target=gLoc, weight="weight")
		bestpath.pop(0)

		return self._as_directions(curpos, bestpath[:4])


players = [basic()]
