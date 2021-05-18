#!/usr/bin/env python3
import sys
import fileinput
import argparse
import numpy

def usage():
    print("Usage: [-N number of sequences to generate] [input sequnece from file - sequnce must be in one line]")

def exit_abnormal():
    print("Invalid argument input")
    usage()
    sys.exit(1)

class dice:
    def __init__(self, inputfile=[], n_sequence=0):
        self.inputfile = inputfile
        self.n_sequence = n_sequence
        self.in_sequence=""
        self.base_frequency={}

    def print(self):
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

    def get_frequency(self):
        present_bases = {base: 0 for base in
                         set(self.in_sequence)}  # unique bases in sequence e.g. {'A': 0, 'S': 0, 'D': 0, 'F': 0}
        for base in self.in_sequence:
            present_bases[base] = present_bases[base] + 1

        for base in present_bases:
            present_bases[base] = round(present_bases[base] / len(self.in_sequence), ndigits=8)
        self.base_frequency = present_bases

    def shuffle(self):
      for i in range(0, self.n_sequence):
          r=numpy.random.choice([base for base in self.base_frequency.keys()], p=[freq for freq in self.base_frequency.values()], size=len(self.in_sequence))
          print("".join(e for e in r))

def main(argv):
    RD = dice(inputfile=argv.inputfile, n_sequence=argv.N)
    RD.read_data()
    RD.get_frequency()
    RD.shuffle()
    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage: [-N number of sequences to generate]")
    parser.add_argument("inputfile")
    parser.add_argument("-N", required=True, type=int, help="Number of sequences")
    argv=parser.parse_args()
    main(argv)
    sys.exit()
