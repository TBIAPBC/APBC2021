#!/usr/bin/env python3

import sys
import argparse

import MarkusBeicht_A5
from MarkusBeicht_A5.modules import HelloWorld, WordCount, Administration, Manhattan, RollingDice, MonoShuffle, KLetShuffle


def add_args(parser):
	parser.add_argument("filename", help="filename")

	parser.add_argument("-A0", action="store_true", help="Uses the Hello World module to print a 'Hello World' and the contents of the input file")

	parser.add_argument("-A1", action="store_true", help="Uses the Word Count module to count the total number of total words and different words")
	parser.add_argument("-I", action="store_true", help="WordCount option 'Ignore': case shall be ignored")
	parser.add_argument("-l", action="store_true", help="WordCount option 'list': prints a list of words, instead of only counts")

	parser.add_argument("-A2", action="store_true", help="Uses the Administration module to group capitals into pairs which fulfill the requirements")
	parser.add_argument("-o", action="store_true", help="Administration option 'optimize': optimises the cost instead of enumerating")

	parser.add_argument("-A3", action="store_true", help="Uses the Manhattan module to maximaize the path through a grid from top-left to bottom-right")
	parser.add_argument("-d", action = "store_true", help = "Manhattan option 'diagonal': processes input files with horizantal-vertical-diagonal input")
	parser.add_argument("-t", action = "store_true", help = "Manhattan option 'trace': prints the best path in addition to the maximized value")

	parser.add_argument("-A4", choices = ["D", "M", "K"], help="Uses one of the Random Sequences modules: rolling dice, mono shuffle or k-let shuffle, depending on the given choice")
	parser.add_argument("-N", type=int, help="Random sequence option: number of produced random sequences")
	parser.add_argument("-k", type=int, help="K-let shuffle option: length of k-lets")



def main():
	args = parser.parse_args()
	
	if args.A0:
		MarkusBeicht_A5.modules.HelloWorld.main(args)
	elif args.A1:
		MarkusBeicht_A5.modules.WordCount.main(args)
	elif args.A2:
		MarkusBeicht_A5.modules.Administration.main(args)
	elif args.A3:
		MarkusBeicht_A5.modules.Manhattan.main(args)
	
	elif args.A4 == "D":
		MarkusBeicht_A5.modules.RollingDice.main(args)
	elif args.A4 == "M":
		MarkusBeicht_A5.modules.MonoShuffle.main(args)
	elif args.A4 == "K":
		MarkusBeicht_A5.modules.KLetShuffle.main(args)
	
	else:
		print("Error: No module correct module was chosen")
		sys.exit()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MarkusBeicht_A5 Python package for the tasks in the course APBC2021")
    add_args(parser)
    main(parser.parse_args())
    sys.exit()
