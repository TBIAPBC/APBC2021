# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 18:12:01 2021

@author: Lino
"""
import sys
import itertools
import numpy as np
import collections
import argparse


# setting obligatory and optional comand line argumnents 
parser = argparse.ArgumentParser(description='')

parser.add_argument("file", help="the path to input file")
parser.add_argument("-o","--optimize",
                    help="prints optimal solution, instead of  enumeration",
                    action="store_true")

args = parser.parse_args()

## Assigning new names to input variables
path=args.file
opt_flag=args.optimize



#path="Administration-test1.in.txt"

with open(path) as f:
    data=f.readlines()

data=[i.rstrip() for i in data]
data=[i.split() for i in data]

data_info=data.pop(0)
col_names=data.pop(0)

data_df=np.array(data)
state_nr=int(data_info[0])
cost_max=int(data_info[1])

# generating all possibel capital paires
capital_combis=itertools.combinations(col_names,2)
capital_combis=list(capital_combis)


cost_dict=collections.defaultdict()
index=0
for i in range(0,len(col_names)):
    for j in range (i+1,len(col_names) ):
        
        cost_dict[capital_combis[index]]=int(data_df[i][j])
        
        index+=1


path_list=[]
city_list=col_names
curent_path=[]
best=int()



def branch_n_bound(state_nr,cost_dict,path_list,cost_max,city_list,col_names, opt_flag,curent_path,best):
    
    
    
    
    if len(city_list) > 0:
        city_a=city_list.pop(0)
        best=cost_max+1
    else:
        return
    city_l_copy=city_list.copy()
   
    result_list=[]
    curent_paths_list=[]
    
    for ind in range(len(city_l_copy)):
        
        city_b=city_list[ind]
        curent_pair = (city_a,city_b)
        
        
        if cost_dict[curent_pair] < cost_max:
            #city_l_copy.remove(city_b)
            #curent_cost=cost_dict[curent_pair]
            if len(curent_path) <= state_nr/2-1:
                
                copy_path=curent_path.copy()
                copy_path.append(curent_pair)
                
                if len(copy_path) == state_nr/2:
                    if opt_flag==True:
                        curent_cost=0
                        for i in  copy_path:
                            curent_cost+=cost_dict[i]
                        if curent_cost < best:
                            best = curent_cost
                            best_path=copy_path
                            path_list=[best,best_path]
                            print(best)
                            print(best_path)
                    curent_paths_list.append(copy_path)
                    
                    
                else:
                    
                    result_list=branch_n_bound(state_nr,cost_dict,path_list,cost_max,city_l_copy,col_names, opt_flag,copy_path,best)
            else:
                if len(curent_path) <= state_nr/2:
                    curent_paths_list.append(curent_path)
            
             
            
            
             
        else:
            continue
   
        
    if len(curent_paths_list) > 0:
       path_list.extend(curent_paths_list)
   
   
    return path_list
    

rs=branch_n_bound(state_nr,cost_dict,path_list,cost_max,city_list,col_names, opt_flag,curent_path,best)
 
    
