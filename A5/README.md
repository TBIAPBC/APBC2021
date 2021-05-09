#Collection of assignments for APBC2021 as a single package

Usage:
$ MilanG-Git_A5 [options] [filename]

Options:
  -h, --help            show this help message and exit
  -A0                   Use the Hello World module.
  -A1                   Use the Word Count module.
  -I                    WordCount option: count words in case ignore mode.
  -l                    WordCount option: print a list of counted words, instead of pure counts.
  -A2                   Use the Administration module to optimise costs.
  -o                    Administration option: Optimises the cost and prints the best solution.
  -A3                   Use the Manhattan module to find the best path through a weighted matrix.
  -d                    Manhattan option: Include diagonal_matrix paths.
  -t                    Manhattan option: Print the path from start to finish
  -A4 {dice,mono,klet}  Use the Random sequence module to shuffle sequences. Three methods are available: 1. rolling dice, 2. mono shuffle, 3. k-let shuffle.
  -N N                  Random sequence option: Number of random sequences printed. Default=1
  --verbose             Random sequence option: Print verbose output
  -k K                  Random sequence, k-let shuffle option: Length of k-lets. Default=2

Modules:
-A0 HelloWorld:
Will take a text file and print "Hello World!" and the contents of the file in the next line to screen.

-A1 WordCount:
Counts the words in a text file and prints "<unique words> / <total wordcount>" to screen.
The count can be case insensitive with -I. And the sorted list of words can be printed with -l.

-A2 Administration:
Needs a file containing the number of capitals and the maximum cost in the first line, aswell as a matrix containing the cost of pairs.
With -o flag only the best combination will be printe with the corresponding score.
Example input:
```
  8 10                     # number of capitals; cost limit
   B  E  G  I  K  L  P  S  # names of capitals
   - 10 10  2 10 10 10 10  # symmetric cost matrix
  10  -  2 10 10 10  1 10
  10  2  - 10  2  3  3  3
   2 10 10  -  4 10 10  2
  10 10  2  4  - 10 10  3
  10 10  3 10 10  -  2  2
  10  1  3 10 10  2  - 10
  10 10  3  2  3  2 10  -
```

-A3 Manhattan:
Calculates the best (highest pointed) path through a matrix.
-d will include diagonal weights in the calculation
-t will calculate the path through the grid.
Example input:
```
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
#---
```

-A4 Random Sequences:
Will take sequences and return -N N random sequencs.
Three methods are available:
    -Rolling dice:
    Calculates the frequencies of letters (nucleotides) in a sequence and randomly generates new sequences with the same frequencies as the input sequenc.
    -Mono shuffle:
    Iterates through the sequence and swaps each letter with a randomly chosen one later in the sequence.
    -K-let shuffle:
    Shuffles k-lets of a given length (-k K) to generate random sequences, preserving the k-let composition.
