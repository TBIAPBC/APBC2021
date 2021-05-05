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
            seq = ""
            for line in fh_file.readlines():
                line = line.rstrip()
                seq += line
        self.seq = seq
        self.length = len(seq)
        if self.klength > self.length:
            print("Error: K-let length greater than sequence length.", file=sys.stderr)
            sys.exit(1)
        
    #generate all k-1-lets
    def kletsm1(self):
        for i in range(self.length-self.klength+2):
            klet = self.seq[i:i+self.klength-1]
            self.km1lets.append(klet)
        self.uniquek = list(set(self.km1lets))
        self.firstk = self.km1lets[0]
        self.lastk = self.km1lets[-1]
       
    #build the directed graph
    def graph(self):
        for u in self.uniquek:
            neighbours = [self.uniquek.index(self.km1lets[x+1]) for x, y in enumerate(self.km1lets) if y == u if x < len(self.km1lets)-1]
            
            if u == self.lastk:
                tab = [u, self.uniquek.index(u), neighbours, 1, "T"]
            else:
                tab = [u, self.uniquek.index(u), neighbours, 0, "udef"]
            self.mgraph.append(tab)
        
        if self.verbose:
            print("#Graph structure after randomly selected spanning tree")
            print("symb\tid\tseen\tnext\tout_id")
            for t in self.mgraph:
                print(f"{t[0]}\t{t[1]}\t{t[3]}\t{t[4]}\t{t[2]}")
        
    #using Wilson's algorithm create random spanning trees
    def arbo(self):
        for i in range(len(self.mgraph)-1):
            u = i
            
            while self.mgraph[u][3] == 0:
                self.mgraph[u][4] = random.choice(self.mgraph[u][2])
                u = self.mgraph[u][4]
            
            u = i
            
            while self.mgraph[u][3] == 0:
                self.mgraph[u][3] = 1
                u = self.mgraph[u][4]
    
    def check_graph(self):
        c = 0
        while c != len(self.mgraph):
            c = 0
            for n in self.mgraph:
                if n[3] == 1:
                    c += 1
            if c != len(self.mgraph):
                for m in self.mgraph:
                    if m[4] != "T":
                        m[3] = 0
                self.arbo()
    
    def path(self):
        self.check_graph()
        
        shuffle_graph = copy.deepcopy(self.mgraph)
        
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
            print("symb\tid\tseen\tnext\tout_id")
            for t in shuffle_graph:
                print(f"{t[0]}\t{t[1]}\t{t[3]}\t{t[4]}\t{t[2]}")
        
        rand_seq = []
        v = self.ifirstk
        while len(rand_seq) < self.length:
            rand_seq.append(v)
            if len(shuffle_graph[v][2]) > 0:
                next_v = shuffle_graph[v][2].pop(0)
                v = next_v

        new_seq = shuffle_graph[self.ifirstk][0]
        for w in range(len(rand_seq)-(self.klength-1)):
            new_seq += shuffle_graph[rand_seq[w]][0][-1]
        
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
        print("symb\tid\tseen\tnext\tout_id")
        for t in self.mgraph:
            print(f"{t[0]}\t{t[1]}\t{t[3]}\t{t[4]}\t{t[2]}")
        
def main(args):
    if args.k < 2:
        print("Error: K-let length below minimum of 2!", file=sys.stderr)
        sys.exit(1)
    
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
    sys.exit(0)