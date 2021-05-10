# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 20:30:46 2021

@author: Lino Boehler
"""
import sys
from collections import Counter
from numpy import random as rd


in_file=sys.argv[1]
Nr_strg=int(sys.argv[2])

main(args):
	Nr_strg=args.Nstr
	in_file=args.file
	
	with open (in_file) as f:
		  string=f.read()

	string=string.rstrip()

	string=list(string)
	char_set=frozenset(string)
	char_set=list(char_set)
	char_count=Counter(string)

	char_prob=[]
	for i in char_set:
		  char_count[i]= char_count[i]/len(string)
		  char_prob.append(char_count[i])

	new_strings=rd.choice(char_set, (Nr_strg,len(string)), p=char_prob)
	return
	
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("file", help="pah to input file ")
    
    parser.add_argument("-nr","--Nstr",
                        help="number of strings")
    args=parser.parse_args()
    main(args)
