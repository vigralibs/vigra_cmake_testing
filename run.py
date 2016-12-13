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
        line = text_type(line, 'utf-8', errors='ignore')
        if VERBOSE:
            print(line[:-1])
        output += line
    proc.communicate()
    if proc.returncode:
        raise RuntimeError(output)
    return output


def grep(s, substr):
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


def cmake_configure(testname, extra_param=None):
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


def cmake_test(testname, extra_param=None):
    build_dir = default_build_dir(testname)
    if extra_param is None:
        return run_unbuffered_command(r'ctest', build_dir)
    else:
        return run_unbuffered_command(r'ctest ' + extra_param, build_dir)


class path_ctx(object):

    def __init__(self, tname):
        self._tname = tname

    def __enter__(self):
        import platform
        import os
        if 'Windows' in platform.system():
            self._original_path = os.environ['PATH']
            with open(os.path.join(default_build_dir(self._tname), '.vad', 'vad_path_Debug')) as fpath:
                extra_path = fpath.readline()[:-1]
            os.environ['PATH'] = extra_path + ';' + os.environ['PATH']

    def __exit__(self, *args):
        import platform
        import os
        if 'Windows' in platform.system():
            os.environ['PATH'] = self._original_path


class zlib_test_00(unittest.TestCase):

    def test_main(self):
        import platform
        tname = type(self).__name__
        if 'Windows' in platform.system():
            return
        rm_fr(default_build_dir(tname))
        rm_fr(default_external_dir(tname))
        cmake_configure(tname)
        cmake_build(tname)
        cmake_test(tname)


class zlib_test_01(unittest.TestCase):

    def test_main(self):
        import os
        import platform
        tname = type(self).__name__
        include_dirs = [os.path.join(tname, 'external', 'ZLIB'), os.path.join(
            tname, 'external', 'ZLIB', 'build_external_dep')]
        rm_fr(default_build_dir(tname))
        rm_fr(default_external_dir(tname))
        if 'Windows' in platform.system():
            conf_opts = '-G "Visual Studio 14 2015 Win64"'
            test_opts = '-C Debug'
        else:
            conf_opts = None
            test_opts = None
        cmake_configure(tname, conf_opts)
        out = grep(cmake_build(tname), 'main.cpp')
        # Check that the include dirs of the live dependency are passed in
        # while building main.
        self.assertTrue(grep(out, include_dirs[0]))
        self.assertTrue(grep(out, include_dirs[1]))
        with path_ctx(tname):
            cmake_test(tname, test_opts)


class tiff_test_00(unittest.TestCase):

    def test_main(self):
        import platform
        tname = type(self).__name__
        if 'Windows' in platform.system():
            return
        rm_fr(default_build_dir(tname))
        rm_fr(default_external_dir(tname))
        cmake_configure(tname)
        cmake_build(tname)
        cmake_test(tname)


class tiff_test_01(unittest.TestCase):

    def test_main(self):
        import os
        import platform
        tname = type(self).__name__
        include_dirs = [os.path.join(tname, 'external', 'TIFF'), os.path.join(
            tname, 'external', 'TIFF', 'build_external_dep')]
        rm_fr(default_build_dir(tname))
        rm_fr(default_external_dir(tname))
        if 'Windows' in platform.system():
            conf_opts = '-G "Visual Studio 14 2015 Win64"'
            test_opts = '-C Debug'
        else:
            conf_opts = None
            test_opts = None
        cmake_configure(tname, conf_opts)
        out = grep(cmake_build(tname), 'main.cpp')
        # Check that the include dirs of the live dependency are passed in
        # while building main.
        self.assertTrue(grep(out, include_dirs[0]))
        self.assertTrue(grep(out, include_dirs[1]))
        with path_ctx(tname):
            cmake_test(tname, test_opts)

class png_test_01(unittest.TestCase):

    def test_main(self):
        import os
        import platform
        tname = type(self).__name__
        include_dirs = [os.path.join(tname, 'external', 'PNG'), os.path.join(
            tname, 'external', 'PNG', 'build_external_dep')]
        rm_fr(default_build_dir(tname))
        rm_fr(default_external_dir(tname))
        if 'Windows' in platform.system():
            conf_opts = '-G "Visual Studio 14 2015 Win64"'
            test_opts = '-C Debug'
        else:
            conf_opts = None
            test_opts = None
        cmake_configure(tname, conf_opts)
        out = grep(cmake_build(tname), 'main.cpp')
        # Check that the include dirs of the live dependency are passed in
        # while building main.
        self.assertTrue(grep(out, include_dirs[0]))
        self.assertTrue(grep(out, include_dirs[1]))
        with path_ctx(tname):
            cmake_test(tname, test_opts)

if __name__ == '__main__':
    unittest.main()
