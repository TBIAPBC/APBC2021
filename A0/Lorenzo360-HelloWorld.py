# Script prints Hello World! and the content of a text file provided by command line
import sys

print("Hello World!")

if len(sys.argv) != 2:
    print("Please provide just one text file!")
    print("Aborting")
    sys.exit(1)
try:
    file = open(sys.argv[1], "r")
    for line in file.readlines():
        print(line, end='')
    file.close()
except Exception as e:
    print(e)
sys.exit(0)