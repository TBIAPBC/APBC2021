# A0 Hello World Program written in python by Gabor Mate Erdo - 7 lines of code
# See the code for fulfilling the given requirements under the hash sections below

# accepts a single file name on the command line
# use [HelloWorld-test1.in](https://github.com/TBIAPBC/APBC2021/blob/master/A0/HelloWorld-test1.in) as input: 
# this needs to be added as argument in the command line.

import sys

filename = sys.argv[1]
with open(sys.argv[1], 'r') as my_file:
    inputcontent=(my_file.read())

# "Hello World!", adding a line break
# and the content of the file
# NO additional line break
# and prints (to standard output)
#  output should be like [HelloWorld-test1.out](https://github.com/TBIAPBC/APBC2021/blob/master/A0/HelloWorld-test1.out)

f = open("HelloWorld-test1.out", 'w')
f.write("Hello World!\n"+inputcontent)
f.close()
