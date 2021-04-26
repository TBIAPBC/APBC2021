#!/usr/bin/env python3 
#MonoShuffle Program
#called with command "python3 MarkusBeicht-MonoShuffle.py -N 5 MonoShuffle-test30.in"
import sys
import argparse
import random

#reads input file (last argument) into string
file = open(sys.argv[-1], "r")
sequence = ""
for line in file.readlines():
	sequence += line    
file.close()
sequence = sequence[:-1]


#swaps each position in the sequence with a random position after it or with itself 
def MonoShuffle(sequence):
	#turns string to list 
	lst = []
	for s in sequence:
		lst.append(s)
	
	#swaps
	n = len(sequence) 
	for i in range(n-2):
		j = random.randint(i, n-1)
		if i < j:
			lst[i], lst[j] = lst[j], lst[i]
	
	#transforms list to string again
	result = ""
	for l in lst:
		result += l
	
	return result
	

#parses keyboard arguments for input N and input file
def add_args(parser):
	parser.add_argument("filename", help="Input text file")
	parser.add_argument("-N", required=True, type=int, help="The option -N gives the number of output sequences tha are produced.")


#calls Monoshuffle function N times
def main(args):	
	for i in range(args.N):
		print(MonoShuffle(sequence))


#calls main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates N sequecnes randomized with the MonoShuffle approach (Knuth-Fisher-Yates).")
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)
