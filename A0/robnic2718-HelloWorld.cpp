// please compile the src code using a C++ compiler to run it

#include<iostream>
#include<fstream>
#include<stdexcept>
using namespace std;

// argc = argument count on command-line including the program
// args = array of char pointers
int main(int argc, char **args) {

  if(argc != 2)
    throw runtime_error("\nPlease provide one input file.\n");

  // initialize instance of stream class (constructor opens file)
  ifstream input_file{*++args};
  // declare string variable
  string line;

  cout << "Hello World!\n";

  if(input_file.is_open())
    while(getline(input_file, line))
      cout << line << endl;

  input_file.close();

  return 0;
}
