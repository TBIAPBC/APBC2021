#!/usr/bin/python3
import sys
import fileinput
import argparse
import numpy as np
import itertools
import copy

def usage():
    print("Usage of K-letSchuffle: [-N number of sequences to create][-K assure frequency of sub-sequences of length k]")

def exit_abnormal():
    print("Invalid argument input")
    usage()
    sys.exit(1)

class kletschuffle:
    def __init__(self, inputfile=[], n_sequence=0, k=2):
        self.k=k
        self.inputfile = inputfile
        self.n_sequence = n_sequence
        self.in_sequence=""
        self.shuffle_sequence=[]
        self.base_frequency={}
        #sym,id, neighbors, seen, next
        self.kmers=[]
        self.multigraph=[]#vermulitch unnötig

    def print(self):
        print(self.kmers)
        print(self.in_sequence)

    def read_data(self):
        # input data specifications:
        # input sequence must be in one line
        try:
            for line in fileinput.input(self.inputfile):
                self.in_sequence=str(line).rstrip()
                break
        except FileNotFoundError:
            print("File not found " + str(self.inputfile))
            exit_abnormal()

    def create_kmer_one(self):
        for i in range(0, (len(self.in_sequence)-1)):
            self.kmers.append(self.in_sequence[i:(i + self.k - 1)])
        self.kmers=dict(zip(self.kmers, range(0, len(self.kmers)) ))
        self.kmers={k: [[i], []] for i, k in enumerate(self.kmers)}

    def create_multigraph(self):
        for i in range(0, (len(self.in_sequence)-1)):
            self.kmers[self.in_sequence[i:(i+self.k-1)]][1].append(self.kmers[self.in_sequence[(i + 1):(i + self.k)]][0][0])



def main(argv):
    parser = argparse.ArgumentParser(description="Usage: [-N number of sequences to generate]")
    parser.add_argument("inputfile")
    parser.add_argument("-N", required=True, type=int, help="Number of sequences")
    parser.add_argument("-K", required=True, type=int, help="K-let")
    argv=parser.parse_args()
    KlettS = kletschuffle(inputfile=argv.inputfile, n_sequence=argv.N, k=argv.K)
    KlettS.read_data()
    KlettS.create_kmer_one()
    KlettS.create_multigraph()
    KlettS.print()
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit()
