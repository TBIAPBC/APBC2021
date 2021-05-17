#!/usr/bin/env python3 
import sys
import argparse 
import itertools as it

#parses command line arguments
def parse_args(parser):
    parser.add_argument("filename", help="Input text file")
    parser.add_argument("-o", action="store_true", help="If option -o is present, the program must optimize the cost instead of enumerating")
    
#prints optimization or enumeration deping on the command line input
def main(args):
    possible=input_to_prep(args.filename)
    
    if args.o:
        res = "" 
        opt = min(possible, key=possible.get)
        for j in opt:
            res = " ".join(opt[i:i+2] for i in range(0, len(opt), 2))
        print(res)

    else: 
        res = "" 
        for j in possible:
            for i in possible:
                res = " ".join([j[i:i+2] for i in range(0, len(j), 2)])
            print(res)

#reads input file into string, prepares it, turns it into dictionary, then eliminates options by evaluating costs of pairs and returns all possbile pair combinations
def input_to_prep(filename):
    file = open(filename, "r")
    text = ""
    for line in file.readlines():
        text += line    
    file.close()

    text = text.replace("  ", " ")
    text = text.replace("-", "0")
    lst = text.split("\n")

    new = []
    for l in lst:
        if (l[0] != " "):
            new.append(l[0:])
        else:
            new.append(l[1:])

    n = [list(word.split(" ")) for word in new]

    z = int(n[0][0])
    x = 2
    dic = {}
    for i in range(x, z+1):
        x += 1
        for j in range(x-2,z):
            a= n[1][i-2] + n[1][j]
            b= n[i][j]
            dic[a]=b

    c = list(it.combinations(dic.items(), int(z/2)))
    sums = []
    strgs = []
    
    z = int(n[0][0])
    for l in range(0, len(c)): 
        sum_ = 0
        new_str = ""
        for i in range(0, int(z/2)):
            sum_ += int((c[l][i][1]))
            new_str += str((c[l][i][0]))
        sums.append(sum_)
        strgs.append(new_str)

    st = []
    for s in strgs:
        st.append(''.join([j for i,j in enumerate(s) if j not in s[:i]]))

    final_s = []
    final_n = []
    dd = {}
    j = 0
    for i in st: 
        l = len(st[j]) 
        if l == z:
            final_s.append(st[j])
            final_n.append(sums[j])
            j += 1
        else:
            j+=1

    zip_it = zip(final_s, final_n)
    ddd = dict(zip_it)
    possible = {}
    pr = int(n[0][1])
    for i,j in ddd.items():
        if j <= pr:
            possible[i]=j
    return(possible)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Prints the possible combinations or the optimization to the terminal")
    parse_args(parser)
    main(parser.parse_args())        

sys.exit()
