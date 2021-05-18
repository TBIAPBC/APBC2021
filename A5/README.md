# APBC 2021
---------------------------------------------------------------------
270056 Algorithmen und Programmentwicklung für die Biologische Chemie
---------------------------------------------------------------------
(Algorithms and program development for biological chemistry) 

Usage eerah_A5 [-A* <parameters> ] [inputfile]




* Mar-03-2021 (A0 and A1) --- Word Count
  e.g eerah_A5 -A1 -l -i <inputfile>
    * [-l (list of words)]
    * [-I ignore case]
    * [inputfile]

* Mar-10-2021 (A2) --- Optimization
  e.g eerah_A5 -A2 -o <inputfile>
    * [-o  optimize the cost (instead of enumerating)]
    * [inputfile]
  
* Mar-24-2021 (A3) --- Dynamic programming
  e.g eerah_A5 -A3 -d <inputfile>
    * [-t trace  prints one optimal solution]
    * [-d use diagonal elements]
    * [inputfile]

* Apr-14-2021 (A4) --- Random Sequences
  e.g eerah_A5 -A4 -N 4 -K 3 KLetShuffle <inputfile>
    * [RollingDive, MonoShuffle, KLettShuffle]
    * [-N number of output sequences]
    * [-k for KLetShuffle - klet frequency]
    * [inputfile]
    

##A1
Write a program that reads in a text (file name given on the command
line) and counts the total number of words and the number of different
words. On request, the program should print a list of the words.

* If option -I (for 'Ignore') is given, case shall be ignored (by
  converting all upper case to lower case, see below).

* If option -l (for 'list') is present, the program must print a list
  of words instead only counts.  This list must be sorted by word
  frequency, starting with the most common words.  ( per line print
  one word and its frequency, separated by a tab symbol; in case of
  equal frequencies, the words must be sorted alphabetically.). Please
  have a look at the example inputs and outputs; your program should
  produce outputs in exactly the same format.
  
##A2
### Optimizing the administration of Atirasu

The government of the federal state Atirasu plans to modernize its administration by creating four new authorities for generally
unremarkable affairs.
These authorities shall be distributed to the capitals of eight
provinces such that each two provinces share one authority.
Consequently, the set of capitals

```
  {B,E,G,I,K,L,P,S}
```

shall be partitioned into four subsets of two elements each.

The cost of a partition is calculated as sum over the costs per
authority, where the cost per authority depends on the two assigned
cities and can be read from the following matrix (in million Euros /
year). For example, putting authority 1 in charge of the provinces
with capitals B and I costs 2 million Euros per year.

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

The federal government can provide 10 million Euros per year; it wants to
know all the possible combinations that don't exceed this cost limit.

The output lists like:

```
  BE GI KL SP
```

When given the flag -o, the program must optimize the cost (instead
of enumerating). The cost limit should be used as initial bound. As
result it print the score of the best solution.


##A3
###dynamic programming.
The Manhattan Tourist Problem:
------------------------------

The street network of Manhattan has the form of a grid. Our tourist values streets (from crossing to crossing) by the number of sights along them.

```
       start here
       |
       v
       +--3--+--3--+
       |     |     |
       1     6     2
       |     |     |
       +--3--+--2--+
       |     |     |
       4     0     7
       |     |     |
       +--5--+--7--+
                   ^
                   |
                  end here
```

The problem is to find a path from the top left to the bottom right corner of the grid with maximum weight. In each step, the tourist moves either to the east or to the south.

The program reads <inputfile> as followed:

```
     # size (north-south dimension times west-east dimension)
     # 3 3
     # north-south streets
     1 6 2
     4 0 7
     # west-east streets
     3 3
     3 2
     5 7
```


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

##A4
###Generating random sequences 

Create a random sequence based on either RollingDive, MonoShuffle or KLetShuffle  (k-mer
frequencies).

## Random sequences (preserving the frequencies of the single symbols):

### Rolling dice:

