#include <iostream>

#include "codelift.h"

using namespace std;

int main(int argc,char **argv)
{
    // cout << "input:" << argv[1] << endl;
    const char *result;
    string flag = argv[1];
    string input = argv[2];
    const char *p = input.c_str();
    // cout << "Hello, world!" << endl;
    if (flag == "guessInput"){
        result = guessInput(p);
    }
    else{
        result = getDeoaep(p);
    }
    
    cout << result << endl;
    // cout << "Hello, world!" << endl;
    return 0;
}