"""Cythonize everything that needs to be."""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from os import listdir, path, walk

import numpy

if __name__ == "__main__":
    ext_modules = []
    for root, directories, files in walk("sc2"):
        for d in directories:
            for file in listdir(path.join(root, d)):
                if file.endswith("pyx"):
                    ext_modules.append(Extension("*", [path.join(root, d, file)]))
        for file in files:
            if file.endswith("pyx"):
                ext_modules.append(Extension("*", [path.join(root, file)]))

    setup(
        name="sc2",
        cmdclass={"build_ext": build_ext},
        ext_modules=cythonize(ext_modules),
        include_dirs=[numpy.get_include()],
    )
