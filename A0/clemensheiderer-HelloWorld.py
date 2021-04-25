import sys
#cd C:/Users/User/PycharmProjects/manhatten
#python3 HelloWorld.py HelloWorld-test1.in


def read(thatandmore):
    with open(thatandmore, 'r') as f:
        for line in f:
            return line.strip()


text = read(sys.argv[1])
#

sys.stdout = open('HelloWorld-test1.out','wt')
da = "Hello World!\n" + str(text)
print(da)

