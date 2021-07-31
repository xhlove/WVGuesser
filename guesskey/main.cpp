#include <iostream>
#include <cstring>

// #include "Socket.h"
// #include <process.h>
#include "codelift.h"

using namespace std;

int main(int argc,char **argv)
{
    std::string input;
    const char *result = "err";
    std::string flag_guessInput = "guessInput";
    std::string flag_getDeoaep = "getDeoaep";

    while (1){
        cin >> input;
        // cout << "The value you entered is " << input << endl;
        // 以|分割得到要调用的方法名和具体参数
        int pos = input.find_first_of('|');
        std::string func_name = input.substr(0, pos);
        std::string func_arg = input.substr(pos + 1);
        // 调用函数
        if(strcmp(func_name.c_str(), flag_guessInput.c_str()) == 0){
            result = guessInput(func_arg.c_str());
        }
        else if(strcmp(func_name.c_str(), flag_getDeoaep.c_str()) == 0){
            result = getDeoaep(func_arg.c_str());
        }
        else{
            break;
        }
        cout << result << endl;
    }

    return 0;
}

// unsigned __stdcall Answer(void* a) {
//     Socket* s = (Socket*) a;
//     std::string flag = "guessInput";
//     while (1) {
//         std::string msg = s->ReceiveLine();
//         // 去除末尾的换行符
//         msg = msg.substr(0, msg.size() - 1);
//         // 以|分割得到要调用的方法名和具体参数
//         int pos = msg.find_first_of('|');
//         std::string func_name = msg.substr(0, pos);
//         std::string func_arg = msg.substr(pos + 1);
//         const char *result = "err";
//         // 调用函数
//         if(strcmp(func_name.c_str(), flag.c_str()) == 0){
//             result = guessInput(func_arg.c_str());
//         }
//         else{
//             result = getDeoaep(func_arg.c_str());
//         }
//         if (msg.empty()){
//             break;
//         }
//         s->SendLine(result);
//     }
//     delete s;
//     return 0;
// }

// int main(int argc,char **argv)
// {
//     std::string::size_type sz;
//     int port = std::stoi(argv[1], &sz);
//     cout << "listen at:" << port << endl;
//     SocketServer in(port, 10);
//     while (1) {
//         Socket* s=in.Accept();
//         unsigned ret;
//         _beginthreadex(0,0,Answer,(void*) s,0,&ret);
//     }
//     return 0;
// }