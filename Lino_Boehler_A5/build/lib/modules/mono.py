# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 10:23:38 2021

@author: Lino
"""
import argparse
import random 

#in_file=sys.argv[1]

def main(args):
    in_file=args.file
    with open (in_file) as f:
        string=f.read()
    
    string=string.rstrip()
    string=list(string)
    
    for i in range(len(string)+1,0,-1):
        j=random(0,len(string)+1)
        string[i],string[j] = string[j],string[i]



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("file", help="pah to input file ")
    args=parser.parse_args()
    main(args)