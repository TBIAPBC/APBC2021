# coding: utf-8

import sys
import argparse as ap
import random as rd

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

def get_frequency(sequence):
    """Get base frequencies"""
    base_count = {}
    base_frequ = []
    # Generate base:count dict
    pos = 0
    for b in sequence:
        pos += 1
        if b not in ['A','G','T','C','U']:
            print("Invalid DNA/RNA sequence. Program stopped!")
            print("Error -->", str(pos) + ". position in sequence.")
            sys.exit(0)
        if b not in base_count:
            base_count[b] = 1
            continue
        base_count[b] += 1
    # Obtain base:frequency tuples in list
    for b in sorted(base_count.keys()):
        base_frequ.append((b, base_count[b]/len(sequence)))
    
    return (base_frequ,len(sequence))

def rand_sequences(base_frequ, N):
    """Generate N random sequences with approx. equal frequency"""
    population = [t[0] for t in base_frequ[0]]
    rel_weights = [t[1] for t in base_frequ[0]]
    rand_sequ = []
    for s in range(N):
        rand_sequ.append("".join(rd.choices(population, rel_weights, k=base_frequ[1])))
    return rand_sequ

def start(args):
    """Run program"""
    sequence=read_input(args.file)
    frequencies=get_frequency(sequence)
    for s in rand_sequences(frequencies, args.N):
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