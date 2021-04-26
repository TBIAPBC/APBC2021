# coding: utf-8

import sys
import argparse as ap
import random as rd
from copy import deepcopy

######
def read_input(filename):
    try:
        with open(filename, 'r') as file:
            sequence=""
            for line in file.readlines():
                sequence+=line.strip()
            return sequence
    except(FileNotFoundError):
        print("Input file required. Please provide or check filename.")
        sys.exit(0)

def mono_shuffle(sequence, N):
    """Fisher-Yates method"""
    n = len(sequence)
    sequence = list(sequence)
    original_sequence = deepcopy(sequence)
    for sequs in range(N):
        sequence = original_sequence
        for i in range(n-1):
            # Check sequence validity
            if sequence[i] not in ['A','G','T','C','U']:
                print("Invalid base encountered. Program stopped!")
                print("Error -->", str(pos+1) + ". position in sequence")
                sys.exit(0)
            # Get random position according to Fisher-Yates
            j = rd.randrange(i,n)
            # Swap mononucleotides in sequence
            helper = sequence[i]
            sequence[i] = sequence[j]
            sequence[j] = helper
        yield "".join(sequence)

def start(args):
    """Run program"""
    sequence = read_input(args.file)
    for s in mono_shuffle(sequence, args.N):
        print(s)
######

if __name__ == "__main__":
    cmdl_parser=ap.ArgumentParser(description="Generate N random base-sequences \
                                               and approx. preserve frequencies.")
    cmdl_parser.add_argument("file", help="Specify name of input file.")
    cmdl_parser.add_argument('-N', type=int, required=True, help="Specify number of \
                             random sequences to generate.")
    start(cmdl_parser.parse_args())
    sys.exit(0)