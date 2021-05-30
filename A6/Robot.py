# -*- coding: utf-8 -*-
"""
Created on Sat May 29 20:25:56 2021

@author: Lino Boehler
"""

from player_base import  Player
from game_utils import  Direction

class My_robo(Player):
    pass



ab=Direction(1)



bot=My_robo
st=4
t="we"
#bot.move(t,st)

class test_player(Player):
	def reset(self, player_id, max_players, width, height):
		self.player_name = "test" # nameFromPlayerId(player_id)
		self.ourMap = Map(width, height)

	def round_begin(self, r):
		pass

	def move(self, status):
		# print("-" * 80)
		# print("Status for %s" % self.player_name)
		# print(status)

		ourMap = self.ourMap
		# print("Our Map, before")
		# print(ourMap)
		for x in range(ourMap.width):
			for y in range(ourMap.height):
				if status.map[x, y].status != TileStatus.Unknown:
					ourMap[x, y].status = status.map[x, y].status
		# print("Our Map, after")
		# print(ourMap)


		neighbours = []
		for d in D:
			diff = d.as_xy()
			coord = status.x + diff[0], status.y + diff[1]
			if coord[0] < 0 or coord[0] >= status.map.width:
				continue
			if coord[1] < 0 or coord[1] >= status.map.height:
				continue
			tile = ourMap[coord]
			if tile.status != TileStatus.Wall:
				neighbours.append((d, coord))
		if len(neighbours) == 0:
			print("Seriously map makers? Thanks!")
			assert False

		assert len(status.goldPots) > 0
		gLoc = next(iter(status.goldPots))
		dists = []
		for d, coord in neighbours:
			dist = max(abs(gLoc[0] - coord[0]), abs(gLoc[1] - coord[1]))
			dists.append((d, dist))
		d, dist = min(dists, key=lambda p: p[1])

		#print("Gold is at", gLoc)
		#print("Best non-wall direction is", d, "with distance", dist)
		return [d]


players = [MyNonRandomPlayer(),
           MyRandomPlayer()]
