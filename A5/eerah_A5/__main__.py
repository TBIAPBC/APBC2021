#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  18 2021
@author: philippf
"""

import sys
import argparse
from eerah_A5.programs import RollingDice, WordCount, Administration, Manhattan, MonoShuffle, KLetShuffle

def main():
    parser = argparse.ArgumentParser(description="eerah_A5 APBC2021 - Assignment A1, A2, A3, A4.")
    parser.add_argument("inputfile", help="inputfile")
    parser.add_argument("-A1", action='store_true', help="Word Count of a given file")
    parser.add_argument("-i", action='store_true')
    parser.add_argument("-l", action='store_true')

    parser.add_argument("-A2", action="store_true", help="Optimizing the administration of Atirasu")
    parser.add_argument("-o", action="store_true",
                        help="if given: the program optimizes the cost (instead of enumerating)")

    parser.add_argument("-A3", action="store_true", help="The Manhattan Tourist Problem")
    parser.add_argument("-d", action="store_true", default=False, help="accepts also diagnoals (default: false)")
    parser.add_argument("-t", action="store_true", default=False, help="prints out best path (default: false)")

    parser.add_argument("-A4", choices=["RollingDice", "MonoShuffle", "KletShuffle"],
                        help="Shuffle a given sequenve based on choices")

    parser.add_argument("-N", type=int, default=1, help="Number of random sequences")
    parser.add_argument("-K", type=int, default=2, help="size of klet klet (2) ")

    argv = parser.parse_args()
    if argv.A1:
        WordCount.main(sys.argv[1:5])
    elif argv.A2:
        Administration.main(sys.argv[1:4])
    elif argv.A3:
        Manhattan.main(sys.argv[1:5])
    elif argv.A4:
        if argv.A4 == "RollingDice":
            RollingDice.main(argv)
        if argv.A4 == "MonoShuffle":
            MonoShuffle.main(argv)
        if argv.A4 == "KletShuffle":
            KLetShuffle.main(argv)


if __name__ == '__main__':
    main()
    sys.exit(0)
