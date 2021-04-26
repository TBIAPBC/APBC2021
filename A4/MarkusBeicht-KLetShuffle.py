#!/usr/bin/env python3 
#k-let Shuffling
#called with command "python3 MarkusBeicht-KLetShuffle.py -N 5 -k 5 KLetShuffle-test30_k2.in"

import sys
import argparse
import numpy as np
import random
import copy 

#reads input file (last argument) into string
file = open(sys.argv[-1], "r")
sequence = ""
for line in file.readlines():
	sequence += line    
file.close()
sequence = sequence[:-1]
paths = []



#command line arguments -N and -k 
N = int(sys.argv[2])
k = int(sys.argv[4])
if k <2:
	print("Parameter -k has to be >= 2")
	exit()



#Prepares list of unique nodes, list of lists containing edges, and adjacency list like dictionary 
def Prep(sequence, k):
	#determines subsequences (k_lets) of length k-1
	n = len(sequence)
	k_lets = []
	for i in range(n-k+2):
		k_lets.append(sequence[i:i+k-1])
	
	
	#removes duplicate nodes
	unique_nodes = list(dict.fromkeys(k_lets))
	
	#determines all possible directed edges
	edges = []
	for i in range(n-k+1):
		edge = [sequence[i:i+k-1], sequence[i+1:i+k]] 
		edges.append(edge)

	
	#changes directed edges list to their indices
	edges_num = []
	for edge in edges:
		edge_num = []
		edge_num.append(unique_nodes.index(edge[0]))
		edge_num.append(unique_nodes.index(edge[1]))
		edges_num.append(edge_num)
	
	#creates adjacency like dictionary 
	dic = {}
	for key, val in edges_num:
		dic.setdefault(key, []).append(val)
	
	return edges_num, dic, unique_nodes, n






#finds Euleraian Cyle/Path by calling depth first search function until a path with the full length is found 
def FindEulerianPath(edges, dictionary, n):
	indeg = CountInDegrees(edges, n)
	outdeg = CountOutDegrees(edges, n)
	if GraphHasEulerianPath(outdeg, indeg) == 1:
		None
		#print("Eulerian Cyle")
	elif GraphHasEulerianPath(outdeg, indeg) == 2:
		None
		#print("Eulerian path")
	else: 
		return "No Eulerain Path"
	
	#initiates search after finding start node
	DFS(FindStartNode(outdeg, indeg), outdeg, dictionary)
	if len(paths) == len(edges)+1: 
		path = paths[::-1]
		return path
	else:
		return None


#counts out-degrees for all nodes
def CountOutDegrees(edges, n):
	outdeg = []
	for i in range(n):
		out = 0
		for edge in edges:
			if edge[0] == i:
				out += 1
		outdeg.append(out)
	return outdeg


#counts in-degrees for all nodes
def CountInDegrees(edges, n):
	indeg = []
	for i in range(n):
		ind = 0
		for edge in edges:
			if edge[1] == i:
				ind += 1
		indeg.append(ind)
	return indeg


#checks if a Eulerian Cycle/Path can be found based on the node degrees 
def GraphHasEulerianPath(outdeg, indeg):
	start_nodes, end_nodes = 0, 0
	for i in range(len(outdeg)):
		if (outdeg[i] - indeg[i]) > 1 or (indeg[i] - outdeg[i]) > 1:
			return False
		elif (outdeg[i] - indeg[i]) == 1:
			start_nodes += 1
		elif (indeg[i] - outdeg[i]) == 1:
			end_nodes += 1
	if end_nodes == 0 and start_nodes == 0:
		return 1
		#Eulerian Cycle
	elif end_nodes == 1 and start_nodes == 1:
		return 2
		#Eulerian Path


#finds starting node by looking for node with (outdegree - indegree = 1) 
def FindStartNode(outdeg, indeg):
	start = 0
	for i in range(len(outdeg)):
		#Identifies 1 possible start node in euler path
		if outdeg[i] - indeg[i] == 1:
			return i
		#chooses start node for euler cycle which has outgoing edges
		if outdeg[i] > 0: 
			return i

#Performs depth first search until all outdegrees are 0
def DFS(position, outdeg, dictionary):
	global paths
	while outdeg[position] != 0:
		
		#chooses random adjacent node from dictionary and removes it, increments outdegree
		next_position = dictionary[position].pop(random.randint(0, len(dictionary[position])-1))
		outdeg[position] -= 1
		
		#calls DFS on the next node with the updated outdegrees & dictionary until all outdegrees are 0
		DFS(next_position, outdeg, dictionary)
	paths = paths + [position]






#finds 10000 EulerianPaths and saves all unique paths
all_paths = []
edges_index, dictionary, unique_nodes, n = Prep(sequence, k)

i = 10000
while i > 0:
	edges_copy = edges_index[:]
	dictionary_copy = copy.deepcopy(dictionary)
	paths = []
	new_path = (FindEulerianPath(edges_copy, dictionary_copy, n))
	if new_path not in all_paths and new_path != None:
		all_paths.append(new_path)
	i -= 1


#randomly choses and prints 1 of the paths (as sequence), N times
for i in range(N):
	one_path = all_paths[random.randint(0, len(all_paths)-1)]
	
	result = unique_nodes[one_path[0]]
	for j in range(1, len(one_path)):
		result += unique_nodes[one_path[j]][-1]
	print(result)
