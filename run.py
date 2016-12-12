import os
import unittest
from git import Repo
from six import text_type

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


def run_unbuffered_command(raw_command, directory, **kwargs):
    import shlex
    from subprocess import Popen, PIPE, STDOUT
    proc = Popen(shlex.split(raw_command), cwd=directory,
                 stdout=PIPE, stderr=STDOUT, **kwargs)
    output = ''
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        line = text_type(line,'utf-8', errors='ignore')
        if VERBOSE:
            print(line[:-1])
        output += line
    proc.communicate()
    if proc.returncode:
        raise RuntimeError(output)
    return output


def grep(s,substr):
    l = s.split('\n')
    return '\n'.join([_ for _ in l if substr in _])


def default_build_dir(testname):
    import os
    base_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_dir, testname, 'build')

def default_external_dir(testname):
    import os
    base_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_dir, testname, 'external')

def rm_fr(path):
    import os
    import shutil
    import stat
    def del_rw(action, name, exc):
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)
    if os.path.isdir(path) and not os.path.islink(path):
        # NOTE: the idea here is that certain git dirs in Windows
        # might be read-only after checkout by cmake, and that prevents
        # rmtree from working. We then forcibly remove the read-only flag
        # and remove the offending file.
        shutil.rmtree(path, onerror=del_rw)
    elif os.path.exists(path):
        os.remove(path)

def cmake_configure(testname,extra_param = None):
    import shutil
    import os
    build_dir = default_build_dir(testname)
    if os.path.exists(build_dir):
        if VERBOSE:
            print("Removing previous build dir: " + build_dir)
        shutil.rmtree(build_dir)
    if VERBOSE:
        print("Creating build dir: " + build_dir)
    os.mkdir(build_dir)
    if extra_param is None:
        return run_unbuffered_command(r'cmake ..', build_dir)
    else:
        return run_unbuffered_command(r'cmake .. ' + extra_param, build_dir)


def cmake_build(testname):
    build_dir = default_build_dir(testname)
    return run_unbuffered_command(r'cmake --build .', build_dir)


def cmake_test(testname, extra_param = None):
    build_dir = default_build_dir(testname)
    if extra_param is None:
        return run_unbuffered_command(r'ctest', build_dir)
    else:
        return run_unbuffered_command(r'ctest ' + extra_param, build_dir)


class zlib_test_00(unittest.TestCase):

    def test_main(self):
        import platform
        if 'Windows' in platform.system():
            return
        rm_fr(default_build_dir('zlib_test_00'))
        rm_fr(default_external_dir('zlib_test_00'))
        cmake_configure('zlib_test_00')
        cmake_build('zlib_test_00')
        cmake_test('zlib_test_00')


class zlib_test_01(unittest.TestCase):

    def test_main(self):
        import os
        import platform
        include_dirs = [os.path.join('zlib_test_01', 'external', 'ZLIB'), os.path.join('zlib_test_01', 'external', 'ZLIB', 'build_external_dep')]
        rm_fr(default_build_dir('zlib_test_01'))
        rm_fr(default_external_dir('zlib_test_01'))
        if 'Windows' in platform.system():
            conf_opts = '-G "Visual Studio 14 2015 Win64"'
            test_opts = '-C Debug'
        else:
            conf_opts = None
            test_opts = None
        cmake_configure('zlib_test_01', conf_opts)
        out = grep(cmake_build('zlib_test_01'),'main.cpp')
        # Check that the include dirs of the live dependency are passed in
        # while building main.
        self.assertTrue(grep(out,include_dirs[0]))
        self.assertTrue(grep(out,include_dirs[1]))
        if 'Windows' in platform.system():
            original_path = os.environ['PATH']
            extra_path = open(os.path.join(default_build_dir('zlib_test_01'),'.vad','vad_path_Debug')).readline()[:-1]
            os.environ['PATH'] =  extra_path + ';' + os.environ['PATH']
        cmake_test('zlib_test_01', test_opts)
        if 'Windows' in platform.system():
            os.environ['PATH'] = original_path

class tiff_test_00(unittest.TestCase):

    def test_main(self):
        import platform
        if 'Windows' in platform.system():
            return
        rm_fr(default_build_dir('tiff_test_00'))
        rm_fr(default_external_dir('tiff_test_00'))
        cmake_configure('tiff_test_00')
        cmake_build('tiff_test_00')
        cmake_test('tiff_test_00')

class tiff_test_01(unittest.TestCase):

    def test_main(self):
        import os
        import platform
        include_dirs = [os.path.join('tiff_test_01', 'external', 'TIFF'), os.path.join('tiff_test_01', 'external', 'TIFF', 'build_external_dep')]
        rm_fr(default_build_dir('tiff_test_01'))
        rm_fr(default_external_dir('tiff_test_01'))
        if 'Windows' in platform.system():
            conf_opts = '-G "Visual Studio 14 2015 Win64"'
            test_opts = '-C Debug'
        else:
            conf_opts = None
            test_opts = None
        cmake_configure('tiff_test_01', conf_opts)
        out = grep(cmake_build('tiff_test_01'),'main.cpp')
        # Check that the include dirs of the live dependency are passed in
        # while building main.
        self.assertTrue(grep(out,include_dirs[0]))
        self.assertTrue(grep(out,include_dirs[1]))
        if 'Windows' in platform.system():
            original_path = os.environ['PATH']
            extra_path = open(os.path.join(default_build_dir('tiff_test_01'),'.vad','vad_path_Debug')).readline()[:-1]
            print("Adding the following entries to the PATH: " + extra_path)
            os.environ['PATH'] =  extra_path + ';' + os.environ['PATH']
        cmake_test('tiff_test_01', test_opts)
        if 'Windows' in platform.system():
            os.environ['PATH'] = original_path

if __name__ == '__main__':
    unittest.main()
