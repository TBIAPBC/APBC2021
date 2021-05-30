#!/usr/bin/env python3
"""
Created on Sun Mar  7 22:18:11 2021

@author: Lino
"""
import re
import collections



## the word counting function 
def count_words(data,Ignore,show_list):

    counter_dict=collections.Counter()
    total_count=0
    
    ## spliting the lines into words, containg letters only
    for line in data:
        line=line.rstrip()
        split_list=re.split("[^a-zA-ZäöüÄÖÜß]",line)

        for word in split_list:
            if len(word) > 0:
              #the ignore case is currently in the for loop - I would be better to put it out - this way the if check is computetd allways -> a bit slower
              #total_count can be ommited by len(split_list)
                if Ignore == True:
                    word=word.lower()
                total_count+=1
                counter_dict[word]+=1
                
    unique=len(counter_dict)
    
    if show_list == True:
        for word in counter_dict:
            print(f"{word}\t{counter_dict[word]}\n")
    else:
        print(f"{unique}/{total_count}")
    return


def main(args):
    ## Assigning new names to input variables
    input_file=args.file 
    Ignore=args.Ignore_case
    show_list=args.countlist
    
    with open (input_file) as file:
        data = file.readlines()
        
    count_words(data,Ignore,show_list)





if __name__ == "__main__":
    import argparse

    # setting obligatory and optional comand line argumnents 
    parser = argparse.ArgumentParser(description='word count in input file uniqe/total word count')
    
    parser.add_argument("file", help="the path to input file")
    parser.add_argument("-l","--countlist",
                        help="shows list of different word counts",
                        action="store_true")
    parser.add_argument("-I","--Ignore_case",help="Ignore case sensitivity",action="store_true")
    args = parser.parse_args()
    main(args)