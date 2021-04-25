#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 11:08:01 2021

@author: milan
"""
import sys
import argparse
import random
import copy

class KLetShuffle:
    def __init__(self, file, klength, verbose):
        #initialise attributes
        self.file = file
        self.verbose = verbose
        self.seq = ""
        self.length = 0
        self.klength = klength
        self.km1lets = []
        self.uniquek = []
        self.firstk = ""
        self.lastk = ""
        self.spanning = []
        self.mgraph = []
        #call methods that are always used (once)
        self.open_file(file = file)
        self.kletsm1()
        self.ilastk = self.uniquek.index(self.lastk)
        self.ifirstk = self.uniquek.index(self.firstk)
        self.graph()
        self.arbo()

    
    def open_file(self, file):
        with open(file, "r") as fh_file:
            seq = fh_file.read()
            seq = seq.rstrip()
        self.seq = seq
        self.length = len(seq)
        
    
    #generate all k-1-lets
    def kletsm1(self):
        for i in range(self.length-self.klength+2):
            klet = self.seq[i:i+self.klength-1]
            self.km1lets.append(klet)
        self.uniquek = list(set(self.km1lets))
        self.firstk = self.km1lets[0]
        self.lastk = self.km1lets[-1]
       
    #build the directed graph stored as an adjacency matrix
    def graph(self):
        for u in self.uniquek:
            neighbours = [self.uniquek.index(self.km1lets[x+1]) for x, y in enumerate(self.km1lets) if y == u if x < len(self.km1lets)-1]
            
            if u == self.lastk:
                tab = [u, self.uniquek.index(u), neighbours, 1, "T"]
            else:
                tab = [u, self.uniquek.index(u), neighbours, 0, "udef"]
            self.mgraph.append(tab)
    
    #create random spanning trees
    #works currently just with -k 2, but not with longer k-lets
    def arbo(self):
        def tree(self, start, u, path):
            candidates = [a for a in u[2] if a != self.ilastk if a not in path]
            if len(path) == len(self.mgraph)-1 and self.ilastk in u[2]:
                path += [self.ilastk]
                self.spanning.append(path)
                return
            
            if candidates != []:
                next_u = random.choice(candidates)
                path.append(next_u)
                tree(self, start, self.mgraph[next_u], path)
            else:
                return False

        for t in self.mgraph:
            if t[4] != "T":
                tree(self, t, t, [t[1]])
    
    def path(self):
        shuffle_graph = copy.deepcopy(self.mgraph)
        rand_tree = random.choice(self.spanning)
        for k in range(len(rand_tree)):
            if shuffle_graph[rand_tree[k]][4] == "T":
                shuffle_graph[rand_tree[k]][3] = 1
            else:
                shuffle_graph[rand_tree[k]][3] = 1
                shuffle_graph[rand_tree[k]][4] = rand_tree[k+1]
        
        for tab in shuffle_graph:
            if tab[4] != "T":
                index = tab[2].index(tab[4])
                del tab[2][index]
                random.shuffle(tab[2])
                tab[2].append(tab[4])
            else:
                random.shuffle(tab[2])
            
        if self.verbose:
            print("#Graph structure after randomly selected spanning tree")
            print("symb\tid\tout_id\tseen\tnext")
            for t in shuffle_graph:
                for ti in t:
                    print(ti, end="\t")
                print("")
        
        rand_seq = []
        v = self.ifirstk
        while len(rand_seq) < self.length:
            rand_seq.append(v)
            if len(shuffle_graph[v][2]) > 0:
                next_v = shuffle_graph[v][2].pop(0)
                v = next_v
        
        new_seq = ""
        for w in rand_seq:
            new_seq += shuffle_graph[w][0]
        
        if self.verbose:
            print("#Old Sequence")
            print(self.seq)
            print("#Shuffled Sequence")
            print(new_seq)
        else:
            print(new_seq)
        
    def verbose_output(self):
        print("#Sequence of length", self.length)
        print(self.seq)
        print("#All k-1-lets")
        print(self.km1lets)
        print("#Unique k-1-lets")
        print(self.uniquek)
        print("#First k-1-let:", self.firstk)
        print("#Last k-1-let:", self.lastk)
        print("#Graph structure")
        print("symb\tid\tout_id\tseen\tnext")
        for t in self.mgraph:
            for ti in t:
                print(ti, end="\t")
            print("")
        print("#Spanning Tree(s)")
        print(self.spanning)
        
def main(args):
    if args.k < 2:
        print("Error: K-let length below minimum of 2!", file=sys.stderr)
        quit()
    
    KLS = KLetShuffle(args.filename, args.k, args.verbose)
    
    if args.verbose:
        KLS.verbose_output()
    
    for i in range(args.N):
        KLS.path()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Sequences: k-let shuffle")
    parser.add_argument("filename", help = "Input Sequence")
    parser.add_argument("-N", type=int, default=1, help="Number of random sequences printed. Default=1")
    parser.add_argument("-k", type=int, default=2, help="Length of k-lets. Default=2")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    main(parser.parse_args())
    sys.exit()