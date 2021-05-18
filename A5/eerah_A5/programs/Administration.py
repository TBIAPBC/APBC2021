#!/usr/bin/env python3

#Traveling salesman problem (TSP)
#Approximately solved by branch and bound optimazation algorithm.

import linecache
import sys
import numpy as np
import pandas as pd
from math import inf


def usage():
    print("Usage: [input file missing]")


def exit_abnormal():
    print("Invalid argument input")
    usage()
    sys.exit(1)



class BBTreeNode:

    def __init__(self, cost=0, constraint=0, feasible=[], solution=[], CM=[], final_solution =[]):
        #self.ownnode=feasible[0]
        self.cost = cost  # contains the cost
        self.constraint = constraint
        self.feasible = feasible  # what nodes can be expanded
        self.solution = solution  # contains the current solution (BE, IG...)
        self.CM=CM
        self.final_solution=final_solution


    def check_cost(self):
        #returns true and continues if cost < constraints
        if self.cost > self.constraint:
            return False
        return True

    def update_cost(self):
        if isinstance(self.solution, list):
            node=self.solution[-1]
        if isinstance(self.solution, str):
            node=self.solution
        self.cost=self.cost+self.CM[node[0]][node[1]]


    def update_feasible(self):
        feasible = self.feasible.copy()
        if isinstance(self.solution, list):
            node=self.solution[-1]
        if isinstance(self.solution, str):
            node=self.solution
        # feasible is a list of possible nodes - delets the current "added" node from the lsit
        for ci in range(0, len(node)):
            c = node[ci]
            to_pop = []
            for i in feasible:
                # returns position of the match if its not present returns -1
                if i.find(c) >= 0:
                    to_pop.append(i)
            if isinstance(feasible, list):
                [feasible.remove(s) for s in to_pop]

            if isinstance(feasible, str):
                feasible=[]

        return feasible

    def update_finalsolution(self):
        global result
        if not result:
            result = [self.solution + [self.cost]]
        else:
            bool_res = []
            for a in result:
                bool_res.append(set(a) == set(self.solution + [self.cost]))
            if sum(bool_res) == 0:
                result.append(self.solution + [self.cost])

    def bab(self):
        self.update_cost()
        if self.check_cost()==True:
            feasible = self.update_feasible()
            if isinstance(feasible, list):  # len(self.feasible) > 0:
                # meaning if there ary any possible solutiosn left
                if isinstance(self.solution, str):
                    for f in feasible:
                        zwisch = [self.solution] + [f]
                        BB = BBTreeNode(cost=self.cost, constraint=self.constraint, feasible=feasible, solution=zwisch, CM=self.CM)
                        BB.bab()
                if isinstance(self.solution, list):
                    # meaning if there ary any possible solutiosn left
                    for f in feasible:
                        zwisch = self.solution + [f]
                        BB = BBTreeNode(cost=self.cost, constraint=self.constraint, feasible=feasible, solution=zwisch, CM=self.CM)
                        BB.bab()


            # last case if feasible is string is missing
            if not feasible:
                self.update_finalsolution()
                #result = self.solution



def main(argv):
    if not argv:
        usage()
        sys.exit(1)

    inputfile = argv[-1]
    argv = [a.lower() for a in argv]  # excepts iI and lL cases
    opti = False
    if not argv:
        exit_abnormal()
    ignore_t = False
    word = False
    arg = list(set(argv))  # removes duplicates
    for opt in argv:
        if opt in "-o":
            arg.remove("-o")
            opti = True

    #Data preparation start
    try:
        nc, upbound = map(int, linecache.getline(inputfile, 1).split())  # check for integers nc=number of cities and upbound maximum cost
    except Exception as e:
        print(e)

    try:
        # get citiie names
        cities = linecache.getline(inputfile, 2).split()
        #read cost data
        dtype = [(c, np.int_) for c in cities]
    except Exception as e:
        print(e)

    try:
        df=np.genfromtxt(inputfile, skip_header=1, dtype=dtype, names=True )#, names =["a", "b", "c", "d", "e", "f", "g", "h"])#cost matrix
        CM=pd.DataFrame(df, index=cities)
        CM[CM>upbound] = inf #Sets all values exceedign the upper boundary upbound to infinity
        CM[CM == -1] = inf #diagonal elements to inf
        CM[CM == 0] = inf #sets values which can no be reached to inf

    except Exception as e:
        print(e)
    #Data preparation end

    #creating feasible solutions BE and EB are the same
    start_feasible=[]
    for i in range(len(CM.columns)):
        for j in range(i + 1, len(CM.columns)):
            start_feasible.append(CM.columns[i] + CM.columns[j])

    initial_nodes=[]
    for i in range(1, len(CM.columns)):
        #creates initial nodes
        initial_nodes.append(CM.columns[0] + CM.columns[i])

    global result
    result = []
    for init in range(0, len(initial_nodes)):
        # start with first node
        node = initial_nodes[init]
        # access costs
        cost = CM[str(node[0])][str(node[1])]
        #def __init__(self, cost=0, constraint=0, feasible=[], solution=[]):
        BB=BBTreeNode(cost=0, constraint=upbound, feasible=start_feasible, solution=node, CM=CM)
        BB.bab()


    if opti:
        print(min([r[-1] for r in result]))
    else:
        for r in result:
            print(' '.join(r[0:-1]))


if __name__ == "__main__":
    main(sys.argv[1:3])
    sys.exit()