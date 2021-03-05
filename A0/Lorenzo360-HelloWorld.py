# Script prints Hello World! and the content of HelloWorld-test1.in
print("Hello World!")
try:
    file = open("HelloWorld-test1.in", "r")
    for line in file.readlines():
        print(line, end='')
    file.close()
except Exception as e:
    print(e)