The program reads in a  sequence and determines the
frequencies of its symbols. Then, it generates N random sequences of
the same length, where symbols are drawn at random with the same
frequencies. 

Here is an example of input, frequencies and possible output
sequences.

```
      CUUUUGCUAG

          |
	  V
      
      A => 0.1             UGUACGCUGA
      C => 0.2    -----\   ACCUUCAUCU
      G => 0.2    -----/   UCUUCCUCCC
      U => 0.5             GUGCAUUUGU
```

### MonoShuffle:

The program reads in a sequence and generates random
sequences by randomly shuffling (i.e. swapping symbols of) the input
sequence.

e.g
For input of length n, perform exactly n-1 swaps like in this example
trace of an algorithm run:

```
      C <-+ G     G     G     G     G     G     G     G     G
      U   | U <-+ C     C     C     C     C     C     C     C
      U   | U   | U <-+ U     U     U     U     U     U     U
      U   | U   | U   | U <-+ C     C     C     C     C     C
      U   | U   | U <-+ U   | U <-+ G     G     G     G     G
      G <-+ C <-+ U     U   | G   | G <-+ A     A     A     A
      C     C     C     C <-+ U   | U   | U <-+ G     G     G
      U     U     U     U     U   | U   | U   | U <-+ U     U
      A     A     A     A     A   | A <-+ G <-+ U   | U <-+ U
      G     G     G     G     G <-+ U     U     U <-+ U <-+ U
```

Remark: this method produces permutations of the input, preserving the
frequencies of symbols in the input exactly; pay attention to produce
each possible permutation with the same probability. This method is
known as Fisher-Yates or Knuth shuffling.


## K-let-Shuffling (Shuffling preserving k-let frequencies)

The program reads in a sequence and generates random
sequences that preserve the k-let frequencies of the original
sequence. The _k-lets_ of a sequence s are its subsequences
s[i..i+k-1] of length $k$ (e.g. for dinucleotide frequencies, we
consider the 2-lets).

The k-let shuffling algorithm (for k>=2) works as follows

1. Determine all subsequences s[i..i+k-2] (of length k-1) of the
   input sequence s. 

2. These subsequences (the (k-1)-lets of s) form the vertices of
   a graph (which initially has no edges).

```
     CUUUUGCUAG               
                                
         | for k=2             
         V                      
                                
        A     U                  
                                
        
         
         G    C                    
```
                                
3. Run through the original sequence and insert an edge between
   each successive (k-1)-lets. Note that two (k-1)-lets could
   occur several times in direct succession; in this case, one
   must record an additional edge for each occurrence. (Thus, we
   construct a a _multi_-graph.)
     
```
	 CUUUUGCUAG                      +-----+
                                         |+---+|
             | for k=2                   ||+-+||
	     V                           ||| |||
	                                 vvv |||
	    A     U                  A<---U--+++
                             ->      |  / ^^	
	                             | /  ||	
				     vv   ||	
	     G    C                   G-->C     
```

4.  Each Euler-path in this multigraph corresponds to a shuffled
    version of the original sequence; this shuffled sequence
    preserves the k-let frequencies!  Recall: Euler-paths are
    paths that contain each edge of the graph exactly once (but
    can visit some vertices more than once.)

5.  The true art is to find a method that randomly selects
    Euler-paths, such that each Euler-path is selected with equal
    probability (meaning uniform distribution of shuffled
    sequences).

    The following two papers present solutions to this problem:

    1. Kandel D et al (1996) Shuffling biological sequences.
       Discrete Appl Math 71:171-185
       [doi:10.1016/S0166-218X(97)81456-4](https://doi.org/10.1016/S0166-218X(97)81456-4)
       
    2. Jiang M et al (2008) uShuffle: a useful tool for shuffling
       biological sequences while preserving the k-let counts.
       BMC Bioinformatics 9:192
       [doi:10.1186/1471-2105-9-192](https://doi.org/10.1186/1471-2105-9-192)
       
