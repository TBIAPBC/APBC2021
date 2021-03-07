#!/usr/bin/env python3
#This program accepts a single file name for input on the command line
#Used with: python3 program_name input_file_name
#Prints "Hello World!" and the contents of the entered file 

import sys

print("Hello World!")

#Checks if more than one input file was used
if len(sys.argv) > 2:
    print("This program only accepts a single file!")
    print("Shutting down!")
    sys.exit(1)

#Checks if no input file was used
if len(sys.argv) < 2:
    print("No file name was given!")
    print("Shutting down!")
    sys.exit(1)

#Reads the input file and prints it
try:
    file = open(sys.argv[1], "r")
    for line in file.readlines():
        print(line, end='')
    file.close()
except Exception as e:
    print(e)
sys.exit(0) 
