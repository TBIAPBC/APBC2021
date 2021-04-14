import re

"""
with open ("data.txt") as f:
    db = f.readlines()
linecount=0
capitals=[]
for line in db:
    if linecount==0:
        #line.split()
        for i in line:
             print(i,"\n")
        capitalcount=line[0]
        costlimit=line[1]
        continue
    if linecount==1: 
        line.split()
        for i in range (0, len(line)):
            capitals.append(line[i])    
    linecount+=1
    else: """
    
capitals=8
costlimit=10

# only data other than "10" and "-" is recorded and stored in a dictionary:
dict={"BI" : 2,"EG" : 2, "EP" : 1, "GE" : 2, "GK" : 2, "GL" : 3, "GP" : 3, "GS" : 3, "IB" : 2, "IK" : 4, "IS" : 2,  "KG" : 2, "KI" : 4, "KS" : 3, "LG" : 3, "LP" : 2, "LS" : 2, "PE" : 1, "PG" : 3, "PL" : 2, "SG" : 3, "SI" : 2, "SK" : 3, "SL" : 2}

# a list is filled with duplicates of cities and entries that come later in alph 

dellist=[]
for key, value in dict.items():
    print(key)
    for revkey, value in dict.items():
        if key[::-1]==revkey and key<revkey: dellist.append(revkey)

for entry in dellist:
    print(entry,"AAA")
    if entry in dict: 
        del dict[entry]
print(dict.keys())
print(dict.values())

alphabet = ["B", "E", "G", "I", "K", "L", "P", "S"]

# a list of best choices for each letter is generated.

bestlist=[]
for key, value in dict.items():
    bestvalue=5
    for letter in alphabet:
        if letter in key and value<bestvalue:
            bestvalue=value
            key_of_bestvalue=key
        else: continue
        bestlist.append([bestvalue, key_of_bestvalue, letter]) 

# "count options for letters where there are is only one option, and remove the complementary letter to narrow selection, from the rest pic the lowest possible"

def filter(bestlist):
    onlychoices=[]
    rounds=0
    savedrounds=[]
    letterstopurge=[]
    for i in bestlist:  
        count=0
        for j in bestlist: 
            if i[2] in j[1]: count+=1
            else: continue
        if count==1: 
            onlychoices.append((i[1], i[0]))
            print("Saving ",i[1]," because its the only entry containing ",i[2])
            letterstopurge.append(i[1].replace(i[2],""))
            print("Purging complementers containing ",str(letterstopurge)[2:-2])
            savedrounds.append(rounds)
    rounds+=1
    for entry in savedrounds:
        bestlist.pop(entry)
    should_restart = True
    while should_restart:
        should_restart = False
        for letter in letterstopurge:
            for k in bestlist:
                print("Examining leaf: ",k)
                if letter in k:
                    print("Trimming leaf ", k)
                    bestlist.remove(k)
                    should_restart=True
    return onlychoices, bestlist

# cleanup: all entries which contain unique city values are saved, and if there are any entries with the complementer letter left, are deleted, in order to ensure every city has an administration and is not left out. The iteration happens as long as there area such cities - with every removel of complementers the check is performed again and the list of best values is still stored under bestlist - with only 9 entries remaining, reducing the problem size:

fixedvalues=[]
start=0
end=1
while end>start:
    start=len(fixedvalues)
    a,b=filter(bestlist)
    if len(a)>0: fixedvalues.append(str(a))
    bestlist=b
    end=len(fixedvalues)
 
print (fixedvalues)    
print (bestlist)

#a,b=filter(bestlist)
#if len(a)>0: fixedvalues.append(a)
#bestlist=b
#
#print (fixedvalues)     
#print (bestlist)

for value in fixedvalues:
    v=re.sub("[^0-9]","",value)
    costlimit-=int(v)
print("Remaining spendings after filtering:", costlimit)

for letter in alphabet: 
    print(letter)
    if letter in str(fixedvalues): 
        alphabet.remove(letter)
print(alphabet)
for letter in alphabet:
    for letter2 in alphabet:
        if letter2!=letter: 

 
