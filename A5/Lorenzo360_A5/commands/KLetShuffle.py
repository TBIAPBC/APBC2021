#!/usr/bin/env python3
'''Generate random sequences with the same k-let frequencies as in the input sequence using Euler paths.'''

import argparse
import sys
import random
import numpy as np


class KLetShuffle:
    #Special Vertex, rather special Char --> used to make degree of every node 0
    specialVertex= "@"
    def __init__(self,filename,k):
        self.k=k
        self.sequence = self.read_input_file(filename)
        self.sanity_check()
        self.kLetFrequencies = self.get_k_let_frequencies()
        self.verticesDegreeTable = self.get_vertices_degree(self.kLetFrequencies)
        self.eulerianPathExists = self.eulerian_path_exists()
        self.alphabet=np.unique(list(self.sequence))
        assert self.specialVertex not in self.alphabet, "change self.specialVertex to symbol that is not in alphabet"

    def read_input_file(self,filename):
        try:
            file=open(filename, mode='r')
        except Exception as e:
            print(e)
            sys.exit(1)
        sequence=""
        for line in file:
            sequence=sequence+line.rstrip()

        return sequence

    def sanity_check(self):
        try:
            if self.k > len(self.sequence):
                raise RuntimeError("k must not be larger than sequence length.")
        except RuntimeError as e:
            print(e)
            sys.exit(2)

    def get_k_let_frequencies(self):
        letter_frequencies = {}
        sequence=list(self.sequence)
        for i in range(0,len(sequence)-self.k+1):
            kLet="".join(list(sequence)[i:i+self.k])
            if kLet.isalpha():
                self.add_edge(letter_frequencies,kLet)
        return letter_frequencies

    def print_k_let_frequencies(self, absolute=False):
        for kLet in sorted(self.kLetFrequencies.keys()):
            if absolute:
                print(kLet, ":", self.kLetFrequencies[kLet])
            else:
                print(kLet, ":", self.kLetFrequencies[kLet]/(len(self.sequence)-self.k+1))

    def print_verticesDegreeTable(self):
        for kLet in sorted(self.verticesDegreeTable.keys()):
            print(kLet, ":", self.verticesDegreeTable[kLet])

    def get_vertices_degree(self, frequencyDict):
        verticeDegreeTable={}
        for kLet in sorted(frequencyDict.keys()):
            #Outgoing edges
            vertex="".join(list(kLet)[0:self.k-1])
            if vertex in verticeDegreeTable:
                verticeDegreeTable[vertex] = verticeDegreeTable[vertex] - frequencyDict[kLet]
            else:
                verticeDegreeTable[vertex] = -frequencyDict[kLet]
            #Incoming edges
            vertex = "".join(list(kLet)[1:self.k])
            if vertex in verticeDegreeTable:
                verticeDegreeTable[vertex] = verticeDegreeTable[vertex] + frequencyDict[kLet]
            else:
                verticeDegreeTable[vertex] = frequencyDict[kLet]
        return verticeDegreeTable

    def eulerian_path_exists(self): #Actually always satisfied for sequences of text
        unevenCount=0
        for kLet in sorted(self.verticesDegreeTable.keys()):
            unevenCount = unevenCount+self.verticesDegreeTable[kLet] % 2
        #print("uneven count: " + str(unevenCount))
        self.unevenDegreeCount=unevenCount
        return unevenCount==0 or unevenCount==2

    # Function checks whether new edge is connect to path to avoid disjunct loops
    def is_connected(self,edge,path):
        return edge[0:self.k-1] in path

    def add_edge(self,dict,edge):
        if edge in dict:
            dict[edge]=dict[edge]+1
        else:
            dict[edge]=1

    def delete_edge(self,dict,edge):
        assert edge in dict, "Cannot delete edge from dict if edge not in dict."
        dict[edge] = dict[edge] - 1
        if dict[edge]==0:
            del dict[edge]

    # Function adds edges to dict so that degree for every node in graph is 0
    # Furthermore the function connects the first edges in the graph
    def unevenDegreeInitializer(self,dict):
        startVertexList=[]
        startEdgeList=[]
        for i in range(1,self.k):
            startEdge = self.specialVertex*i + "".join(list(self.sequence)[0:self.k - i])
            finalEdge = "".join(list(self.sequence)[-self.k + i:]) + self.specialVertex*i
            startEdgeList.append(startEdge)
            self.add_edge(dict, startEdge)
            self.add_edge(dict, finalEdge)
        for i in range(self.k-2,0,-1):
            vertex="".join(list(startEdgeList[i])[0:self.k-1])
            startVertexList.append(vertex)
            del dict[startEdgeList[i]]
        self.alphabet = np.unique(list(self.sequence+self.specialVertex)) #Update alphabet to contain special character
        return startVertexList, startEdgeList[0]

    def eularian_master_path(self):
        edgeTable=self.kLetFrequencies.copy()
        masterPath=[]
        while len(edgeTable)>0:
            subPath=[]
            r = random.randint(0, len(edgeTable) - 1)
            edge = list(edgeTable.keys())[r]
            if masterPath: #if masterPath is not empty --> first edge of new subpath should be connected to vertex in masterPath
                while not self.is_connected(edge,masterPath):
                    r=random.randint(0,len(edgeTable)-1)
                    edge = list(edgeTable.keys())[r]
            else: #masterPath is empty (first path is to be added)
                if self.unevenDegreeCount:
                    path,edge=self.unevenDegreeInitializer(edgeTable)
                    if path:
                        subPath=subPath+path
            startVertex="".join(list(edge)[0:self.k-1])
            currentVertex="".join(list(edge)[1:self.k])
            subPath.append(startVertex)
            subPath.append(currentVertex)
            self.delete_edge(edgeTable,edge)
            newedgeFound=True
            while startVertex != currentVertex and newedgeFound == True:
                newedgeFound = False
                PermutedAlphabet=np.random.choice(self.alphabet, replace=False, size=len(self.alphabet))
                for letter in PermutedAlphabet:
                    edge = currentVertex+letter
                    if edge in edgeTable:
                        self.delete_edge(edgeTable, edge)
                        newedgeFound = True
                        currentVertex = "".join(list(edge)[1:self.k])
                        subPath.append(currentVertex)
                        break
            if masterPath:
                masterPath=self.join_paths(masterPath,subPath)
            else:
                masterPath=subPath
        return masterPath

    def eularian_walk(self):
        if not self.eulerianPathExists:
            print("Euler Path does not exist.")
            return ""
        masterPath=self.eularian_master_path()
        return self.vertex_path_to_sequence(masterPath)

    def vertex_path_to_sequence(self,vertexPath):
        if self.unevenDegreeCount:
            letters=[vertex[0] for vertex in vertexPath if vertex[0] is not self.specialVertex]
            return "".join(letters)
        else:
            letters = [vertex[0] for vertex in vertexPath[0:-1]] + [vertexPath[-1]]
            return "".join(letters)

    def join_paths(self,path1, path2):
        if path1[-1]==path2[0]:
            return path1+path2[1:]
        if path2[-1]==path1[0]:
            return path2 + path1[1:]
        if path1[0]==path1[-1] and path1[0] in path2:  #Inject path1 in path2
            ind=path2.index(path1[0])
            return path2[0:ind] + path1 + path2[ind + 1:]
        if path2[0] == path2[-1] and path2[0] in path1: #Inject path2 in path1
            ind=path1.index(path2[0])
            return path1[0:ind] + path2 + path1[ind + 1:]
        return []


def main(args):
    kLet=KLetShuffle(args.filename,args.k)
    if (args.verbose or args.justStats):
        print("KLet frequencies: ")
        kLet.print_k_let_frequencies(absolute=True)
        print("Vertex Degree Table:")
        kLet.print_verticesDegreeTable()
        if args.justStats:
            sys.exit(0)
    for i in range(0,args.N):
        sequence=kLet.eularian_walk()
        print(sequence)
    sys.exit(0)

def k_let_type(k):
    try:
        k=int(k)
    except Exception as e:
        raise argparse.ArgumentTypeError(e)
    if k < 2:
        raise argparse.ArgumentTypeError("Requirement k>=2 not satisfied")
    else:
        return k

def add_args(parser):
    parser.add_argument("filename", help="Inputfile with sequence to be shuffled")
    parser.add_argument("-N", required=True,type=int, help="Number of sequences to generate")
    parser.add_argument("-k", default=2, type=k_let_type, help="Number of sequences to generate")
    parser.add_argument("--verbose",action="store_true", help="Print verbose output.")
    parser.add_argument("--justStats",action="store_true",help="Just print k-let frequencies and vertex degrees.")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)
