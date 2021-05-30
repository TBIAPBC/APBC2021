# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 19:57:17 2021

@author: Lino
"""

import argparse
from random import sample



#k_length=2
"""
###################################### hard coded!!!!!!! ###########
file_in="KLetShuffle-test30_k2.in"

k_length=3

#########################!!!!!!
#"""




class Graph ():
    
    def __init__(self,graph_dict=None):
        if graph_dict == None :
            graph_dict = {}
        self.graph_dict = graph_dict
        self.path=[]    
    
    # constructing the graph
    def add_vertex(self,vertex):
        if vertex not in self.graph_dict:
            self.graph_dict[vertex]=[]
    
    def add_edge (self,edge):
        (vertex_1,vertex_2)= tuple(edge)
        if len(vertex_1) != len(vertex_2):
            return
        if vertex_1 not in self.graph_dict:
            self.graph_dict[vertex_1]=vertex_2
        else:
            self.graph_dict[vertex_1].append(vertex_2)
    
    #constructing string from path 
    def path_to_string(self):
        k1,path=self.path[0],self.path[1:]
        for i in path:
            k1+=i[-1]
        string="".join(k1)
        return string
    
    # doing the recursion and back tracking to find the path 
    
    def euler (self,vertex):
        neigh_bour=self.graph_dict[vertex]
        permuated_vertices=sample(neigh_bour,len(neigh_bour))
        
        if len(self.path) == 0:

            self.path.append(vertex)
       # print(f"curent node {vertex} ,{permuated_vertices} ")
        if len(permuated_vertices)!= 0:
            for random_v in permuated_vertices:
                    
                    #print(f"in loop: curent node {vertex},next{random_v} ,{permuated_vertices} ")
                    
                    if len(self.path) < len(seq):
                        neigh_bour.remove(random_v)
                    
                    self.path.append(random_v)
                                        
                    token=self.euler(random_v)
                    
                    if token == "$back":
                        
                        edge_back=list([vertex,self.path.pop()])
                        self.add_edge(edge_back)
                        #print(f"here next node {random_v},current:{vertex},reurn{edge_back}")
                    else:
                        if token == "$fin":                            
                           
                            
                            return "$fin"
                        else:
                            continue
            return "$back"
        else:
            if len(self.path) == len(seq)-(k_length-2):
                #print("fin!!!")
                return "$fin"
            else:
               # print("sackgasse")

                return "$back"
                
        return 

############################################################
## mainly used for diagnostic purposses, not used in alg ##
############################################################
    
    def edges (self):
        edges = []
        for v in self.graph_dict:
            for neighbour in self.graph_dict[v]:
                     edges.append((v, neighbour))
        return edges
    
    def print_dict (self):
        print(self.graph_dict)
    
    def vertices (self):
        return list(self.graph_dict.keys())
    
    def path_list(self):
        #print(self.path)
        return(self.path)
            

def main(args):
    file_in=args.file
    global k_length
    k_length= int(args.klet)
    
    global seq
    with open (file_in) as f:
        seq=f.read()
    seq=seq.rstrip()
    
    ##########################
    ### constructing graph ###
    ##########################
    
    
    
    obj=Graph()
    
    for i in range(len(seq)-1):
        k1_let=seq[i:i+k_length-1]
        #print(k1_let)
        k1_let_conseq=seq[i+1:i+k_length]
        obj.add_vertex(k1_let)
        edge=[k1_let,k1_let_conseq]
        obj.add_edge(edge)
    
    
    ########################################################
    ### calling graph class to generat the shuffeld string##
    ########################################################
    
    
    #for random start vertices / does probably not work 
    #start_v=sample(obj.vertices(),1)[0]
    #something=obj.euler(start_v)
    
    find_path=obj.euler(seq[0:k_length-1])
    
    #print(start_v)
    """
    print(obj.print_dict())
    print(obj.path_list())
    print(len(obj.path_list()))
    #"""
    
    shuffeld_string=obj.path_to_string()
    
    print(f"\n input sequence: \n\t{seq}\n\n the shuffeled sequence: \n\t{shuffeld_string}\n")
    
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("file", help="pah to input file ")
    
    parser.add_argument("-k","--klet",
                        type=int,
                        help="k-let length")
    args=parser.parse_args()
    main(args)
    

