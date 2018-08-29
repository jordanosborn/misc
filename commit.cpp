#include <iostream>
#include <vector>

using namespace std;
using vec = vector<std::string>;

int main (int argc, char* argv[]) {
    vec items_in = {};
    vec items = {};
    for_each(items.begin(), items.end(), [&items_in] (in i, string s){ 
    cout << s << ": ";
    items_in.push_back(cin);
    
    });
    
    return 0;
}