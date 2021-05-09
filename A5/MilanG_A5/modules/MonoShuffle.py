#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 20:35:00 2021

@author: milan
"""
import argparse
import random
import sys

class MonoShuffle:
    #initialise class variables
    def __init__(self, file, verbose):
        self.file = file
        self.verbose = verbose
        self.seq = ""
        self.length = 0
        self.empty_string = ""
        self.open_file(file=file)
        
    def open_file(self, file):
        with open(file, "r") as fh_file:
            seq = ""
            for line in fh_file.readlines():
                line = line.rstrip()
                seq += line
        self.seq = seq
        self.length = len(seq)
        if self.verbose:
            self.empty_string = self.length*" "
    
    #shuffle process
    def shuffle(self):
        if self.verbose:
            print("#Shuffle Process")
        for i in range(self.length-1):
            j = random.randint(i+1, self.length-1)
            nuc_i = self.seq[i]
            nuc_j = self.seq[j]
            self.seq = self.seq[:i] + nuc_j + self.seq[i+1:j] + nuc_i + self.seq[j+1:]
            
            if self.verbose:
                marker = self.empty_string[:i] + "V" + self.empty_string[i+1:j] + "V"
                print(marker)
                print(self.seq)
        
        if self.verbose:
            print("#Shuffled Sequence")
            print(self.seq)
        else:
            print(self.seq)
    
    def verbose_output(self):
        print("#Sequence")
        print(self.seq)
        print("#Sequence Length")
        print(self.length)

def main(args):
    MS = MonoShuffle(args.filename, args.verbose)
    
    if args.verbose:
        MS.verbose_output()
    
    for n in range(args.N):
        MS.shuffle()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Random Sequences: Mono Shuffle")
    parser.add_argument("filename", help = "Input Sequence")
    parser.add_argument("-N", type=int, default = 1, help="Number of random sequences printed. Default=1")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    main(parser.parse_args())
    sys.exit(0)