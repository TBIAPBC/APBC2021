This package contains the programs written for the course Algorithmen und Programmentwicklung für die biologische Chemie SS2021 by Markus Beicht. 
It contains 5 different modules with several options. 

Module -A0 HelloWorld: takes a string as input and prints "Hello World" followed by the input text. 

Module -A1 WordCount: takes a string as input and prints counts the number of total words and different words. 
Option -I: ignores upper/lower-case 
Option -l: prints a list of the words instead of only the counts

Module -A2 Administration: takes a distance matrix in a text file (example below) as input and groups the nodes in pairs. Prints all combinations of pairs which result in a overall cost <= the second value in the first line (10). 
Option -o: finds only the optimal solution of the problem instead of all possible solutions

8 10
 B  E  G  I  K  L  P  S
 - 10 10  2 10 10 10 10
10  -  2 10 10 10  1 10
10  2  - 10  2  3  3  3
 2 10 10  -  4 10 10  2
10 10  2  4  - 10 10  3
10 10  3 10 10  -  2  2
10  1  3 10 10  2  - 10
10 10  3  2  3  2 10  -


Module -A3 ManhattanTourist: solves the Manhattan Tourist problem. It takes 2 (3 for option -d) matrices representing the edge weights used for navigating a grid from top-left to bottom-right. Prints the length of the longest path. 
Option -d: takes 3 input matrices (vertical-horizontal-diagonal) as input and also considers diagonal moves. 
Option -t: prints the best path in addition to the best value 

#G_down: 4 5
  0.60   0.65   0.91   0.94   0.14
  0.85   0.27   0.70   0.31   0.63
  0.63   0.23   0.35   0.77   0.20
  0.37   0.76   0.41   0.30   0.67
#---
#G_right: 5 4
  0.76   0.41   0.72   0.13
  0.57   0.64   0.62   0.62
  0.37   0.98   0.36   0.24
  0.99   0.77   0.39   0.35
  0.37   0.34   0.62   0.82
#---
#G_diag: 4 4
  6.74   7.03   2.47   6.25
  4.48   3.75   2.98   3.62
  7.90   3.63   3.67   3.18
  9.30   8.40   9.02   2.58

Module -A4 Random Sequences: Contains 3 programs: RollingDice, MonoShuffle, KLetShuffle, which create randomized sequences based on an input sequence
RollingDice: Produces randomized sequences by randomly selecting letters with the same frequencey as the input sequence
MonoShuffle: Produces randomized sequences by swapping each position in the sequence with a random later position
KLetShuffle: Produces randomized sequences by creating Euler-paths with k-let length k to preserve k-let frequency 
Option -N: number of produced sequences 
Option -k (only for KLetShuffle): K-let length
