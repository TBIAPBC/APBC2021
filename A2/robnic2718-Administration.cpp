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
void read_file(int, char**, bool&, int&, int&, map<string, int>&, string&);

// START Branch and Bound algorithm
vector<string> branchNbound(string input_set, const map<string, int> &costMatrix, int costLimit_parameter,
                            bool optimize = false, int current_cost = 0, string current_path = "") 
{
  // If input data is empty, return empty set
  static size_t recursion_count{0};
  if(recursion_count == 0 && input_set.empty())
    return vector<string>{};
  recursion_count++;
  
  // Initialize static variables ("one-lifetime variables")
  static int costLimit{costLimit_parameter};
  static vector<string> solutions;
  
  // This approach follows the idea of a DEPTH-FIRST-SEARCH
  // --> branch until either the costLimit is not satisfied anymore or a child-node has been reached
  if(!input_set.empty())
  {
    int pair_cost;
    char root{input_set.at(0)};
    string children{input_set.erase(0, 1)}, children_copy;

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
  else
  { 
    // If all feasible results should be yielded, add feasible solution to solution list
    if(!optimize)
    {
      solutions.push_back(current_path);
      return vector<string>{};
    }
    // If only optimal solution required, update currently best solution
    if(current_cost < costLimit)
    {
      solutions = vector<string>{current_path};
      costLimit = current_cost;
      return vector<string>{};
    }
    // If there is more than one optimal solution, add it to solution list
    if(current_cost == costLimit)
    {
      solutions.push_back(current_path);
      return vector<string>{};
    }
  }
  return solutions;
}
// END

int main(int argc, char **args)
{

  // Variable declarations
  bool optimize{false};
  map<string, int> costMatrix;
  string capitals;
  int numCapitals, costLimit;
  vector<string> solutions;

  // Read in parameters and cost matrix
  read_file(argc, args, optimize, numCapitals, costLimit, costMatrix, capitals);

  // Call branch N bound function
  solutions = branchNbound(capitals, costMatrix, costLimit, optimize);
  
  for(auto& solution : solutions) 
  {
    for(int pos{0}; pos < numCapitals; pos += 2)
      cout << solution.substr(pos, 2) << " ";
    cout << '\n';
  }

  return 0;
}

// Concatenate two chars into a string
string concat_chars(size_t pos1, size_t pos2, const string &str) 
{
  string a{str.at(pos1)}, b{str.at(pos2)};
  return a + b;
} 

void read_file(int argc, char **args, bool &optimize, int &numCapitals,
               int &costLimit, map<string, int> &costMatrix, string &capitals)
{
  ifstream inputFile;
  bool file_exists{false};
  
  // START exceptions handling
  if (argc != 2 && argc != 3)
    throw runtime_error("Too few/many command-line arguments:\n- flag \'-o\' for optimization! (optional)\n- provide one input file! (compulsory)");

  for (char **arg{++args}; *arg != nullptr; arg++)
  {
    if (static_cast<string>(*arg) == "-o")
      optimize = true;

    if (__fs::filesystem::exists(static_cast<string>(*arg)))
    {
      inputFile.open(*arg);
      file_exists = true;
    }
  }
  if (!file_exists)
    throw runtime_error("No file found, please check file name!");
  // END

  // Variable declarations
  size_t lineCount{0};
  string line;
  bool first{true};

  while (getline(inputFile, line))
  {
    stringstream sstr;
    string strbuff{""};

    // START preprocessings
    lineCount++;
    // If in costMatrix: remove entries until including char '-'
    // to read in only entries in upper triangular part
    if (lineCount > 2)
    {
      size_t pos{0};
      for (; line.at(pos) != '-'; pos++);
      line.erase(0, pos + 1);
    }
    sstr << line;
    // END preprocessings

    // Read in capital number and cost limit
    if (lineCount == 1)
    {
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
    }
    // Read in capital names
    if (lineCount == 2)
    {
      while (!sstr.eof())
      {
        sstr >> strbuff;
        if (strbuff.size() != 1)
          throw runtime_error("This program only works for one character capital names!");
        capitals.push_back(strbuff.at(0));
      }
    }
    // Read upper triangular part of cost matrix into map
    if (lineCount > 2)
    {
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
  inputFile.close();
}