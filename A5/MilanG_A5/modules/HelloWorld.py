#!/usr/bin/env python3
import argparse
import sys

def main(args):
    with open(args.filename, "r") as fh_file:
        content = fh_file.read()
        content = content.rstrip("\n")
        
    print(f"Hello World!\n{content}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hello World!")
    parser.add_argument("filename", help="filename")
    main(parser.parse_args())
    sys.exit(0)