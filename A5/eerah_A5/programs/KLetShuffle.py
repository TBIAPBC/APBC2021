#!/usr/bin/env python3
import sys
import fileinput
import argparse
import numpy as np
import copy

def usage():
    print("Usage of K-letSchuffle: [-N number of sequences to create][-K assure frequency of sub-sequences of length k]")

def exit_abnormal():
    print("Invalid argument input")
    usage()
    sys.exit(1)

class kletschuffle:
    def __init__(self, inputfile=[], n_sequence=0, k=2):
        self.k=k-1
        self.inputfile = inputfile
        self.n_sequence = n_sequence
        self.in_sequence=""
        self.shuffle_sequence=[]
        #sym,   id, neighbors, seen, next
        # key,   0, 1        , 2   , 3
        self.kmers=[]
        self.root=""
        self.start=""
        self.multigraph=[]#vermulitch unnötig
        self.valid=False

    def print(self):
        u=self.start
        self.shuffle_sequence.append(u)
        while self.multigraph[u][1]:
            v=self.multigraph[u][1][0]
            self.multigraph[u][1].pop(0)
            u=v
            self.shuffle_sequence.append(u)
            #print(self.multigraph)
            #print(self.shuffle_sequence)
        if len("".join(self.shuffle_sequence[::self.k])) != len(self.in_sequence):
            self.shuffle_sequence="".join(self.shuffle_sequence[::self.k]) + self.shuffle_sequence[-1][-1]
        else:
            self.shuffle_sequence="".join(self.shuffle_sequence[::self.k])
        if len(self.shuffle_sequence) == len(self.in_sequence):
            self.valid=True
            print(self.shuffle_sequence)

    def print_result(self):
        u=self.start
        self.shuffle_sequence.append(u)
        while self.multigraph[u][1]:
            v=self.multigraph[u][1][0]
            self.multigraph[u][1].pop(0)
            u=v
            self.shuffle_sequence.append(u)
            #print(self.multigraph)
            #print(self.shuffle_sequence)
        if len("".join(self.shuffle_sequence[::self.k])) != len(self.in_sequence):
            self.shuffle_sequence="".join(self.shuffle_sequence[::self.k]) + self.shuffle_sequence[-1][-1]
        else:
            self.shuffle_sequence="".join(self.shuffle_sequence[::self.k])
        print(self.multigraph)
        print(self.shuffle_sequence)
        print(len(self.shuffle_sequence))

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
        self.start=self.in_sequence[0:self.k]
        for i in range(0, (len(self.in_sequence)-self.k+1)):
            self.kmers.append(self.in_sequence[i:(i + self.k)])
        self.kmers=dict(zip(self.kmers, range(0, len(self.kmers)) ))
        self.kmers={k: [[k], []] for i, k in enumerate(self.kmers)}
        self.root=self.in_sequence[i:(i + self.k)]

    def create_multigraph(self):
        for i in range(0, (len(self.in_sequence)-self.k)):
            self.kmers[self.in_sequence[i:(i+self.k)]][1].append(self.kmers[self.in_sequence[(i+1):(i+1 + self.k)]][0][0])

    #RandomTreeWithRoot(r)
    #Wilson's algorithm from https://bmcbioinformatics.biomedcentral.com/track/pdf/10.1186/1471-2105-9-192.pdf
    #The root is the last k-let of the sequence
    #starting vertex is the first k-let of the sequence (Wilson’s algorithm).
    def randomtreewithroot(self):
        self.multigraph=copy.deepcopy(self.kmers)
        [v.append([False]) for k, v in self.multigraph.items()]
        self.multigraph[self.root][2]=[True] #set

        #starting node
        counter=0
        break_bug=1000
        for idx in self.multigraph.values():
            u=idx[0][0]
            while not self.multigraph[u][2][0]:#while not "seen"
                r=np.random.choice(self.multigraph[u][1], replace=True)
                self.multigraph[u].append([r])#choose random neighbour as next
                u=r
                #u=self.multigraph[u][3][0]
            u=idx[0][0]
            while not self.multigraph[u][2][0]: #while not "seen"
                self.multigraph[u][2][0]=True #set seen to true
                u=self.multigraph[u][3][0] #go to "next"
        self.multigraph[self.root].append("root")
        #print(self.multigraph)

    def shuffle(self):
        for idx in self.multigraph:
            if self.multigraph[idx][1]:
                if len(self.multigraph[idx][1])<=1:#if there is just one neighbour no shuffle needed
                    continue
                else:
                    if not self.multigraph[idx][3] == "root":
                        zwisch=self.multigraph[idx][1]
                        zwisch.remove(self.multigraph[idx][3][0])
                        self.multigraph[idx][1]=list(np.random.choice(zwisch, size=len(zwisch), replace=False)) + [self.multigraph[idx][3][0]]
                    else:
                        pass
                        #self.multigraph[idx][1]=list(np.random.choice(zwisch, size=len(zwisch), replace=False))
        #print(self.multigraph)

    def kletshuffle(self):
        self.read_data()
        self.create_kmer_one()
        self.create_multigraph()
        counter=0
        #for i in range(0, self.n_sequence):
        while counter < self.n_sequence:
            self.shuffle_sequence=[]
            self.randomtreewithroot()
            self.shuffle()
            self.print()
            if self.valid:
                self.valid=False
                counter = counter + 1


def main(argv):
    KlettS = kletschuffle(inputfile=argv.inputfile, n_sequence=argv.N, k=argv.K)
    KlettS.kletshuffle()

    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage: [-N number of sequences to generate]")
    parser.add_argument("inputfile")
    parser.add_argument("-N", required=True, type=int, help="Number of sequences")
    parser.add_argument("-K", required=True, type=int, help="K-let")
    argv=parser.parse_args()
    main(argv)
    sys.exit()
