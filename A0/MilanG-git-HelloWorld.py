#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

file = sys.argv[1]

with open(file, "r") as fh_file:
    content = fh_file.read()

output = "Hello World!\n" + content

outfile = "MilanG-git-HelloWorld.out"
with open(outfile, "w") as fh_out:
    fh_out.write(output)