#!/usr/bin/env python3
import sys
import argparse
import re
from functools import cmp_to_key as cmp

#parses parameters for the command line 
def parse_args(parser):
    parser.add_argument("filename", help="Input text file")
    parser.add_argument("-l", action='store_true', help="If option -l (for 'list') is present, the program must print a list of words instead only counts.")
    parser.add_argument("-I", action='store_true', help="If option -I (for 'Ignore') is given, case shall be ignored (by converting all upper case to lower case.")

#Function, which prints the WordCounts or the WordCounts and the list of words
def main(args):
    totalWordCount,uniqueWordCount, dic=TextFileToDictionary(args.filename,args.I)

    if args.l:
        dic={key: value for key, value in sorted(dic.items(),key=cmp(compare_words))}
        for key, value in dic.items():
            print(key + "\t" + str(value))
    else:
        print(str(uniqueWordCount) + " / " + str(totalWordCount))

#Compares words in dictionary by WordCount and then alphabetically
def compare_words(item1,item2):
    if item2[1] == item1[1]:
        if item1[0] < item2[0]:
            return -1
        else:
            return 1
    else:
        return item2[1]-item1[1]

#reads the input file to a string, replaces all special symbols with whitespaces and then splits the whitespace deliminated words 
def TextFileToDictionary(filename,Ignore=False):
    try:
        file=open(filename, "r")
        string=""
        dic={}
        totalWordCount=0
        uniqueWordCount=0
        for line in file.readlines():
            string+=line
        for char in """,.'";-!?:[]""":
            string=string.replace(char," ")
                
        words=string.split() 
        for word in words:
            if word != "":
                if Ignore:
                    word=word.lower()
                if word in dic:
                    dic[word]=dic[word] + 1
                    totalWordCount=totalWordCount + 1
                else:
                    dic[word]=1
                    totalWordCount=totalWordCount + 1
                    uniqueWordCount=uniqueWordCount+1
        file.close()
        return totalWordCount,uniqueWordCount,dic
    except Exception as e:
        print(e)
        sys.exit()

#checks whether the module is run directly and if so executes it 
if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Prints the word counts or word list to the terminal")
    parse_args(parser)
    main(parser.parse_args())
    sys.exit()
