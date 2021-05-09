#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import itertools
import math
import sys

def cost(pair, capitals, matrix):
    i1 = capitals.index(pair[0])
    i2 = capitals.index(pair[1])
    cost = matrix[i1, i2]
    return int(cost)

def branch_bound(combis, nocap, maxcost, cost_dict, args):
    
    if args.o:
        best = math.inf
        solution = []
    else:
        solutions = []
    
    
    tree = {}
    for i in combis:
        if cost_dict[i] < maxcost:
            #initialise the search tree with single combinations
            if i not in tree:
                tree[i] = cost_dict[i]
            
            #create separate dict to add new nodes, will be combined later with the dict tree
            new_node_dict = {}
            
            for admin in tree:
                ad_list = admin.split(" ")
                
                #check for duplicates in new node if the next pair would be added to the old one
                current_cities = []
                for couple in ad_list:
                    current_cities.append(couple[0])
                    current_cities.append(couple[1])
                    
                if i[0] not in current_cities and i[1] not in current_cities:
                    
                    #sort node to avoid duplicates
                    new = ad_list + [i]
                    new_ad = sorted(new)
                    
                    #calculate the new cost
                    new_cost = tree[admin] + cost_dict[i]
                    
                    new_node = str(new_ad[0])
                    for k in new_ad[1:]:
                        new_node += " " + k
                    
                    #if optimisation is wanted, only the best solution is saved
                    if args.o:
                        if len(new_ad) == nocap/2 and new_cost < best:
                            best = new_cost
                            solution = []
                            solution.append(new_node + ": "  + str(best))
                        elif len(new_ad) == nocap/2 and new_cost == best:
                            solution.append(new_node + ": " + str(best))
                    
                    #otherwise save all eligible solutions
                    elif len(new_ad) == nocap/2 and new_node not in solutions and new_cost <= maxcost:
                        solutions.append(new_node)
                    
                    #store new nodes
                    if new_cost <= maxcost and len(new_ad) <= nocap/2:
                        if new_node not in new_node_dict and new_node not in tree:
                            new_node_dict[new_node] = new_cost
                    
            #update the tree dictionary with the new nodes
            for l in new_node_dict:
                if l not in tree:
                    tree[l] = new_node_dict[l]
    
    if args.o:
        return sorted(solution)
    else:
        return sorted(solutions)

def main(args):
    with open(args.filename, "r") as fh_file:
        content = []
        for i in fh_file.readlines():
            content.append(i.rstrip("\n"))
    
    #extract the number of capitals and the maximum cost from the file
    nocap, maxcost = content[0].split(" ")
    
    #store capitals in a list
    capitals = content[1].split(" ")
    capitals = [a for a in capitals if a != ""]
    
    c_list = []
    for l in content[2:]:
        sl = l.split(" ")
        sl = [b for b in sl if b != ""]
        c_list.append(sl)
    
    matrix = np.array(c_list)
    
    #get all possible combinations of capitals, without duplicates
    cap_string = ("").join(capitals)
    combis = [c[0]+c[1] for c in itertools.combinations(cap_string, 2)]
    
    cost_dict = {}
    for i in combis:
        combi_cost = cost(i, capitals, matrix)
        if i not in cost_dict:
            cost_dict[i] = int(combi_cost)
    
    
    solution = branch_bound(combis, int(nocap), int(maxcost), cost_dict, args)
    for s in solution:
            print(s)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Optimizing the administration of Atirasu")
    parser.add_argument("filename", help="Input text file")
    parser.add_argument("-o", action="store_true", help="Optimises the cost and prints the best solution.")
    main(parser.parse_args())
    sys.exit(0)