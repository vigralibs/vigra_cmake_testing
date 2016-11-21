#include <zconf.h>
#include <zlib.h>

int main()
{
    ::z_stream z;
    (void)z;
    const char *v = zlibVersion();
    return 0;
}
