#!/usr/bin/env python3

'''Script prints Hello World! and the content of a text file provided by command line'''
import sys


def main(args):
    print("Hello World!")

    try:
        file = open(sys.argv[1], "r")
        for line in file.readlines():
            print(line, end='')
        file.close()
    except Exception as e:
        print(e)
    sys.exit(0)


def add_args(parser):
    parser.add_argument("filename", help="Input text file")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    main(parser.parse_args())
    sys.exit(0)


