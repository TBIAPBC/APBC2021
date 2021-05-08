#!/usr/bin/env python3
'''Prints the word counts for each word in the given text file.'''
import argparse
import re
import sys
from functools import cmp_to_key

def add_args(parser):
    parser.add_argument("filename", help="Input text file")
    parser.add_argument("-l", action='store_true', help="If option -l (for 'list') is present, the program must "
                                                        "print a list of words instead only counts.")
    parser.add_argument("-I", action='store_true', help="If option -I (for 'Ignore') is given, case shall be ignored "
                                                        "(by converting all upper case to lower case.")


def main(args):
    totalWordCount,uniqueWordCount, dictionary=TextFileToDictionary(args.filename,args.I)

    if args.l:
        dictionary={key: value for key, value in sorted(dictionary.items(),key=cmp_to_key(my_dictionary_compare))}
        for key, value in dictionary.items():
            print(key + "\t" + str(value))
    else:
        print(str(uniqueWordCount) + " / " + str(totalWordCount))

def my_dictionary_compare(item1,item2):
    "Compares dictionary entries first by value and if equal by key"
    if item2[1]-item1[1] == 0:
        if item1[0]<item2[0]:
            return -1
        else:
            return 1
    else:
        return item2[1]-item1[1]

def TextFileToDictionary(filename,caseinsensitive=False):
    """Reads to content of a textfile to a python dictionary
    Special characters will be ignored
    filename: Path to the text file
    caseinsensitive: if TRUE words will be put in lower case
    Returns (totalWordCount,uniqueWordCount,dictionary)
    """
    try:
        file = open(filename, "r")
        dictionary={}
        totalWordCount = 0
        uniqueWordCount=0
        for line in file.readlines():
            words=re.split("[^a-zA-ZäöüÄÖÜß]", line) #Splits line by any non alphabetical characters
            for word in words:
                if word != "":
                    if caseinsensitive:
                        word = word.lower()
                    if word in dictionary:
                        dictionary[word] = dictionary[word]+1
                        totalWordCount=totalWordCount+1
                    else:
                        dictionary[word] = 1
                        totalWordCount = totalWordCount + 1
                        uniqueWordCount=uniqueWordCount+1
        file.close()
        return totalWordCount,uniqueWordCount,dictionary
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser)
    main(parser.parse_args())
    sys.exit(0)

