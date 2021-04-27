# coding: utf-8

import sys
import argparse as ap
import random as rd
from copy import deepcopy

# Read in sequence
def read_input(filename):
    try:
        with open(filename, 'r') as file:
            sequence=""
            for line in file.readlines():
                sequence+=line.strip()
            return sequence
    except(FileNotFoundError):
        print("Input file required. Please provide or check filename.")
        sys.exit(0)

# Check sequence validity
def check_warn(base):
    if base not in ['A','G','T','C','U']:
        print("Invalid base encountered. Program stopped!")
        print("Error -->", str(pos+1) + ". position in sequence")
        sys.exit(0)

# Data structure for storing multigraph info
class Vertex:
    def __init__(self, sym, neighbors=[], seen=False, next_=None):
        self.sym = sym
        self.neighbors = neighbors
        self.seen = seen
        self.next_ = next_

######
class KLetShuffle:
    # Initialize instance with existing multigraph or create it
    def __init__(self, sequence, k):
        self.sequence = sequence
        self.multigraph = self.build_graph(k-1)
        self.multigraph_copy = deepcopy(self.multigraph)
    
    # Generate all k_lets for sequence
    def k_lets(self, sequence, km1):
        if km1 < 1:
            print("Program stopped. Size of k_let needs to be ≥ 2!")
            sys.exit(0)
        sequence = iter(sequence)
        km1Let = []
        # Initialize process with first k_let
        for i in range(km1-1):
            try:
                base = next(sequence)
            except:
                return
            check_warn(base)
            km1Let.append(base)
        # Yield all k_lets
        for b in sequence:
            check_warn(b)
            km1Let.append(b)
            yield "".join(km1Let)
            del km1Let[0]
    
    # Create multigraph
    def build_graph(self, km1):
        multigraph = {}
        sequ2id = {}
        id_ = 0
        # Add vertices
        for km1_let in self.k_lets(self.sequence, km1):
            if km1_let not in [V.sym for V in multigraph.values()]:
                sequ2id[km1_let] = id_
                multigraph[id_] = deepcopy(Vertex(km1_let))
                id_ += 1
        # Add edges
        for pos in range(len(self.sequence)-2*km1+1):
            left_kletID = sequ2id[self.sequence[pos:pos+km1]]
            right_kletID = sequ2id[self.sequence[pos+km1:pos+km1*2]]
            multigraph[left_kletID].neighbors.append(right_kletID)
        return multigraph
    
    # Create and store random spanning tree in Vertex.next
    # according to WILSON's algorithm
    def random_spanning_tree(self):
        numNodes = len(self.multigraph)
        for i in range(numNodes):
            self.multigraph[i].seen=False
        self.multigraph[numNodes-1].seen=True
        for i in range(numNodes):
            u = i
            while not self.multigraph[u].seen:
                self.multigraph[u].next_ = rd.choices(self.multigraph[u].neighbors)[0]
                u = self.multigraph[u].next_
            u = i
            while not self.multigraph[u].seen:
                self.multigraph[u].seen = True
                u = self.multigraph[u].next_
    
    # Shuffle neighbor list and ensure that next is the last entry
    def shuffle_neighbors(self):
        for node in self.multigraph.values():
            if node == self.multigraph[len(self.multigraph)-1]:
                break
            for i in range(len(node.neighbors)):
                if node.neighbors[i] == node.next_:
                    del node.neighbors[i]
                    break
            rd.shuffle(node.neighbors)
            node.neighbors.append(node.next_)
    
    # Get sequence based on current uniformly&randomly generated spanning tree
    def get_sequence(self):
        curr_node = 0
        base_IDs = [0]
        # Run through nodes and neighbour lists
        while(self.multigraph[curr_node].neighbors != []):
            base_IDs.append(self.multigraph[curr_node].neighbors[0])
            del self.multigraph[curr_node].neighbors[0]
            curr_node = base_IDs[-1]
        # Turn base_IDs into bases
        new_sequence = ""
        for i in base_IDs[::-1]:
            new_sequence += self.multigraph[i].sym
        return "".join(new_sequence)
    
    # Produce steps required to obtain sequence for new uniform/random spanning tree
    def result(self):
        self.random_spanning_tree()
        self.shuffle_neighbors()
        print(self.get_sequence())
######

def start(args):
    """Run program"""
    for i in range(args.N):
        klet_instance = KLetShuffle(read_input(args.filename),args.k)
        klet_instance.result()


if __name__ == "__main__":
    cmdl_parser=ap.ArgumentParser(description="Generate N random base-sequences and approx. preserve frequencies.")
    cmdl_parser.add_argument("filename", help="Specify name of input file.")
    cmdl_parser.add_argument("-k", required=True, type=int, help="Specify size of k-let.")
    cmdl_parser.add_argument("-N", required=True, type=int, help="Specify number of sequences to generate.")
    
    start(cmdl_parser.parse_args())
    sys.exit(0)