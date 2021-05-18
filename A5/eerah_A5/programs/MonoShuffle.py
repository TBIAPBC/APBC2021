#!/usr/bin/env python3
import sys
import fileinput
import argparse
import numpy as np
import copy

def usage():
    print("Usage: [-N number of sequences to generate] [input sequnece from file - sequnce must be in one line]")

def exit_abnormal():
    print("Invalid argument input")
    usage()
    sys.exit(1)

class monosh:
    def __init__(self, inputfile=[], n_sequence=0):
        self.inputfile = inputfile
        self.n_sequence = n_sequence
        self.in_sequence=[]
        self.shuffle_sequence=[]
        self.base_frequency={}

    def print(self):
        print("".join(e for e in self.shuffle_sequence))

    def read_data(self):
        # input data specifications:
        # input sequence must be in one line
        try:
            for line in fileinput.input(self.inputfile):
                self.in_sequence=list(str(line).rstrip())
                break
        except FileNotFoundError:
            print("File not found " + str(self.inputfile))
            exit_abnormal()

    def swap(self, i, j):#i equals current position and j is the position to change with
        zwisch=self.shuffle_sequence[i]
        self.shuffle_sequence[i]=self.shuffle_sequence[j]
        self.shuffle_sequence[j]=zwisch
        del zwisch

    def shuffle(self):
        for i in range(0, self.n_sequence):
            la = list(np.arange(0, len(self.in_sequence)))  # list from 0 to length of sequence
            self.shuffle_sequence=copy.deepcopy(self.in_sequence)
            for v, k in enumerate(self.shuffle_sequence):
                self.swap(i=v, j=np.random.choice(la))
                la.pop(0)
            self.print()

def main(argv):
    RD = monosh(inputfile=argv.inputfile, n_sequence=argv.N)
    RD.read_data()
    RD.shuffle()
    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage: [-N number of sequences to generate]")
    parser.add_argument("inputfile")
    parser.add_argument("-N", required=True, type=int, help="Number of sequences")
    argv=parser.parse_args()
    main(argv)
    sys.exit()
