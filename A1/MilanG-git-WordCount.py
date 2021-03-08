#!/usr/bin/env python3
import sys
import argparse
import re
from functools import cmp_to_key

#define commandline arguments
def add_args(parser):
    parser.add_argument("filename", help="Input text file")
    parser.add_argument("-I", action = "store_true", help="If option -I (for 'Ignore') is given, case shall be ignored.")
    parser.add_argument("-l", action = "store_true", help="If option -l (for 'list') is present, the program prints a list of words instead of only counts.")

#store text in dictonary, count total and unique words
def text_to_dict(args):
    wdict = {}
    totalcount = 0
    uniquecount = 0
    
    with open(args.filename, "r") as fh_file:
        content = fh_file.read()
    
    words = re.split("[^a-zA-ZäöüÄÖÜß]", content)
    
    for w in words:
        if w != "":
            #count case insensitive:
            if args.I:
                w = w.lower()
            if w not in wdict:
                wdict[w] = 1
                uniquecount +=1
                totalcount +=1
            else:
                wdict[w] +=1
                totalcount +=1
    
    fh_file.close()
    
    return wdict, uniquecount, totalcount

#Compare two entries of the dictionary, first by word count then alphabetically
def compare(item1, item2):
    if item1[1] == item2[1]:
        if item1[0] < item2[0]:
            return -1
        else:
            return 1
    else:
        return item2[1]-item1[1]


def main(args):
    wdict, unique, total = text_to_dict(args)
    
    if args.l:
        wdict ={key: value for key, value in sorted(wdict.items(), key = cmp_to_key(compare))}
        for key, value in wdict.items():
            p = str(key) + "\t" + str(value)
            print(p)
    else:
        print(unique, "/", total)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count unique and total words in a text file.")
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)