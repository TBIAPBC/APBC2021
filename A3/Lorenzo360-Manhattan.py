#!/usr/bin/env python3
import argparse
import sys
import numpy as np
import time

class Manhattan:

    #Class constructor
    def __init__(self, file):
        self.nNorth=-1
        self.nEast=-1
        self.northWeights=[]
        self.eastWeights=[]
        self.diagonalWeights=[]
        self.matrix=None
        self.read_input(file=file)
        self.solutions=[]

    #Print for diagnostics and verbose output
    def print(self):
        print("#North weigths")
        Manhattan.print_matrix(self.northWeights)
        print("#East weights")
        Manhattan.print_matrix(self.eastWeights)
        print("#Diagonal weights")
        Manhattan.print_matrix(self.diagonalWeights)
        print("#nNorth: " + str(self.nNorth))
        print("#nEast: " + str(self.nEast))
        print("#Matrix with (sub)solutions:")
        Manhattan.print_matrix(self.matrix)
        print("#Best score: ")
        print("%.2f" % np.round(self.get_best_score(), 2))
        print("#Solutions")
        for solution in self.solutions:
            print(solution)

    @staticmethod
    def print_matrix(matrix):
        for i in range(0,matrix.shape[0]):
            for j in range(0,matrix.shape[1]):
                print("%.2f" % np.round(matrix[i,j],2),end="\t")
            print()

    #Read input file: Automaticaly recognized HV and HVD format
    def read_input(self, file):
        try:
            f = open(file, mode='r')
        except Exception as e:
            print(e)
            sys.exit(1)
        lines_read=0
        current="None"
        nEast = 1
        for line in f:
            if line[0] != "#" and line!="\n":
                lines_read=lines_read+1
                line=line.rstrip().lstrip() # Remove trailing and leading white space characters
                weights=line.split()
                if lines_read==1:
                    self.nNorth=len(weights)
                    current="north"
                if len(weights) == self.nNorth - 1 and self.nEast == -1:
                    self.nEast=nEast
                    current="east"
                if lines_read==2*self.nEast:
                    current="diagonal"

                if current=="north":
                    self.northWeights.append(weights)
                    nEast=nEast+1
                if current=="east":
                    self.eastWeights.append(weights)
                if current=="diagonal":
                    self.diagonalWeights.append(weights)
        self.create_weight_matrices()
        f.close()

    #Reshape weight lists to numpy matrices after reading input files
    def create_weight_matrices(self):
        self.eastWeights = np.reshape(self.eastWeights, (self.nEast, self.nNorth-1))
        self.eastWeights = self.eastWeights.astype(np.float)
        self.northWeights = np.reshape(self.northWeights, (self.nEast-1, self.nNorth))
        self.northWeights = self.northWeights.astype(np.float)
        if self.diagonalWeights:
            self.diagonalWeights = np.reshape(self.diagonalWeights, (self.nEast - 1, self.nNorth - 1))
            self.diagonalWeights = self.diagonalWeights.astype(np.float)
        else:
            self.diagonalWeights=np.zeros([self.nEast - 1, self.nNorth - 1],dtype=np.float)

    #Dynamic programming algorithm to solve manhattan problem
    def dynamic_solver(self):
        self.matrix=np.zeros([self.nEast,self.nNorth],dtype=np.float)
        for i in range(1,self.nEast):
            self.matrix[i,0]=self.matrix[i-1,0] + self.northWeights[i - 1, 0]
        for i in range(1,self.nNorth):
            self.matrix[0, i] = self.matrix[0, i-1] + self.eastWeights[0, i - 1]

        for i in range(1,self.nEast):
            for j in range(1,self.nNorth):
                self.matrix[i,j]=max(self.matrix[i-1,j]+self.northWeights[i-1,j],
                                     self.matrix[i, j-1] +self.eastWeights[i, j - 1],
                                     self.matrix[i-1, j-1] +self.diagonalWeights[i-1, j - 1])

    def get_best_score(self):
        return self.matrix[self.nEast-1,self.nNorth-1]

    def back_track(self):
        sys.setrecursionlimit(max(self.nEast+self.nNorth,1000))
        self.back_track_child(i=self.nEast-1,j=self.nNorth-1)

    def back_track_child(self,i,j,solution=""):
        if i==0 and j==0:
            self.solutions.append(solution[::-1]) #Reverse backtracked path and add to solution
            return
        else:
            if i>0:
                if self.matrix[i-1,j]+self.northWeights[i-1,j]==self.matrix[i,j]:
                    self.back_track_child(i-1,j,solution+"S")
            if j>0:
                if self.matrix[i, j-1] +self.eastWeights[i, j - 1]==self.matrix[i,j]:
                    self.back_track_child(i,j-1,solution+"E")
            if i>0 and j>0:
                if self.matrix[i-1, j-1] +self.diagonalWeights[i-1, j - 1]==self.matrix[i,j]:
                    self.back_track_child(i-1,j-1,solution+"D")


def main(args):
    manhattan = Manhattan(args.filename)
    manhattan.dynamic_solver()
    if args.verbose:
        manhattan.back_track()
        manhattan.print()
    else:
        print("%.2f" % np.round(manhattan.get_best_score(),2))
        if args.t:
            manhattan.back_track()
            for solution in manhattan.solutions:
                print(solution)

def add_args(parser):
    parser.add_argument("filename", help="Format must be HV or HVD.")
    parser.add_argument("-t", action="store_true", help="Print all best paths")
    parser.add_argument("-d", action="store_true", help="Dummy flag - just implemented for specification's sake")
    parser.add_argument("--verbose",action="store_true",help="Print verbose output")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve Manhattan problem using dynamic programming.")
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)
