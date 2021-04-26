# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 10:23:38 2021

@author: Lino
"""
import sys 
import random 

in_file=sys.argv[1]

with open (in_file) as f:
    string=f.read()

string=string.rstrip()
string=list(string)

for i in range(len(string)+1,0,-1):
    j=random(0,len(string)+1)
    string[i],string[j] = string[j],string[i]
    