import os
import unittest
from git import Repo

VERBOSE = True

if os.path.exists('vigra_cmake'):
    if not os.path.isdir('vigra_cmake'):
        raise RuntimeError('"vigra_cmake" is not a directory')
    print("The vigra_cmake repository already exists.")
else:
    print("Cloning the vigra_cmake repository.")
    Repo.clone_from(
        "https://github.com/vigralibs/vigra_cmake.git", "vigra_cmake")
    repo = Repo("vigra_cmake")


def run_unbuffered_command(raw_command, directory):
    import shlex
    from subprocess import Popen, PIPE, STDOUT
    proc = Popen(shlex.split(raw_command), cwd=directory,
                 stdout=PIPE, stderr=STDOUT)
    output = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        if VERBOSE:
            print(line)
        output.append(line)
    proc.communicate()
    if proc.returncode:
        raise RuntimeError(output)
    return output


def cmake_configure(testname):
    import shutil
    import os
    base_dir = os.path.dirname(os.path.realpath(__file__))
    build_dir = os.path.join(base_dir, testname, 'build')
    if os.path.exists(build_dir):
        if VERBOSE:
            print("Removing previous build dir: " + build_dir)
        shutil.rmtree(build_dir)
    if VERBOSE:
        print("Creating build dir: " + build_dir)
    os.mkdir(build_dir)
    return run_unbuffered_command(r'cmake ..', build_dir)


def cmake_build(testname):
    import os
    base_dir = os.path.dirname(os.path.realpath(__file__))
    build_dir = os.path.join(base_dir, testname, 'build')
    return run_unbuffered_command(r'cmake --build .', build_dir)


def cmake_test(testname):
    import os
    base_dir = os.path.dirname(os.path.realpath(__file__))
    build_dir = os.path.join(base_dir, testname, 'build')
    return run_unbuffered_command(r'ctest', build_dir)

class zlib_test_00(unittest.TestCase):

    def test_main(self):
        cmake_configure('zlib_test_00')
        cmake_build('zlib_test_00')


class zlib_test_01(unittest.TestCase):

    def test_main(self):
        cmake_configure('zlib_test_01')
        cmake_build('zlib_test_01')
        cmake_test('zlib_test_01')


if __name__ == '__main__':
    unittest.main()
