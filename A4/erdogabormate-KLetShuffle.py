#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26  22:22:09 2021
@author: erdogabormate
"""

import time
import argparse

# filename and number of repeats as well as k-mer length are parsed from the input arguments 

my_parser = argparse.ArgumentParser(description='KLetShuffle generator for RNA Sequences')
my_parser.version = '1.0'
my_parser.add_argument('-N', metavar='number of repeats', action='store', type=int, required=False, help='Specify number of repeats.')
my_parser.add_argument('-k', metavar='k-mer length', action='store', type=int, required=True, help='Specify k length >=2')
my_parser.add_argument('filename', type=str, action='store', nargs='*', help='Specify input file.')
args = my_parser.parse_args()

repeats = args.N
k = args.k
### use filename argument. In case no filename was specified we can choose or input one - quick testing feature.

if args.filename!="": file=str(args.filename)[2:-2]
else:
    file=input("Type 1 for KLetShuffle-test30_k2.in, 2 for KLetShuffle-test100_k3.in, 3 for other input: ")
    if file=="1": file="KLetShuffle-test30_k2.in"
    elif file=="2": file="KLetShuffle-test100_k3.in"
    elif file=="3": file=input("Type file name: ")

fin = open(file, 'r')

content=""
for line in fin:
    content+=line.strip('\n')

string_sequence=content
k_mer_length=k

start1 = time.time()

def debruijnize(reads):
    nodes = set()
    not_starts = set()
    edges = []
    for r in reads:
        r1 = r[:-1]
        r2 = r[1:]
        nodes.add(r1)
        nodes.add(r2)
        edges.append((r1, r2))
        not_starts.add(r2)
    return (nodes, edges, list(nodes - not_starts))

def build_k_mer(str, k):
    return [str[i:k + i] for i in range(0, len(str) - k + 1)]

def make_node_edge_map(edges):
    node_edge_map = {}
    for e in edges:
        n = e[0]
        if n in node_edge_map:
            node_edge_map[n].append(e[1])
        else:
            node_edge_map[n] = [e[1]]
    return node_edge_map

def eulerian_trail(m, v):
    #print("Eulerian Trail: \n")
    nemap = m
    result_trail = []
    start = v
    result_trail.append(start)
    while (True):
        trail = []
        previous = start
        while (True):
            if (previous not in nemap):
                break
            next = nemap[previous].pop()
            if (len(nemap[previous]) == 0):
                nemap.pop(previous, None)
            trail.append(next)
            if (next == start):
                break;
            previous = next
        # completed one trail
        # print(trail)
        index = result_trail.index(start)
        result_trail = result_trail[0:index + 1] + trail + result_trail[index + 1:len(result_trail)]
        # choose new start
        if (len(nemap) == 0):
            break
        found_new_start = False
        for n in result_trail:
            if n in nemap:
                start = n
                found_new_start = True
                break  # from for loop
        if not found_new_start:
            print("error")
            print("result_trail", result_trail)
            print(nemap)
            break
    return result_trail

def assemble_trail(trail):
    if len(trail) == 0:
        return ""
    result = trail[0][:-1]
    for node in trail:
        result += node[-1]
    return result

def visualize_debruijn(G):
    nodes = G[0]
    edges = G[1]
    dot_str = 'digraph "DeBruijn graph" {\n '
    for node in nodes:
        dot_str += '    %s [label="%s"] ;\n' % (node, node)
    for src, dst in edges:
        dot_str += '    %s->%s;\n' % (src, dst)
    return dot_str + '}\n'

def test_assembly_debruijn(t, k):
    reads = build_k_mer(t, k)
    G = debruijnize(reads)
    v = visualize_debruijn(G)
    nemap = make_node_edge_map(G[1])
    #print(G)
    #print(v)
    start = next(iter(G[2])) if (len(G[2]) > 0) else next(iter(G[0]))
    trail = eulerian_trail(nemap, start)
    return assemble_trail(trail)

print(content)

for repeat in range (0, repeats):
    reads = build_k_mer(string_sequence, k_mer_length)
    G = debruijnize(reads)
    m = make_node_edge_map(G[1])
    # print(reads)
    # print(G)
    # print(m)
    start=string_sequence[0:k_mer_length-1]
    t = eulerian_trail(m, start)
    assemble_trail(t)
    string_sequence=test_assembly_debruijn(string_sequence, k_mer_length)
    print(string_sequence)

end = time.time()

runtime = ('Runtime: ' + str(end - start1)[0:10])

print(runtime)



