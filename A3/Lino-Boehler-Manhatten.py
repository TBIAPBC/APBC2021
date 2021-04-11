# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 12:23:01 2021

@author: Lino Boehler
"""
import numpy as np
import argparse
from collections import deque

parser = argparse.ArgumentParser(description='')

parser.add_argument("file", help="pah to input file ")

parser.add_argument("-d", "--diagonal",
                    help="use this flage if the input file contains diagonal weights",
                         action="store_true")

parser.add_argument("-t", "--path",
                    help="prints the best path if set true",
                    action="store_true")

args = parser.parse_args()

path_file=args.file
diagonal=args.diagonal
best_path=args.path

list_south=[]
list_east=[]
list_weigths=[list_south,list_east]
if diagonal == True:
    list_diag=[]
    list_weigths.append(list_diag)
with open (path_file) as f:
   lines=f.readlines()
   counter=0
   ind=0
   n=0
   row_counter=0
   for l in lines:
        if l[:1] == "#" or l == "\n":
            #switch=1
            #print(f"line coment: {l}")
            #print(f"kk{ind}\n")
            continue
       
        else:
            l=l.rstrip()
            l=l.split()
            l=[float(i) for i in l]
            for i in l:
                if i < 1:
                    counter+=1
            #print(f"mat:{l}\tswitch:{switch}")
            
            if len(list_weigths[0])==0:
                n=len(l)
            
            if len(l)< n:
                ind=1
                row_counter+=1
                
                if row_counter > n:
                    if diagonal == True:
                        ind=2
                    else:
                        break
            #if ind-1 > len(list_weigths):
                #print(l)
                #break
            #print(f"mat:{l}\tindex:{ind}")
            #if switch == 1:
                #ind+=1
            #print(list_weigths)
            
            
                #print(f"n{n}")
                #if switch == 0:
                    #ind=1
        
            #print(f"ind: {ind}")
            #switch=0
            list_weigths[ind].append(l)
       
       
            
            
            
#print(list_weigths)


matrix = np.zeros(shape=(n,n),dtype=float)
def manhatten (list_weigths,diagonal,):
    #global matrix = np.ndarray(shape=(n,n),sdtype=float)
    nord_south=np.array(list_weigths[0])
    
    west_east=np.array(list_weigths[1]) 
    
    if diagonal == True :
        diagonal_weight=np.array(list_weigths[2])
    
    pos_matrix=np.empty(shape=(n,n),dtype=object)
    #print(pos_matrix)
    longest_path=deque([])
    
    for i in range(1,n):
        matrix[i,0]=nord_south[i-1,0]+matrix[i-1,0]
        pos_matrix[i,0]="S"
    
    for j in range (1,n):
        matrix[0,j]= west_east[0,j-1]+matrix[0,j-1]
        pos_matrix[0,j]="E"
        
    
        
    for i in range(1,n):
        
        for j in range(1,n):
            
            
            
            if matrix[i-1,j]+ nord_south[i-1,j] >= matrix[i,j-1]+ west_east[i,j-1]:
                if (i ==2) and (j == 2):
                    print(f"here 1!{i}{j}")
                if diagonal == True:
                    if  matrix[i-1,j-1] + diagonal_weight[i-1,j-1] > matrix[i-1,j] + nord_south[i-1,j] :
                        matrix[i,j]= matrix[i-1,j-1] + diagonal_weight[i-1,j-1]
                        pos_matrix[i,j]="D"
                    else:
                        matrix[i,j]= nord_south[i-1,j] + matrix[i-1,j]
                        pos_matrix[i,j]="S"
                
                else:
                    matrix[i,j]= nord_south[i-1,j] + matrix[i-1,j]
                    pos_matrix[i,j]="S"
                
                
            else:
                
                if diagonal == True:
                    if  matrix[i-1,j-1] + diagonal_weight[i-1,j-1] > matrix[i,j-1]+ west_east[i,j-1]:
                        matrix[i,j]= matrix[i-1,j-1] + diagonal_weight[i-1,j-1]
                        pos_matrix[i,j]="D"
                    else:
                        matrix[i,j]= matrix[i,j-1]+ west_east[i,j-1]
                        pos_matrix[i,j]="E"
                    
                else:
                    matrix[i,j]= matrix[i,j-1]+ west_east[i,j-1]
                    pos_matrix[i,j]="E"
               #print( pos_matrix[i,j])
    if best_path == True:
        i=n-1
        j=n-1
        while i or j !=0 :
            longest_path.appendleft(pos_matrix[i,j])
                            
            if pos_matrix[i,j] == "S":
                i-=1
            elif pos_matrix[i,j]== "E":
                j-=1
            else :
                i-=1
                j-=1
        print(f"the longest path is: {longest_path}")
    print(f"path length: {matrix[n-1,n-1]}")
    #print(matrix)
    return

        

    
manhatten(list_weigths,diagonal)