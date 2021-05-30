#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 05:34:27 2021

@author: lino
"""
import Lino_Boehler_A5
import argparse
from Lino_Boehler_A5.modules import A1
from Lino_Boehler_A5.modules import A2
from Lino_Boehler_A5.modules import A0
from Lino_Boehler_A5.modules import A3
from Lino_Boehler_A5.modules import k_let


#HelloWorld-test1.in
#Manhattan-testHV1.in
#WordCount-test1.in
#Administration-test1.in


parser = argparse.ArgumentParser(description="All tasks from A0-A4 in one package")
parser.add_argument("file", help="the path to the input file")
subparsers = parser.add_subparsers(title='Modules',
                                   description="Available Modules:",
                                   dest='subparser_name',
                                   help='exactly one has to be choosen from A0-A4:')

parser_A0=subparsers.add_parser("A0",help="Use A0, print: Hello World!")
parser_A0.set_defaults(func=A0.main)


parser_A1=subparsers.add_parser("A1",help="Use A1, word count")
parser_A1.add_argument("-l","--countlist",
                    help="shows list of different word counts",
                    action="store_true")
parser_A1.add_argument("-I","--Ignore_case",help="Ignore case sensitivity",action="store_true")
parser_A1.set_defaults(func=A1.main)


parser_A2=subparsers.add_parser("A2",help="Use A2, Administration Problem / branch and bound")
parser_A2.add_argument("-o","--optimize",
                    help="prints optimal solution, instead of  enumeration",
                    action="store_true")
parser_A2.set_defaults(func=A2.main)


parser_A3=subparsers.add_parser("A3",help="Use A3, the manhatten turist Problem / searching for the longest path ")
parser_A3.add_argument("-d", "--diagonal",
                    help="use this flage if the input file contains diagonal weights",
                         action="store_true")
parser_A3.add_argument("-t", "--path",
                    help="prints the best path if set true",
                    action="store_true")
parser_A3.set_defaults(func=A3.main)



parser_A4_klet=subparsers.add_parser("A4_klet",help="Use A4, k-let shuffeling")
parser_A4_klet.add_argument("-k","--klet",
                         help="k-let length")
parser_A4_klet.set_defaults(func=k_let.main)



parser_A4_dice=subparsers.add_parser("A4_dice",help="Use A4, dice roll")
parser_A4_dice.add_argument("-nr",
                         help="nr of strings")



parser_A4_mono=subparsers.add_parser("A4_mono",help="Use A4, mono shuffeling")







args = parser.parse_args()
args.func(args)
#parser_A3.set_defaults(func=A3.main(args))

#A1.main(args)


#print(args)
#Manhattan-testHV1.in
