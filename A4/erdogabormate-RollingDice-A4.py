#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14  13:47:09 2021
@author: erdogabormate
"""

import random
import re
import argparse

# filename and number of repeats are parsed from the input arguments 

my_parser = argparse.ArgumentParser(description='Rolling Dice generator for RNA Sequences')
my_parser.version = '1.0'
my_parser.add_argument('-N', metavar='number of repeats', action='store', type=int, required=False, help='Specify number of repeats.')
my_parser.add_argument('filename', type=str, action='store', nargs='*', help='Specify input file.')
args = my_parser.parse_args()

repeats = args.N

### use filename argument. In case no filename was specified we can choose or input one - quick testing feature.

if args.filename!="": file=str(args.filename)[2:-2]
else:
    file=input("Type 1 for RollingDice-test30.in, 2 for RollingDice-test30.in, 3 for other input: ")
    if file=="1": file="RollingDice-test30.in"
    elif file=="2": file="RollingDice-test100.in"
    elif file=="3": file=input("Type file name: ")

fin = open(file, 'r')

content=""
for line in fin:
    content+=line

### Count the number of nuclides in a string, determine percent ranges and
### generate random output which is assigned a letter based on the previously determined ranges.

def nuc_count(string):
    U_count=string.count("U")
    U=U_count
    A_count=string.count("A")
    UA=U_count+A_count
    C_count=string.count("C")
    UAC=UA+C_count
    G_count=string.count("G")
    UACG=UAC+G_count
    return U_count, A_count, C_count, G_count

def ranges(UACG_count):
    U=UACG_count[0]
    UA=U+UACG_count[1]
    UAC=UA+UACG_count[2]
    UACG=UAC+UACG_count[3]
    return U, UA, UAC, UACG

def generate(input, UACG_ranges):
    new_string=""
    for i in range (0, len(input)-1):
        number=random.randint(1,(len(input)-1))  
        if number >= UACG_ranges[2]: new_string+="G"
        elif number>=UACG_ranges[1]: new_string+="C"
        elif number>=UACG_ranges[0]: new_string+="A"
        else: new_string+="U"
    return new_string

### Code is run, generation is repeated N number of times as specified in the command line arguments.

UACG_count=nuc_count(content)
UACG_ranges=ranges(UACG_count)
for i in range (0,repeats):
    new_string=generate(content, UACG_ranges)
    print (new_string)

### Quick statistic comparison of input and output:

# for testing the counts:
# print (content," --> \n",new_string,sep='')
# print ("U A C G\n",str(nuc_count(content))[1:-1],"\n", str(nuc_count(new_string))[1:-1], sep='')


