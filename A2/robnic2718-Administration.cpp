#include <iostream>
#include <vector>
#include <map>
#include <stdexcept>
#include <sstream>
#include <cstring>
#include <fstream>
#include <string>
#include <filesystem>
using namespace std;

// Forward declarations
string concat_chars(size_t, size_t, const string&);
ifstream parse_cmd_args(int, char**, bool&);
void read_subpart(const size_t, const string&, int&, map<string, int>&, string&);
void read_file(ifstream&, int&, map<string, int>&, string&);

// START Branch and Bound algorithm
vector<string> branchNbound(string input_set, const map<string, int> &costMatrix, int costLimit_parameter,
                            bool optimize = false, int current_cost = 0, string current_path = "") 
{ 
  /*
    Please note that the costMatrix is passed as a reference, so it is not being copied in each recurive call, but just the memory
    address is passed so that the current scope of a certain recursive call has access to the costMatrix.
  */
  
  // If input data is empty, return empty set
  // Keep track of recursion count
  static size_t recursion_count{0};
  if(recursion_count == 0 && input_set.empty())
    return vector<string>{};
  recursion_count++;
  
  // Initialize static variables ("one-lifetime variables", i.e. variables are only initialized once)
  static int costLimit{costLimit_parameter};
  static vector<string> solutions;
  
  // This approach follows the idea of a DEPTH-FIRST-SEARCH
  // --> branch until either the costLimit is not satisfied anymore or a child-node has been reached
  if(!input_set.empty())
  {
    // Variable declarations/initializations
    int pair_cost; 
    char root{input_set.at(0)}; // root is the first instance (capital) in the set of instances
    string children{input_set.erase(0, 1)}, children_copy; // children are all instances, except the root
    
    // For-loop pairs one node in the children_nodes_list with the root node at each iteration
      // Then we evaluate the cost of the pair and if the cost of this pair is (still) below the limit.
        // We make a recursive call of the branch and bound function, where
          // we pass the current_cost and the current_path in the tree.
            // This way we will make recursive calls as long as the costLimit is satisfied and as long as
              // there are nodes in the children_nodes list who still have to be explored.
    for(size_t pos{0}; pos < children.size(); pos++)
    {
      string pair{string{root} + string{children.at(pos)}};
      
      // Copy desired values from costMatrix, this is required, since the costMatrix is passed as a constant reference
      memcpy(&pair_cost, &costMatrix.find(pair)->second, sizeof(costMatrix.find(pair)->second));
      memcpy(&children_copy, &children, sizeof(children));

      children_copy.erase(pos, 1);
      int current_cost_update{current_cost + pair_cost};
      
      // If condition still satisfied: make recursive call
      if(current_cost_update <= costLimit)
        branchNbound(children_copy, costMatrix, costLimit, optimize, current_cost_update, current_path + pair);
    }
  }
  // This part of the code adds solutions to the list or in case that we reached a final solution and the
    // final solution does not satisfy the costLimit then this code makes sure to just return to the scope
      // of the previous recursive call, to continue the for-loop.
  else
  { 
    // If all feasible results should be yielded, add feasible solution to solution list
    if(!optimize)
    {
      solutions.push_back(current_path);
      return vector<string>{};
    }
    // If only optimal cost required, update currently best cost
    if(current_cost <= costLimit)
    {
      solutions = vector<string>{to_string(current_cost)};
      costLimit = current_cost;
      return vector<string>{};
    }
  }
  return solutions;
}
// END

// For those of you who not acquainted with C++, main is the function that automatically gets
  // called when you start a C++ program, i.e. it is the start of the program.
int main(int argc, char **args)
{

  // Variable declarations
  bool optimize{false};
  map<string, int> costMatrix;
  string capitals;
  int costLimit;
  vector<string> solutions;
  ifstream inputFile;

  // Parse command line arguments and read in file
  inputFile = parse_cmd_args(argc, args, optimize);
  read_file(inputFile, costLimit, costMatrix, capitals);

  // Call branch N bound function
  solutions = branchNbound(capitals, costMatrix, costLimit, optimize);
  
  // Print solutions, the branch and bound is implemented such that the lexicographical order is maintained
  if(!optimize) 
  {
    for(auto& solution : solutions) 
    {
      for(size_t pos{0}; pos < solution.size(); pos += 2)
        cout << solution.substr(pos, 2) << " ";
      cout << '\n';
    }
  } else cout << solutions.at(0) << endl;

  return 0;
}

// Concatenate two chars into a string
string concat_chars(size_t pos1, size_t pos2, const string &str) 
{
  string a{str.at(pos1)}, b{str.at(pos2)};
  return a + b;
} 

// Parse command line arguments and open file
ifstream parse_cmd_args(int argc, char** args, bool &optimize) 
{
  ifstream inputFile;
  bool file_exists{false};

  // Exceptions handling and args parsing
  if (argc != 2 && argc != 3)
    throw runtime_error("Too few/many command-line arguments:\n- flag \'-o\' for optimization! (optional)\n- provide one input file! (compulsory)");

  for (char **arg{++args}; *arg != nullptr; arg++)
  {
    if (static_cast<string>(*arg) == "-o")
      optimize = true;

    if (filesystem::exists(static_cast<string>(*arg)))
    {
      inputFile.open(*arg);
      file_exists = true;
    }
  }
  if (!file_exists)
    throw runtime_error("No file found, please check file name!");

  return inputFile;
}

// Removes substring of input_string until including char '-'
void dele_substr(string &line)
{
  size_t pos{0};
  for (; line.at(pos) != '-'; pos++);
  line.erase(0, pos + 1);
}

// This function reads in the data from the file using so-called streams.
  // Streams always read in the next word in a line string.
    // By iterating this process until the end of string has been reached, I can read in desired words/numbers.
      // I did not use a fancy built-in function, but implemented it on my own.
void read_file(ifstream &inputFile, int &costLimit, map<string, int> &costMatrix, string &capitals)
{
  // Variable declarations
  size_t lineCount{0};
  string line;

  while (getline(inputFile, line))
  { 
    // Increment line counter
    lineCount++;
    // Remove substring to only read in upper triangular part of costMatrix
    if(lineCount > 2) dele_substr(line);
    // Read line_string into stringstream
    // Check which part of the file we have and read it in
    read_subpart(lineCount, line, costLimit, costMatrix, capitals);
  }
  inputFile.close();
}

// Implement switch function
void read_subpart(const size_t lineCount, const string& line, int& costLimit, map<string, int>& costMatrix, string& capitals)
{ 
  static bool first{true};
  static int numCapitals;
  string strbuff{""};
  stringstream sstr;
  // Read line_string into stringstream
  sstr << line;

  switch(lineCount) 
  {
    // Read in capital number and cost limit
    case 1:
      while (!sstr.eof())
      {
        sstr >> strbuff;
        if (first)
        {
          numCapitals = stoi(strbuff);
          first = false;
        }
        if (!first)
          costLimit = stoi(strbuff);
      }
      break;
    
    // Read in capital names
    case 2:
      while (!sstr.eof())
      {
        sstr >> strbuff;
        if (strbuff.size() != 1)
          throw runtime_error("This program only works for one character capital names!");
        capitals.push_back(strbuff.at(0));
      }
      break;
    
    // Read upper triangular part of cost matrix into map
    default:
      size_t rowNum{lineCount - 3}, colNum{rowNum + 1};
      while (!sstr.eof())
      {
        sstr >> strbuff;
        if (rowNum == (size_t)numCapitals - 1)
          break;
        costMatrix[concat_chars(rowNum, colNum, capitals)] = stoi(strbuff);
        colNum++;
      }
  }
}