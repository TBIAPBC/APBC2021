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

# Data structure for storing multigraph info
class Vertex:
    def __init__(self, sym, neighbors=[], seen=False, next_=None):
        self.sym = sym
        self.neighbors = neighbors
        self.seen = seen
        self.next_ = next_
        self.number_in_sequ = 1

######
class KLetShuffle:
    # Initialize instance with existing multigraph or create it
    def __init__(self, sequence, k, print_frequencies):
        self.klet_size = k
        self.print_stats = print_frequencies
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
            km1Let.append(base)
        # Yield all k_lets
        for b in sequence:
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
            # Count number of times the k_let is present in the sequence
            # in order to determine the k_let frequency
            else:
                multigraph[sequ2id[km1_let]].number_in_sequ += 1
        # Add edges
        for pos in range(len(self.sequence)-km1):
            left_kletID = sequ2id[self.sequence[pos:pos+km1]]
            right_kletID = sequ2id[self.sequence[pos+1:pos+km1+1]]
            multigraph[left_kletID].neighbors.append(right_kletID)
        if(self.print_stats):
            self.klet_frequency()
        return multigraph
    
    # Print k_let frequencies with klet_sequence
    def klet_frequency(self, sequence=None, k=None):
        if k == None:
            k = self.klet_size
        if sequence == None:
            sequence = self.sequence
        count_dict = {}
        for km1_let in self.k_lets(sequence, k):
            if km1_let not in count_dict:
                count_dict[km1_let] = 1
                continue
            count_dict[km1_let] += 1
        total_num_klets = sum(count_dict.values())
        frequency_list = []
        for klet in count_dict:
        	  frequency_list.append((klet, round(count_dict[klet]/total_num_klets*100,2)))
        frequency_list.sort()
        for klet in frequency_list:
            print(klet[0]," : ",klet[1])
    
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
        stop_length = len(self.sequence)-self.klet_size+2
        next_one = False
        # The outer while-loop ensures that in case the wilson's algorithm
        # generates by chance (chance is low) a not connected spanning tree
        # then the random spanning tree is generated again to obtain a connected one
        while(len(base_IDs) != stop_length):
            if next_one:
                self.multigraph = deepcopy(self.multigraph_copy)
                self.random_spanning_tree()
                self.shuffle_neighbors()
                base_IDs = [0]
                curr_node = 0
            while(self.multigraph[curr_node].neighbors != []):
                base_IDs.append(self.multigraph[curr_node].neighbors[0])
                del self.multigraph[curr_node].neighbors[0]
                curr_node = base_IDs[-1]
            next_one = True
        # Turn base_IDs into bases
        new_sequence = self.multigraph[base_IDs[0]].sym
        first = True
        for i in base_IDs:
            if first:
                first=False
                continue
            new_sequence += self.multigraph[i].sym[-1]
        if(self.print_stats):
        	  print("\n")
        	  self.klet_frequency()
        self.multigraph = deepcopy(self.multigraph_copy)
        return "".join(new_sequence[::-1])
    
    # Produce steps required to obtain sequence for new uniform/random spanning tree
    def result(self, N):
        for i in range(N):
            self.random_spanning_tree()
            self.shuffle_neighbors()
            print(self.get_sequence())
######

def start(args):
    """Run program"""
    klet_instance = KLetShuffle(read_input(args.filename),args.k,args.stats)
    klet_instance.result(args.N)
    

if __name__ == "__main__":
    cmdl_parser=ap.ArgumentParser(description="Generate N random base-sequences and approx. preserve frequencies.")
    cmdl_parser.add_argument("filename", help="Specify name of input file.")
    cmdl_parser.add_argument("-k", required=True, type=int, help="Specify size of k-let.")
    cmdl_parser.add_argument("-N", required=True, type=int, help="Specify number of sequences to generate.")
    cmdl_parser.add_argument("--stats", action="store_true", help="Print klet frequency of original and newly generated sequences.")
    
    start(cmdl_parser.parse_args())
    sys.exit(0)
