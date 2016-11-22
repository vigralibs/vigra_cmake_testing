#include <zconf.h>
#include <zlib.h>

#include <iostream>

int main()
{
    ::z_stream z;
    (void)z;
    const char *v = zlibVersion();
    std::cout << v << '\n';
    return 0;
}
