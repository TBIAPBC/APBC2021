#!/usr/bin/env python3 
import sys
import argparse 
import numpy

#reads input file line by line into string and ignores comments and empty lines
file = open(sys.argv[1], "r")
text = ""
for line in file.readlines():
	if line[0] != "#" and len(line.strip()) != 0: 
		text += line    
file.close()

#splits string into lines and creates a list of lists containing the input path weights
lines = text.split("\n")
lines = lines[:-1]
lst = []
for line in lines:
	while "  " in line:
		line = line.replace("  ", " ")
	if line[0] == " ":
		line = line[1:]
	if line[-1] == " ":
		line = line[:-1]
	w = line.split(" ")
	lst.append(w)

#parses keyboard arguments for input file, diagonal and traceback
def add_args(parser):
	parser.add_argument("filename", help="Input text file")
	parser.add_argument("-d", action='store_true', help="If option -d (for 'diagonal') is given, the program computes input files with horizontal/vertical/diagonal options.")
	parser.add_argument("-t", action='store_true', help="If option -t (for 'traceback') is given, the best path is output additionally.")

#accesses list of lists depending on chosen keyboard arguments and calls the appropriate MANHATTANTOURIST function on it 
def main(args):
	lst
	
	#for horizontal/vertical/diagonal input
	if args.d:
		z = len(lst[0])

		down_matrix = numpy.matrix(lst[:z-1])
		right_matrix = numpy.matrix(lst[z-1:2*z-1])
		diagonal_matrix = numpy.matrix(lst[2*z-1:])
		if args.t:
			print(MANHATTANTOURIST_D(z, down_matrix, right_matrix, diagonal_matrix))
		else: 
			return MANHATTANTOURIST_D(z, down_matrix, right_matrix, diagonal_matrix)
	
	#for horizontal/vertical input
	else:
		x = len(lst[0])
		y = int((len(lst) +1) /2)

		down_matrix = numpy.matrix(lst[:y-1])
		right_matrix = numpy.matrix(lst[y-1:])
		if args.t:
			print(MANHATTANTOURIST(x-1, y-1, down_matrix, right_matrix))
		else: 
			return MANHATTANTOURIST(x-1, y-1, down_matrix, right_matrix)

#MANHATTANTOURIST function for horizontal/vertical input
def MANHATTANTOURIST(m, n, Down, Right):
	#creates matrix filled with "0"s and fills the first column & row, then creates all possible paths and choses the max value for each position 
	s = numpy.zeros((n+1, m+1), dtype=int)
	for i in range(1,n):
		s[i,0] = s[i-1,0] + int(Down[i-1,0])
	for j in range(1,m):
		s[0,j] = int(s[0,j-1])+ int(Right[0,j-1])
	for i in range(1,n+1):
		for j in range(1,m+1):
			s[i,j] = max(int(s[i-1,j]) + int(Down[i-1,j]), int(s[i,j-1]) + int(Right[i,j-1]))
	
	#traceback by subtracting values at step n with values at all possible steps n-1 and checking them against path weights, stops if value "0" (starting position) is reached
	a = n
	b = m
	trace = ""
	while s[a,b] != 0:
		if s[a,b] - s[a-1,b] == float(Down[a-1, b]):
			trace += "S"
			a -= 1
		elif s[a,b] - s[a,b-1] == float(Right[a, b-1]):
			trace += "E"
			b -= 1
		else: 
			trace += "X"
			b -= 1
	path = trace[::-1]
	print(s[n,m])
	return path
	
	
	
#MANHATTANTOURIST function for horizontal/vertical/diagonal input	
def MANHATTANTOURIST_D(z, Down, Right, Diagonal):
	#creates matrix filled with "0"s and fills the first column & row, then creates all possible paths and choses the max value for each position   
	s = numpy.zeros((z, z), dtype=float)
	for i in range(1,z):
		s[i,0] = s[i-1,0] + float(Down[i-1,0])
	for j in range(1,z):
		s[0,j] = float(s[0,j-1])+ float(Right[0,j-1])
	for i in range(1,z):
		for j in range(1,z):
			s[i,j] = max(float(s[i-1,j]) + float(Down[i-1,j]), float(s[i,j-1]) + float(Right[i,j-1]), float(s[i-1,j-1]) + float(Diagonal[i-1,j-1]))
	
	#traceback by subtracting values at step n with values at all possible steps n-1 and checking them against path weights, stops if value "0" (starting position) is reached
	a = z-1
	b = z-1
	trace = ""
	while s[a,b] != 0:
		if s[a,b] == s[a, 0]:
			trace += "S"
			a -= 1
		elif s[a,b] == s[0, b]:
			trace += "E"
			b -= 1
		elif round(float(s[a,b] - s[a-1,b-1]), 2) == float(Diagonal[a-1, b-1]):
			trace += "D"
			a -= 1
			b -= 1
		elif round(float(s[a,b] - s[a-1,b]), 2) == float(Down[a-1, b]):
			trace += "S"
			a -= 1
		elif round(float(s[a,b] - s[a,b-1]), 2) == float(Right[a, b-1]):
			trace += "E"
			b -= 1
			
	path = trace[::-1]
	print(s[z-1,z-1].round(2))    
	return path



#calls main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PSolves the Manhattan Tourist problem")
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)
