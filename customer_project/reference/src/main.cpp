#include "sdk_api.hpp"

#include <iostream>

int main()
{
    std::cout << "MJ SDK version: " << mj::sdk::version() << std::endl;
    return 0;
}
