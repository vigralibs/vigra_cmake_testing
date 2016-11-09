import os
from git import Repo

if os.path.exists('vigra_cmake'):
    if not os.path.isdir('vigra_cmake'):
        raise RuntimeError('"vigra_cmake" is not a directory')
    print("Updating the vigra_cmake repository.")
    repo = Repo("vigra_cmake")
    repo.remotes.origin.pull()
else:
    print("Cloning the vigra_cmake repository.")
    Repo.clone_from("https://github.com/vigralibs/vigra_cmake.git", "vigra_cmake")
    repo = Repo("vigra_cmake")
