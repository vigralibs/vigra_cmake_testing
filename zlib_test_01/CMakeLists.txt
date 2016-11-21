cmake_minimum_required(VERSION 3.2 FATAL_ERROR)

project(zlib_test_01 VERSION 0.1 LANGUAGES C CXX)

enable_testing()

set(CMAKE_VERBOSE_MAKEFILE ON)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/../vigra_cmake")

set(VAD_VERBOSE TRUE)
include(VigraAddDep)
include(VigraAddTest)

vigra_add_dep(ZLIB LIVE)
vigra_add_test(test_main SOURCES test_main.cpp)
target_link_libraries(test_main ZLIB::ZLIB)
