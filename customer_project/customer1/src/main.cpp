#include <iostream>

#include "customer1_api.hpp"
#include "sdk_api.hpp"

namespace mj {
namespace customer1 {

const char* name()
{
    return "customer1";
}

} // namespace customer1
} // namespace mj

int main()
{
    std::cout << mj::customer1::name() << " SDK version: " << mj::sdk::version() << std::endl;
    return 0;
}
