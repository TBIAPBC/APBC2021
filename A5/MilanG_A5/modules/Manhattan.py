#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 11:27:09 2021

@author: milan
"""
import argparse
import numpy as np
import itertools
import sys

def read_file(filename, with_diag):
    
    with open(filename, "r") as fh_file:
        first_line_found = False
                
        dimension = 0
        north_south = []
        west_east = []
        diagonal_matrix = []
        
        matrix_counter = 0
        
        for l in fh_file.readlines():
            if l[0] != "#" and l != "\n":
                nl = l.rstrip("\n")
                line = nl.split(" ")
                line = [l for l in line if l]
                
                if line[0].isdigit():
                    line = [int(a) for a in line]
                else:
                    line = [float(a) for a in line]
                
                #check in which matrix block one is in the file
                if first_line_found == False:
                    dimension = len(line)
                    first_line_found = True
                    matrix_counter = 1
                
                if len(line) == dimension -1 and matrix_counter == 1:
                    matrix_counter = 2
                
                if len(west_east) == len(north_south) + 1:
                    matrix_counter = 3
                
                #add the line to the respective matrix
                if matrix_counter == 1:
                    north_south.append(line)
                
                if matrix_counter == 2:
                    west_east.append(line)
                
                if matrix_counter == 3:
                    diagonal_matrix.append(line)
    
    if len(diagonal_matrix) > 1 and with_diag == False:
        print("Diagonal Matrix detected without -d option given.\nContinuing calculation without using the diagonal matrix.")
    
    return north_south, west_east, diagonal_matrix



def manhattan(north_south, west_east, diagonal_matrix, args):
    n = len(north_south[0])
    m = len(west_east)
    if isinstance(north_south[0][0], int):
        trip = np.zeros((m, n), dtype=np.int)
    else:
        trip = np.zeros((m, n), dtype=np.float)
    
    #initialise first row and first column
    #first row
    for g in range(len(trip[0])-1):
        trip[0, g+1] = trip[0, g] + west_east[0][g]
        
    #first column
    for h in range(len(trip)-1):
        trip[h+1, 0] = trip[h, 0] + north_south[h][0]
    
    #rest of the matrix
    if args.d:
        for i, j in itertools.product(range(1, trip.shape[0]), range(1, trip.shape[1])):
            down = trip[i-1, j] + north_south[i-1][j]
            right = trip[i, j-1] + west_east[i][j-1]
            diagonal = trip[i-1, j-1] + diagonal_matrix[i-1][j-1]
            trip[i, j] = max(down, right, diagonal)

    else:
        for i, j in itertools.product(range(1, trip.shape[0]), range(1, trip.shape[1])):
            down = trip[i-1, j] + north_south[i-1][j]
            right = trip[i, j-1] + west_east[i][j-1]
            trip[i, j] = max(down, right)
       
    return trip

def route(trip, with_diag, north_south, west_east, diagonal_matrix, i, j, path=""):
    point = trip[i][j]
    
    if i == 0 and j == 0:
        return path
    else:
        #initialise variables
        n = 0
        w = 0
        d = 0
        from_north = 0
        from_west = 0
        from_diag = 0
        
        #get values from the respective score matrices and in the trip matrix for comparison
        if i - 1 >= 0:
            n = north_south[i-1, j]
            from_north = trip[i-1, j]
        
        if j - 1 >= 0:
            w = west_east[i, j-1]
            from_west = trip[i, j-1]
        
        if with_diag and i - 1 >= 0 and j - 1 >= 0:
            d = diagonal_matrix[i-1, j-1]
            from_diag = trip[i-1, j-1]
        
        #compare scores and determine the path (going south is preferred)
        if from_north + n == point:
            path = "S" + path
            i = i -1
            j = j
        elif from_west + w == point:
            path = "E" + path
            i = i
            j = j-1
        elif with_diag and from_diag + d == point:
            path = "D" + path
            i = i-1
            j = j-1
            
    return route(trip, with_diag, north_south, west_east, diagonal_matrix, i, j, path)

def main(args):
    
    north_south, west_east, diagonal_matrix = read_file(args.filename, args.d)
    
    trip = manhattan(north_south, west_east, diagonal_matrix, args)
    
    if isinstance(trip[-1][-1], float):
        print(round(trip[-1][-1], 2))
    else:
        print(trip[-1][-1])
    
    if args.t:
        sys.setrecursionlimit(max(len(north_south[0])+len(west_east), 1000))
        manhattan_path = route(trip, args.d, np.array(north_south), np.array(west_east), np.array(diagonal_matrix), len(trip)-1, len(trip[0])-1)
        print(manhattan_path)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Manhattan Tourist Problem")
    parser.add_argument("filename", help = "Input text file")
    parser.add_argument("-d", action = "store_true", help = "Include diagonal_matrix paths.")
    parser.add_argument("-t", action = "store_true", help = "Print the path from start to finish")
    main(parser.parse_args())
    sys.exit(0)