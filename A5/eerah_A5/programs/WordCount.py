#!/usr/bin/env python3

import sys
import re
import fileinput


def usage():
    print("Usage: [-iI ignore case (default: false)] [-lL print words instead count (default: false)]")


def exit_abnormal():
    print("Invalid argument input")
    usage()
    sys.exit(1)


def split_file(inputfile, ignore_t):
    pat = "[\^\`\'\"\s'%^~!@#§()$%^&*_+-={[\]}}|,:;<>.?]+"
    words = []
    try:
        for line in fileinput.input(inputfile):
            zwisch = re.split(pat, line)
            if (zwisch[-1] == ''):
                zwisch.remove('')
            words = words + zwisch
            # if (zwisch == "None"):
            #    zwisch.remove("None")
        if ignore_t:
            return list(filter(None, [w.lower() for w in words])) #filter empty none values#
        else:
            return list(filter(None, words)) #filter empty none values#


    except FileNotFoundError:
        print("File not found " + str(inputfile))
        exit_abnormal()


def count_words(to_count, dict_words):
    for k, v in dict_words.items(): #key and value of dictionary
        for c in to_count:  # list of splitted words
            if c == k:
                v = v + 1

        dict_words[k] = v
            # and implement delete

    dict_words = dict(sorted(dict_words.items(), key=lambda x: x[0]))
    return sorted(dict_words.items(), key=lambda x: x[1], reverse=True)


# if a word is separated to due a new line it is counted as two words.
# third argument must be the file
def main(argv):
    inputfile = argv[-1]
    argv = [a.lower() for a in argv]  # excepts iI and lL cases
    if not argv:
        exit_abnormal()
    ignore_t = False
    word = False
    arg = list(set(argv))  # removes duplicates
    for opt in argv:
        if opt == '-h':
            arg.remove("-h")
            usage()
            sys.exit()

        if opt in "-i":
            arg.remove("-i")
            ignore_t = True

        if opt in "-l":
            arg.remove("-l")
            word = True


    words = split_file(inputfile, ignore_t)

    #if list is set true print words if not print counts
    dict_words = dict((zd, 0) for zd in list(set(words)))
    if word:
        [print(k, v) for k, v in count_words(words, dict_words)]
    else:
        print("{0} / {1}".format(len(dict_words), len(words)))

if __name__ == "__main__":
    main(sys.argv[1:4])
