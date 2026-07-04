#include <iostream>

#include "sdk_api.hpp"

int main()
{
    std::cout << "MJ SDK version: " << mj::sdk::version() << std::endl;
    return 0;
}
