#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 10:16:32 2021

@author: milan
"""

import argparse
import sys
import MilanG_A5
from MilanG_A5.modules import HelloWorld
from MilanG_A5.modules import WordCount
from MilanG_A5.modules import Administration
from MilanG_A5.modules import Manhattan
from MilanG_A5.modules import RollingDice, MonoShuffle, KLetShuffle

def main():
    """Distribution of the given commands to the single modules."""
    
    parser = argparse.ArgumentParser(description="MilanG-git_A5 package for assignments A0-A4.")
    parser.add_argument("filename", help="filename")
    
    parser.add_argument("-A0", action="store_true", help="Use the Hello World module.")
    
    parser.add_argument("-A1", action="store_true", help="Use the Word Count module.")
    parser.add_argument("-I", action="store_true", help="WordCount option: count words in case ignore mode.")
    parser.add_argument("-l", action="store_true", help="WordCount option: print a list of counted words, instead of pure counts.")
    
    parser.add_argument("-A2", action="store_true", help="Use the Administration module to optimise costs.")
    parser.add_argument("-o", action="store_true", help="Administration option: Optimises the cost and prints the best solution.")
    
    parser.add_argument("-A3", action="store_true", help="Use the Manhattan module to find the best path through a weighted matrix.")
    parser.add_argument("-d", action = "store_true", help = "Manhattan option: Include diagonal_matrix paths.")
    parser.add_argument("-t", action = "store_true", help = "Manhattan option: Print the path from start to finish")
    
    parser.add_argument("-A4",
                        choices = ["dice", "mono", "klet"], 
                        help="Use the Random sequence module to shuffle sequences. Three methods are available: 1. rolling dice, 2. mono shuffle, 3. k-let shuffle.")
    
    parser.add_argument("-N", type=int, default=1, help="Random sequence option: Number of random sequences printed. Default=1")
    parser.add_argument("--verbose", action="store_true", help="Random sequence option: Print verbose output")
    parser.add_argument("-k", type=int, default=2, help="Random sequence, k-let shuffle option: Length of k-lets. Default=2")
    
    args = parser.parse_args()
    
    if args.A0:
        if args.I or args.l or args.o or args.d or args.t or args.N != 1 or args.k !=2 or args.verbose:
            print("Options selected not intended for the selected module Hello World. Continuing.")
        MilanG_A5.modules.HelloWorld.main(args)
    
    elif args.A1:
        if args.o or args.d or args.d or args.t or args.N != 1 or args.k !=2 or args.verbose:
            print("Options selected not intended for the selected module Word Count. Continuing.")
        MilanG_A5.modules.WordCount.main(args)
        
    elif args.A2:
        if args.I or args.l or args.d or args.d or args.t or args.N != 1 or args.k !=2 or args.verbose:
            print("Options selected not intended for the selected module Manhattan. Continuing.")
        MilanG_A5.modules.Administration.main(args)
    
    elif args.A3:
        if args.I or args.l or args.o or args.d or args.N != 1 or args.k !=2 or args.verbose:
            print("Options selected not intended for the selected module Manhattan. Continuing.")
        MilanG_A5.modules.Manhattan.main(args)
        
    elif args.A4 == "dice":
        if args.I or args.l or args.o or args.d or args.t or args.k !=2:
            print("Options selected not intended for the selected module Random Sequences, Rolling Dice. Continuing.")
        MilanG_A5.modules.RollingDice.main(args)
    
    elif args.A4 == "mono":
        if args.I or args.l or args.o or args.d or args.t or args.k !=2:
            print("Options selected not intended for the selected module Random Sequences, Mono Shuffle. Continuing.")
        MilanG_A5.modules.MonoShuffle.main(args)
    
    elif args.A4 == "klet":
        if args.I or args.l or args.o or args.d or args.t:
            print("Options selected not intended for the selected module Random Sequences, K-Let Shuffling. Continuing.")
        MilanG_A5.modules.KLetShuffle.main(args)
        
    else:
        print("Error: No module has been selected!", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)