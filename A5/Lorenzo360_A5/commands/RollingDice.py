#!/usr/bin/env python3
'''Generate N random sequences with the same length and approximately the same letter frequencies as in the input file.'''

import argparse
import sys
import random

class RollingDice:

    def __init__(self,filename):
        self.sequence=self.read_input_file(filename)
        self.letterFrequencies=self.get_letter_frequencies()

    def read_input_file(self,filename):
        try:
            file=open(filename, mode='r')
        except Exception as e:
            print(e)
            sys.exit(1)
        sequence=""
        for line in file:
            sequence=sequence+line.rstrip()

        return sequence

    def get_letter_frequencies(self):
        letter_frequencies= {}
        for i in range(0,len(self.sequence)):
            letter=self.sequence[i]
            if letter.isalpha():
                if letter in letter_frequencies:
                    letter_frequencies[letter]=letter_frequencies[letter]+1
                else:
                    letter_frequencies[letter]=1
        return letter_frequencies

    def generate_random_sequence(self):
        newSequence=""
        for i in range(0, len(self.sequence)):
            limit = 0
            r = random.random()*len(self.sequence)
            for letter in self.letterFrequencies.keys():
                limit=limit+self.letterFrequencies[letter]
                if r<=limit:
                    newSequence=newSequence+letter
                    break

        assert len(newSequence) == len(self.sequence), "Something went wrong. Generate sequence does not have same length."
        return newSequence

    def print_letter_frequencies(self, absolute=False):
        for letter in sorted(self.letterFrequencies.keys()):
            if absolute:
                print(letter, ":", self.letterFrequencies[letter])
            else:
                print(letter, ":", self.letterFrequencies[letter]/len(self.sequence))


def main(args):
    dice=RollingDice(args.filename)

    if(args.verbose):
        #print("Input Sequence:")
        #print(dice.sequence)
        print("Letter frequencies:")
        dice.print_letter_frequencies()

    for i in range(0,args.N):
        print(dice.generate_random_sequence())


def add_args(parser):
    parser.add_argument("filename", help="Inputfile with sequence to be shuffled")
    parser.add_argument("-N", required=True,type=int, help="Number of sequences to generate")
    parser.add_argument("--verbose",action="store_true", help="Print verbose output.")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)
