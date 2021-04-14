import re
import sys
from plistlib import Data

# MANHATTAN TOURIST CODE

# ---PART 1: CHECK ARGUMENTS -------

help="-----\nUSAGE: python erdogabormate-manhattan.py -t -d filename.extension \n\n \
Where -t and -d are optional parameters, to be entered before the filename.\n \
-t types the actual path, not only the highest score\n -d also considers diagonal matrices.\n-----" 

param_T=0
param_D=0

if len(sys.argv)>4 or len(sys.argv) <2: 
    print(help)
    exit()

if len(sys.argv)==2: file=sys.argv[1]
elif len(sys.argv)==3: 
    file=sys.argv[2]
    if sys.argv[1]=="-t": param_T=1
    elif sys.argv[1]=="-d": param_D=1
elif len(sys.argv)==4: 
    file=sys.argv[3]
    if sys.argv[1]=="-t" and sys.argv[2]=="-d": 
        param_T=1
        param_D=1
    elif sys.argv[1]=="-d" and sys.argv[2]=="-t":
        param_T=1
        param_D=1
    else:
        print("\n-----\nERROR, invalid parameter - exiting.",help)
        exit()

# ---PART 2: EXTRACT DATA FROM FILE -------
# since the input files differ largely this part of the code was trickier than expected.
# Yet data can be read from all inputs including diagonal files. 

n=1
m=0
d=0
down_matrix=[]
right_matrix=[]
diagonal_matrix=[]

fin = open(file, 'r')
fout=open('output.txt', 'w')

for line in fin:
    if line[0]=="#" or len(line)<3: 
        continue
    if m<n:
        n=len([i for i in line.split()])-1
        down_matrix.append([i for i in line.split()])
        m+=1
        d+=1
        continue
    if param_D==1 and d>m+n:
        diagonal_matrix.append([i for i in line.split()])
        continue    
    if m>=n:
        right_matrix.append([i for i in line.split()])
        d+=1
        continue

# in case the order is not north-south followed by west-east the last entry of the down_list needs to be removed
# and inserted as first entry of the right matrix

if n<m:
    a=down_matrix.pop()
    right_matrix.insert(0,a)         
#print(n,m, down_matrix,"\n",right_matrix,"\n",diagonal_matrix)


# ---PART 3: MAIN CODE -------

def MANHATTANTOURIST(n, m, Down, Right, Diag):
    s=[[0 for x in range(m+1)]for y in range(n+1)]
    for i in range(1,n):
        s[i][0] = s[i-1][0] + float(Down[i-1][0])
    for j in range(1,m):
        s[0][j] = s[0][j-1]+ float(Right[0][j-1])
    if Diag!=[]:
        for i,j in range(n,m):
            s[i][j] = s[i-1][j-1] + float(Diag[i-1][j-1])
        for i in range(1,n+1):
            for j in range(1,m+1):
                s[i][j] = max(s[i - 1][j] + float(Down[i-1][j]), s[i][j - 1] + float(Right[i][j-1]), s[i-1][j-1] + float(Diag[i-1][j-1]))
    if Diag==[]:
        for i in range(1,n+1):
            for j in range(1,m+1):
                s[i][j] = max(s[i - 1][j] + float(Down[i-1][j]), s[i][j - 1] + float(Right[i][j-1]))
    #print(s)
    return s[n][m]

result="{:.2f}".format(MANHATTANTOURIST(n,m,down_matrix,right_matrix,diagonal_matrix))
if result[-2:]=="00":
    print(result[:-3])
else: 
    print(result)