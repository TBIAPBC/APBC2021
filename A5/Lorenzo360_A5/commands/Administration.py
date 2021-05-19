#!/usr/bin/env python3

'''Calculate possible solutions for government problem.'''

import sys
import argparse
from functools import cmp_to_key
from itertools import compress
import math
class CapitalOptimizer:

    def __init__(self,file,onlyOptimalResult=False):
        self.onlyOptimalResult=onlyOptimalResult
        self.numberOfRecursions=0
        self.maxRecursionDepth=0
        self.solutions=[]
        self.read_input(file)
        self.costDict = {key: value for key, value in
                         sorted(self.costDict.items(), key=cmp_to_key(self.compare_dict_by_value))}
        # set lowest cost to impossible high cost, will be updated in branch and bound step
        self.lowest_cost=list(self.costDict.values())[-1]* self.numberOfCapitals

    #Print some diagnostics
    def print(self):
        print("Cost List:")
        i=0
        for key, value in self.costDict.items():
            print(str(i)+". "+ key + "\t" + str(value))
            i=i+1
        print("Number of capitals: " + str(self.numberOfCapitals))
        print("Cost Limit: " + str(self.costLimit))
        print("Capitals: " + str(self.capitals))
        print("Number of recursions: " + str(self.numberOfRecursions))
        print("Theoretically possible capital pairings: "+ str(self.possible_capital_pairings()))
        print("Performance gain over brute force: " +str(self.possible_capital_pairings()*(self.numberOfCapitals/2)/self.numberOfRecursions))
        print("Maximum recursion depth: " + str(self.maxRecursionDepth))
        print("Number of solutions: "+str(len(self.solutions)))
        print("Lowest cost: " + str(self.lowest_cost))
        print("Solutions")
        self.print_solutions_and_price()


    #Calculate how many capital pairings are possible
    def possible_capital_pairings(self):
        return int(math.factorial(self.numberOfCapitals)/(math.pow(2,self.numberOfCapitals/2)*math.factorial(self.numberOfCapitals/2)))
    #Print solutions of capital problem
    def print_solutions(self):
        solutions=self.solutions.copy()
        for i,solution in enumerate(solutions):
            solutions[i]=sorted(solution)
        solutions = sorted(solutions, key=cmp_to_key(self.compare_list_of_lists))
        for solution in solutions:
            for i,capital in enumerate(solution):
                print(capital, end="")
                if i<len(solution)-1:
                    print(" ",end="")
            print()

    # Print solutions of capital problem
    def print_solutions_and_price(self):
        solutions = self.solutions.copy()
        for i, solution in enumerate(solutions):
            solutions[i] = sorted(solution)
        solutions = sorted(solutions, key=cmp_to_key(self.compare_list_of_lists))
        for solution in solutions:
            price=self.get_price_for_list_of_capitals(solution)
            for i, capital in enumerate(solution):
                print(capital, end="")
                if i < len(solution) - 1:
                    print(" ",end="")
            print(" [Price:"+str(price)+"]")

    # Print solutions of capital with price
    def get_price_for_list_of_capitals(self,solution):
        sum=0
        for capital in solution:
            sum=sum+self.costDict[capital]
        return sum
    @staticmethod
    def compare_list_of_lists(list1,list2):
        for i in range(0,min(len(list1),len(list2))):
            if list1[i] == list2[i]:
                continue
            else:
                if list1[i] < list2[i]:
                    return -1
                else:
                    return 1
        return 0

    @staticmethod
    def compare_dict_by_value(item1, item2):
            return item1[1]-item2[1]

    #Assuming that each capital name consists of only one character
    def read_input(self, file):
        self.numberOfCapitals=None
        self.costLimit=None
        self.capitals=[]
        self.costDict={}
        try:
            file = open(file, "r")
            lineNumber=0
            j=0
            for line in file.readlines():
                line=line.split()
                if lineNumber==0:
                    self.numberOfCapitals=int(line[0])
                    self.costLimit=int(line[1])
                elif lineNumber==1:
                    for capital in line:
                        assert len(capital) == 1, "Capital names are only allowed to consist of one letter"
                        self.capitals.append(capital)
                else: #Read matrix above diagonal to dictionary
                    for i in range(j+1,len(line)):
                        self.costDict[self.capitals[j]+self.capitals[i]] = int(line[i])
                    j=j+1

                lineNumber = lineNumber + 1

            file.close()
        except Exception as e:
            print(e)
            sys.exit(0)

    def price(self,v):
        return sum(list(compress(list(self.costDict.values()), v)))
    def select_keys_from_dict(self,v):
        return list(compress(list(self.costDict.keys()), v))
    def are_all_capitals_covered(self,v): # Assumes that each capital's name is just one letter
        capitalPairs=self.select_keys_from_dict(v)
        return len(set("".join(capitalPairs))) == self.numberOfCapitals and len(capitalPairs) == self.numberOfCapitals/2

    def lower_bound(self, v, index): # Check if it makes sense to branch on
        numberOfMissingPairs=self.numberOfCapitals/2-len(self.select_keys_from_dict(v))
        return self.price(v)+list(self.costDict.values())[index]*numberOfMissingPairs
    def is_solution_disjunct(self,v):
        capitalPairs = self.select_keys_from_dict(v)
        return len("".join(capitalPairs)) == len(set("".join(capitalPairs)))

    def branch_and_bound(self, v=None, currentIndex=0):
        self.numberOfRecursions = self.numberOfRecursions+1
        if self.maxRecursionDepth<currentIndex:
            self.maxRecursionDepth=currentIndex

        if currentIndex==0: # Initialisation step
            v = [False for i in range(0, len(self.costDict))]

        else:
            # Abort if price greater than cost limit or price is greater than lowest cost (only used if onlyOptimalResult is true)
            if self.price(v) > self.costLimit or (self.onlyOptimalResult and self.price(v)>self.lowest_cost):
                return

            if self.are_all_capitals_covered(v):
                if self.onlyOptimalResult and self.price(v)<self.lowest_cost:
                    self.solutions=[self.select_keys_from_dict(v)]
                    self.lowest_cost=self.price(v)
                else:
                    self.solutions.append(self.select_keys_from_dict(v))
                return

            if currentIndex+1 >= len(self.costDict): # Avoid index of bounds
                return

        if self.lower_bound(v, currentIndex)<=self.costLimit: # bounding step
            self.branch_and_bound(v.copy(), currentIndex+1) #branch 1
            v2 = v.copy()
            v2[currentIndex] = True
            if self.is_solution_disjunct(v2): # Make sure that no capital is covered twice
                self.branch_and_bound(v2, currentIndex+1) #branch 2
        else:
            return


def add_args(parser):
    parser.add_argument("filename", help="Input text file")
    parser.add_argument("-o", action='store_true', help="Print only optimal solution with lowest cost.")
    parser.add_argument("--verbose", action='store_true', help="Print verbose output.")

def main(args):
    capitalOptimizer=CapitalOptimizer(file=args.filename,onlyOptimalResult=args.o)
    capitalOptimizer.branch_and_bound()

    if args.verbose:
        capitalOptimizer.print()
    else:
        if args.o:
            print(capitalOptimizer.lowest_cost)
        else:
            capitalOptimizer.print_solutions()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)
