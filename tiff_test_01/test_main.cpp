#include <tiff.h>
#include <tiffio.h>

#include <iostream>

int main()
{
    std::cout << ::TIFFGetVersion() << '\n';
    return 0;
}
