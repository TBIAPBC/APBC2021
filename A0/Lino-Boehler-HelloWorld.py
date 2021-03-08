# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 18:40:13 2021

@author: Lino Boehler
"""
import sys

input_file=sys.argv[1]

with open (input_file) as file:
   data = file.read()
   data=data.rstrip()

hello="Hello World!"
print(f"{hello}\n{data}")


