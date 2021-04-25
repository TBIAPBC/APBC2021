#python3 clemensheiderer-WordCount.py WordCount-test1.in -l -o
import argparse
import sys
import regex as re
#words = ['there', 'Are', 'FEW', 'words', 'so', 'this']

def Main():
    from contextlib import redirect_stdout

    output_to_file = True  # try changing this to True and comparing what happens
    parser = argparse.ArgumentParser()
    # group = parser.add_mutually_exclusive_group()
    parser.add_argument("-l", "--list", help="words", action="store_true")
    parser.add_argument("-I", "--ignore", help="output file", action="store_true")
    parser.add_argument("-o", "--output", help="output file", action="store_true")
    parser.add_argument('filename', help="first input is filename")

    args = parser.parse_args()
    # dew = each_word(words)

    with open(args.filename) as f:
        number_of_words = 0
        number_of_lower_words = 0
        string_without_line_breaks = ""
        for line in f:
            stripped_line = line.rstrip()

            string_without_line_breaks += stripped_line
            li = re.sub('[^A-Za-z0-9]+', ' ', string_without_line_breaks)

            words = li.split()

    #global words

    if args.ignore:
        #print(len(words))
        words_low = []

        for w in words:
            words_low.append(w.lower())

        words = words_low


    if args.list:
        def each_word(words):
            wcount = {}
            for w in words:
                w_low = w.lower()

                if w not in wcount:
                    wcount[w] = 1
                else:
                    wcount[w] += 1
            return wcount

        dew = each_word(words)

        dew_sorted = sorted(dew.items(), key=
        lambda kv: (-kv[1], kv[0]))

        for k, v in dew_sorted:
            print(f"{k} \t {v}")
        if args.output:
            if output_to_file:
                f = open("WordCount-test.out", "w")
            else:
                f = sys.stdout

            redirect_stdout(f)

            with redirect_stdout(f):
                for k, v in dew_sorted:
                    print(f"{k} \t {v}")


    if len(sys.argv) == 2:

        parser.print_help()
        print("\n")

        print(len(words))


        sys.exit(1)



    else:
        if args.output:
            if output_to_file:
                f = open("WordCount-test.out", "w")
            else:
                f = sys.stdout

            redirect_stdout(f)

            with redirect_stdout(f):
                print(len(words))


    #     print(len(words))



if __name__ == '__main__':
    Main()