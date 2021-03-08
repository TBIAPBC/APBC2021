#!/usr/bin/env python3
import sys
import argparse
import re


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


def main(args):
    wdict, unique, total = text_to_dict(args)
    
    if args.l:
        elem = [v[0] for v in sorted(wdict.items(), key =lambda kv: (-kv[1], kv[0]))]
        for i in elem:
            p = str(i) + "\t" + str(wdict[i])
            print(p)

    else:
        print(unique, "/", total)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count unique and total words in a text file.")
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)