#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 09:47:01 2021

@author: milan
"""
import sys
import argparse
import random

class RollingDice:
    #initialise class variables
    def __init__(self, file, verbose):
        self.file = file
        self.seq = ""
        self.length = 0
        self.freq_dict = {}
        self.open_file(file=file)
        self.chars = []
        self.probs = []
        self.verbose = verbose
        
    def open_file(self, file):
        with open(file, "r") as fh_file:
            seq = ""
            for line in fh_file.readlines():
                line = line.rstrip()
                seq += line
        self.seq = seq
        self.length = len(seq)
    
    #determine the nucleotide composition of the sequence
    def composition(self):
        for i in self.seq:
            if i not in self.freq_dict:
                self.freq_dict[i] = 1
                self.chars.append(i)
            else:
                self.freq_dict[i] += 1
        
        self.chars = sorted(self.chars)
        
        for j in self.freq_dict:
            count = self.freq_dict[j]
            self.freq_dict[j] = count/self.length
        
        for k in sorted(self.freq_dict):
            self.probs.append(self.freq_dict[k])
    
    #generate random sequences, using the frequences from the original sequence
    def rand_seq(self):
        chars = random.choices(self.chars, weights=self.probs, k = self.length)
        chars = "".join(chars)
        
        if self.verbose:
            print("#New Random Sequence")
            print(chars)
            rand_dict= {}
            for c in chars:
                if c not in rand_dict:
                    rand_dict[c] = 1
                else:
                    rand_dict[c] += 1
            for el in rand_dict:
                rand_dict[el] = rand_dict[el]/self.length
            print("#Frequencies of the new Sequence")
            for elem in sorted(rand_dict):
                print(f"{elem}: {rand_dict[elem]}; ", end="")
            print("")
        else:
            print(chars)
    
    def verbose_output(self):
        print("#Sequence")
        print(self.seq)
        print("#Sequence Length")
        print(self.length)
        print("#Characters")
        print(self.chars)
        print("#Corresponding Probabilities")
        print(self.probs)
        print("#Random Sequences")
        
def main(args):
    RD = RollingDice(args.filename, args.verbose)
    RD.composition()
    if args.verbose:
        RD.verbose_output()
    
    for n in range(args.N):
        RD.rand_seq()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Random Sequences: Rolling Dice")
    parser.add_argument("filename", help = "Input Sequence")
    parser.add_argument("-N", type=int, default = 1, help="Number of random sequences printed. Default=1")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    main(parser.parse_args())
    sys.exit(0)