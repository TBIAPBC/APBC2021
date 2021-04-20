#!/usr/bin/env python3
import argparse
import sys
import random


#Implements FisherYatesShuffle
class MonoShuffle:

    def __init__(self, filename):
        self.sequence = self.read_input_file(filename)

    def read_input_file(self, filename):
        try:
            file=open(filename, mode='r')
        except Exception as e:
            print(e)
            sys.exit(1)
        sequence = ""
        for line in file:
            sequence = sequence+line.rstrip()
        return sequence

    def gernerate_permuted_sequence(self):
        newSequence = list(self.sequence)
        for i in range(0, len(newSequence)-1):
            r = random.randint(i, len(newSequence)-1)  # Generates random int with low<=r<=high
            temp = newSequence[i]
            newSequence[i] = newSequence[r]
            newSequence[r] = temp
        return "".join(newSequence)


def main(args):
    shuffle = MonoShuffle(args.filename)
    for i in range(0,args.N):
        print(shuffle.gernerate_permuted_sequence())


def add_args(parser):
    parser.add_argument("filename", help="Inputfile with sequence to be permuted")
    parser.add_argument("-N", required=True, type=int, help="Number of sequences to generate")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use Fisher-Yates algorithm to permute a sequence of letters. ")
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)

