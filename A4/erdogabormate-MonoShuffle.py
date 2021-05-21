#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14  13:47:09 2021
@author: erdogabormate
"""
import random
import re
import argparse

# filename and number of repeats are parsed from the input arguments. 

my_parser = argparse.ArgumentParser(description='MonoShuffle generator for RNA Sequences')
my_parser.version = '1.0'
my_parser.add_argument('-N', metavar='number of repeats', action='store', type=int, required=False, help='Specify number of repeats.')
my_parser.add_argument('filename', type=str, action='store', nargs='*', help='Specify input file.')
args = my_parser.parse_args()
repeats = args.N

### use filename argument. In case no filename was specified we can choose or input one - quick testing feature.

if len(args.filename)>1: file=str(args.filename)[2:-2]
else:
    file=input("Type 1 for MonoShuffle-test30.in.in, 2 for MonoShuffle-test100.in, 3 for other input: ")
    if file=="1": file="MonoShuffle-test30.in"
    elif file=="2": file="MonoShuffle-test100.in"
    elif file=="3": file=input("Type file name: ")

fin = open(file, 'r')

content=""
for line in fin:
    content+=line
list_of_strings=list(content)


# The program takes a list input and returns a list output, where two randomized positions (never equal) change place.

def MonoShuffle(input):
    new_string=""
    charpos1=random.randint(1,(len(input)-1))-1
    charpos2=charpos1
    while charpos2==charpos1:
        charpos2=random.randint(1,(len(input)-1))-1
    a,b=input[charpos1],input[charpos2]
    output=input   
    output[charpos1],output[charpos2]=b,a
    return output, charpos1, charpos2

inputstr=""
print(inputstr.join(list_of_strings))

class color:
    PURPLE = '\033[1;35;48m'
    CYAN = '\033[1;36;48m'
    END = '\033[1;37;0m'

# MonoShuffle is repeated as many times as specified in the arguments (at least one time). 
# The alternating places are marked with colors purple and cyan, and each repeat with silent mutations is marked with an asterisk.

for i in range (0,repeats):
    outputstr=""
    list_of_strings,a,b=MonoShuffle(list_of_strings)
    result=outputstr.join(list_of_strings).strip("\n")
    if result[a]==result[b]: Silent=" *"
    else: Silent=""
    if a<b: print(result[0:a]+color.PURPLE+result[a]+color.END+result[a+1:b]+color.CYAN+result[b]+color.END+result[b+1:]+Silent)
    else: print(result[0:b]+color.PURPLE+result[b]+color.END+result[b+1:a]+color.CYAN+result[a]+color.END+result[a+1:]+Silent)





