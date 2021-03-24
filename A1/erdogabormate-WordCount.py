import sys
import os
import re
import collections

printlist=0
ignore=0
print (len(sys.argv))

# based on the command line arguments list printing, and ignoring of upper case characters,
# as well as the filename to process are determined. 

if len(sys.argv)==1:
    print("\n-----\nERROR: No filename defined!\nABORTING.\n-----")
    exit()
else:
    for i in range (len(sys.argv)):
        if sys.argv[i].lower()=="-l": printlist=1
        elif sys.argv[i].upper()=="-I": ignore=1
        else: filename=sys.argv[i]

def checkfile(filename):
    if os.path.isfile(filename):
        return True
    else: return False
if checkfile(filename)==False:
    print("\n-----\nERROR: File not found!\nMake sure to type in proper case, and without spaces.\nABORTING.\n-----")
    exit()
else: print("File found, opening.")

# FOR CODECHECKING: 
# print(printlist,"\n",ignore,"\n",filename)

with open (filename) as f:
    db = f.readlines()
word_list = []
word_count = {}
for line in db:
    line=re.sub("[^A-Za-z]"," ",line)
    line=line.split(" ")
    for i in range (0,len(line)-1):
        if ignore==1: 
            if len(line[i])>0: word_list.append(line[i].lower())
        else: 
            if len(line[i])>0: word_list.append(line[i])
word_list.sort()
print(word_list) 

def frequency_count(list):   
    freq = {} 
    for item in list: 
        freq[item]=freq.get(item,0) + 1
    return freq
        #if (item in freq): 
        #    freq[item] += 1
        #else: 
        #    freq[item] = 1
    #for key, value in freq.items(): 
        #print ("% d : % d"%(key, value))

freq_dict=frequency_count(word_list)
ordered_freq_dict=dict(sorted(freq_dict.items(), reverse=1, key = lambda item: item[1]))
print(ordered_freq_dict)

outputstring=""+str(len(freq_dict))+" / "+str(len(word_list))
print(outputstring) 
final_list=[]
if printlist==1:
    for key, value in ordered_freq_dict.items():
        entry=str(key)+"\t"+str(value)  
        final_list.append(str(entry))
final_list.sort()
for i in final_list:
    print(i)

#in case we wanted to write the results in a file, not only on the screen:
#outfilename=filename[:-2]+"out"
#f = open(outfilename, 'w')
#f.write(outputstring)
#f.close()



