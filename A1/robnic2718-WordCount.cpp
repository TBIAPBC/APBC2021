#include<iostream>
#include<stdexcept>
#include<unordered_map>
#include<fstream>
#include<cctype>
#include<vector>
using namespace std;

// define public class for later use
struct Pair {
  string word;
  int count;
};

// define sorting function (bubble sort algorithm) for later sorting of word counts
void bubble_sort(vector<Pair>& vector) {
  bool sorted{false};

  while(!sorted) {
    sorted = true;
    for(size_t pos{0}; pos < vector.size()-1; pos++)
        if(vector.at(pos).count < vector.at(pos+1).count) {
          swap(vector.at(pos), vector.at(pos+1));
          sorted = false;
        }
  }
}

// define sorting function for alphabetical sorting
void bubble_sort_letters(vector<vector<Pair>>& vector) {
  bool sorted;

  for(size_t opos{0}; opos < vector.size(); opos++) {
    sorted = false;
    while(!sorted) {
      sorted = true;
      for(size_t ipos{0}; ipos < vector.at(opos).size()-1; ipos++)
        if(vector.at(opos).at(ipos).word > vector.at(opos).at(ipos+1).word) {
          swap(vector.at(opos).at(ipos), vector.at(opos).at(ipos+1));
          sorted = false;
        }
    }
  }
}

int main(int argc , char **args) {

  // check if number of arguments is within allowed range
  if(argc < 2 || argc > 4)
    throw runtime_error("Please provide at most two options and exactly one input file.");

  // read in and open input file
  ifstream input_file{args[argc-1]};
  bool list{false}, ignore_case{false};

  // set provided options
  for(int pos{argc-2}; pos > 0; pos--) {
    if(static_cast<string>(args[pos]) == "-I")
      ignore_case = true;
    if(static_cast<string>(args[pos]) == "-l")
      list = true;
  }

  // declare some variables
  int tot_count{0};
  string line, word;
  unordered_map<string, int> word_count;

  // read in all data as word-count pairs in a map/dictionary
  while(getline(input_file, line))
    for(auto c : line) {
      if(isalpha(c)) {
        // if upper_lower case should be ignored, ensure all characters are converted to lower case
        if(ignore_case)
          c = tolower(c);
        word.push_back(c);
      }
      if(!word.empty() && !isalpha(c)) {
        if(word_count.find(word) == word_count.end()) {
          word_count.insert({word, 1});
          word.clear();
        }
        else {
          word_count.find(word)->second++;
          word.clear();
        }
      }
    }
  if(!word.empty()) {
    if(word_count.find(word) == word_count.end())
      word_count.insert({word, 1});
    else
      word_count.find(word)->second++;
  }
  input_file.close();

  // transfer word-count pairs to vector (for easy calculations) and count total number of words
  vector<Pair> wc_vec;
  for(const auto& p : word_count) {
    wc_vec.push_back({p.first, p.second});
    tot_count += p.second;
  }

  // if word and counts should be listed execute body of if-statement
  if(list) {
    bubble_sort(wc_vec);

    vector<vector<Pair>> sorted_word_count;
    vector<Pair> help_vec;
    for(size_t pos{1}; pos < wc_vec.size(); pos++) {
      help_vec.push_back(wc_vec.at(pos-1));

      if(wc_vec.at(pos).count != wc_vec.at(pos-1).count || pos == wc_vec.size()-1) {
        sorted_word_count.push_back(help_vec);
        help_vec.clear();
      }
    }

    bubble_sort_letters(sorted_word_count);

    for(const auto& vec : sorted_word_count)
      for(const auto& wordcount : vec)
        cout << wordcount.word << '\t' << wordcount.count << endl;
  }
  else // if word - count pairs should not be listed just output number of total words and distinct words
    cout << word_count.size() << " / " << tot_count << endl;

  return 0;
}
