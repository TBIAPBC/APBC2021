#!/usr/bin/env python3
import sys
import fileinput


def usage():
    print("Usage: [-t prints out best path (default: false)] [-d accepts also diagnoals (default: false)]")


def exit_abnormal():
    print("Invalid argument input")
    usage()
    sys.exit(1)


class manhattan:
    def __init__(self, inputfile=[], diagonal=False, south_matrix=[], east_matrix=[], diag_matrix=[], path=[], trace=False):
        self.south_matrix = south_matrix  # contains the nort-south data
        self.east_matrix = east_matrix  # contains  the west-east data
        self.diag_matrix = diag_matrix  # contains  the diagonal data
        self.inputfile = inputfile
        self.diagonal = diagonal
        self.trace=trace
        self.res_dict = {(0, 0): [0, ""]}
        self.path=[]

    def print(self):
        print(self.res_dict)
        #print(self.diagonal)

    def print_result(self):
        print(round(self.res_dict[(len(self.south_matrix), len(self.east_matrix[0]))][0], ndigits=5))
        #path is stored reverse
        if self.path and self.trace:
            print("".join(self.path[::-1]))

    def read_data(self):

        # input data specifications:
        # comments must start with # at the beginning of the line.
        # manhattan must be quadratic
        # empty rows are accepted and ignored
        # First datapart must be north-south
        # second datapart must be west-east
        # third can be diagnoals

        try:
            counter = 0
            counter_diagonal = 0
            n = 0
            for line in fileinput.input(self.inputfile):
                if not (line.startswith("#") or len(line.split()) == 0):
                    current_split = line.split()
                    curren_line_length = len(current_split)
                    if counter == 0:  # if counter == 0 then the first line of the north-south part will be read
                        m = curren_line_length
                        counter = 1
                    if m == curren_line_length:
                        self.south_matrix.append([float(i) for i in current_split])
                        n = n + 1
                    if m != curren_line_length and counter == 1:
                        counter = 2

                    if counter == 2 and counter_diagonal <= m:
                        self.east_matrix.append([float(i) for i in current_split])
                        counter_diagonal = counter_diagonal + 1
                    if m < counter_diagonal and counter == 2 and self.diagonal:
                        counter = 3
                        #continue
                    if n < counter_diagonal and counter == 3:
                        self.diag_matrix.append([float(i) for i in current_split])
        except FileNotFoundError:
            print("File not found " + str(self.inputfile))
            exit_abnormal()

    def manhattanTourist(self):
        # n, m, sout and east
        n = len(self.south_matrix)
        m = len(self.east_matrix[0])
        for i in range(0, n):
            self.res_dict[(i + 1, 0)] = [self.res_dict[(i, 0)][0] + self.south_matrix[i][0], "S"]
        for i in range(0, m):
            self.res_dict[(0, i + 1)] = [self.res_dict[(0, i)][0] + self.east_matrix[0][i], "E"]

        if self.diagonal:
            for i in range(1, n + 1):
                for j in range(1, m + 1):
                    south=self.res_dict[(i - 1, j)][0] + self.south_matrix[i - 1][j]
                    east=self.res_dict[(i, j - 1)][0] + self.east_matrix[i][j - 1]
                    diag=self.res_dict[(i - 1, j - 1)][0] + self.diag_matrix[i - 1][j - 1]
                    if south >= east and south >= diag:
                        self.res_dict[(i, j)]=[south, "S"]
                    elif east >= diag:
                        self.res_dict[(i, j)]=[east, "E"]
                    else:
                        self.res_dict[(i, j)]=[diag, "D"]
        else:
            for i in range(1, n + 1):
                for j in range(1, m + 1):
                    south=self.res_dict[(i - 1, j)][0] + self.south_matrix[i - 1][j]
                    east=self.res_dict[(i, j - 1)][0] + self.east_matrix[i][j - 1]
                    if south >= east:
                        self.res_dict[(i, j)]=[south, "S"]
                    else:
                        self.res_dict[(i, j)]=[east, "E"]


    def backtracking(self):
        i=len(self.south_matrix)
        j=len(self.east_matrix[0])
        w=self.res_dict[(i, j)][1]
        while w:
            w=self.res_dict[(i, j)][1]
            if not w:
                break
            else:
                if w in "E":
                    j=j-1
                    self.path.append("E")
                if w in "S":
                    i=i-1
                    self.path.append("S")
                if w in "D":
                    i=i-1
                    j=j-1
                    self.path.append("D")



# if a word is separated to due a new line it is counted as two words.
# third argument must be the file
def main(argv):
    inputfile = argv[-1]
    argv = [a.lower() for a in argv]  # excepts iI and lL cases
    if not argv:
        exit_abnormal()
    trace = False
    diagonal = False
    arg = list(set(argv))  # removes duplicates
    for opt in argv:
        if opt == '-h':
            arg.remove("-h")
            usage()
            sys.exit()

        if opt in "-t":
            arg.remove("-t")
            trace = True

        if opt in "-d":
            arg.remove("-d")
            diagonal = True

    MH = manhattan(inputfile, diagonal=diagonal, trace=trace)
    MH.read_data()
    MH.manhattanTourist()
    MH.backtracking()
    MH.print_result()

    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:4])
    sys.exit()
