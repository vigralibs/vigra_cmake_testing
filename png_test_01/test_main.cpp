#include <png.h>

#include <iostream>

int main()
{
    std::cout << ::png_access_version_number() << '\n';
    return 0;
}
