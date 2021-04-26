#!/usr/bin/env python3 
#RollingDice Program
#called with command "python3 MarkusBeicht-RollingDice.py -N 5 RollingDice-test30.in"
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

n = len(sequence)
As = 0
Cs = 0
Gs = 0
Us = 0

#counts bases in input sequence 
for s in sequence:
	if s == "A":
		As += 1
	elif s == "C":
		Cs += 1
	elif s == "G":
		Gs += 1
	elif s == "U":
		Us += 1
	else: 
		print("Invalid input sequence")
		exit()

#generates base probabilities
As = As / n
Cs = (Cs / n) + As
Gs = (Gs / n) + Cs
Us = (Us / n) +Gs
	

def RollingDice(As, Cs, Gs, Us, n):
	#generates random number between 0 & 1 and adds base according to probabilities defined by input sequence

	seq = ""
	while len(seq) < n:
		num = random.random()
		if num < As:
			seq += "A"
		elif num < Cs:
			seq += "C"
		elif num < Gs:
			seq += "G"
		else:
			seq += "U"
	return seq
	

#parses keyboard arguments for input N and input file
def add_args(parser):
	parser.add_argument("filename", help="Input text file")
	parser.add_argument("-N", required=True, type=int, help="The option -N gives the number of output sequences tha are produced.")


#calls RollingDice function N times
def main(args):	
	for i in range(args.N):
		print(RollingDice(As, Cs, Gs, Us, n))


#calls main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates N sequecnes randomized with the RollingDice approach. ")
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)
