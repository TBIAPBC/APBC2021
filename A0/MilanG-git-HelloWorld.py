#!/usr/bin/env python3

import sys

file = sys.argv[1]

with open(file, "r") as fh_file:
    content = fh_file.read()

output = "Hello World!\n" + content

print(output)