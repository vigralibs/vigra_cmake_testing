cmake_minimum_required(VERSION 3.2 FATAL_ERROR)

project(tiff_test_00 VERSION 0.1 LANGUAGES C CXX)

enable_testing()

set(CMAKE_VERBOSE_MAKEFILE ON)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/../vigra_cmake")

set(VAD_VERBOSE TRUE)
include(VigraAddDep)

vigra_add_dep(TIFF REQUIRED)
add_executable(test_main test_main.cpp)
target_link_libraries(test_main TIFF::TIFF)
add_test(test_main test_main)
