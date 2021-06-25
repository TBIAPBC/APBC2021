#!/usr/bin/env python3
from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from player_base import Player
import networkx as nx
import string


class basic(Player):
	def __init__(self):
		self.gLoc_old=(0, 0)
		self.weight=100000

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

	@staticmethod
	def _distance(xy,xy1):
		return max(abs(xy1[0]-xy[0]),abs(xy1[1]-xy[1]))

	def _as_directions(self, curpos, path):
		return [self._as_direction(x, y) for x, y in zip([curpos] + path, path)]

	def get_weights_nodes(self, s, t, ourMap):
		x1, y1 = s
		x2, y2 = t
		compare=[str(ourMap[x1, y1]), str(ourMap[x2, y2])]
		if [".", "."] == compare or [".", "$"] == compare or ["$", "."] == compare:
			return 0
		else:
			return self.weight

	@staticmethod
	def get_edge_types(s, t, ourMap):
		x1, y1 = s
		x2, y2 = t
		return str(ourMap[x1, y1])+str(ourMap[x2, y2])

	def _create_graph(self, ourMap, pos_other):
		G = nx.grid_2d_graph(ourMap.width, ourMap.height)
		for s, t in G.edges():#s and t are nodes
			if s in pos_other:
				G[s][t]['weight'] = self.weight
				G[s][t]['from_to'] = self.get_edge_types(s=s, t=t, ourMap=ourMap)
			else:
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
		return G

	def update_map(self, status):
		ourMap = self.ourMap
		for x in range(ourMap.width):
			for y in range(ourMap.height):
				if status.map[x, y].status != TileStatus.Unknown:
					ourMap[x, y].status = status.map[x, y].status
		return ourMap

	def get_position_obj(self, status):
		#gets position of an object which is not the own position
		for x in range(status.map.width):
			for y in range(status.map.height):
				if str(status.map[x, y].obj).isalpha() == False and y > 0:

					if not str(status.map[x, y].obj) in string.ascii_uppercase:
						# return first found obj
						if (status.x, status.y) != (x, y):
							return (x, y)
							#print("{} : {} : {}".format(, str(status.map[x, y].obj).isalpha(), str(status.map[x, y].obj) in "ABCD"))

	def is_clear_spot(self, obj_pos, status):
		for d in D:
			diff = d.as_xy()
			coord = obj_pos[0] + diff[0], obj_pos[1] + diff[1]
			try:
				if status.map[coord].status == TileStatus.Empty:
					return coord
				else:
					return False
			except:
				#would access values outside the map
				return False

	def set_mines(self, status):
		mine_pos = []
		# if a player is in visible range
		if any([p != None for p in status.others]):
			curpos = (status.x, status.y)
			# myid=status.player
			obj_pos = self.get_position_obj(status=status)
			gLoc = next(iter(status.goldPots))
			ourMap = self.update_map(status=status)
			G = self._create_graph(ourMap=ourMap, pos_other=obj_pos)
			bestpath_target_gold = nx.shortest_path(G, source=obj_pos, target=gLoc, weight="weight")
			bestpath_target_gold.pop(0)
			if bestpath_target_gold:
				obj_pos=bestpath_target_gold[0]
			if self._distance(obj_pos, curpos) < 4 and self._distance(gLoc, curpos) < 7:
				# print("save spot at {}".format(m))
				mine_pos = [(obj_pos[0], obj_pos[1])]
		return []
		#return mine_pos

	def get_poosition_others(self, status):
		pos_other=[]
		curpos = (status.x, status.y)
		gLoc = next(iter(status.goldPots))
		#gets position of an object which is not the own position and not gold
		for x in range(status.map.width):
			for y in range(status.map.height):
				if str(status.map[x, y].obj).isalpha() == False and y > 0:
					if not str(status.map[x, y].obj) in string.ascii_uppercase:
						# return first found obj
						if curpos != (x, y) and gLoc != (x, y):
							pos_other.append((x, y))
							#print("{} : {} : {}".format(, str(status.map[x, y].obj).isalpha(), str(status.map[x, y].obj) in "ABCD"))
		return pos_other


	def move(self, status):
		ourMap = self.update_map(status=status)
		curpos = (status.x, status.y)

		#get gold location
		gLoc = next(iter(status.goldPots))
		#create graph
		pos_other=self.get_poosition_others(status)
		G = self._create_graph(ourMap=ourMap, pos_other=pos_other)
		bestpath=nx.shortest_path(G, source=curpos, target=gLoc, weight="weight")
		bestpath.pop(0)#is current position

		numMoves = 3
		if len(bestpath) > 25:
			numMoves=0

		return self._as_directions(curpos, bestpath[:numMoves])


players = [basic()]
