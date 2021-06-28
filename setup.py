#!/usr/bin/env python

# from distutils.core import setup, Extension
from setuptools import dist, setup, Extension, find_packages
# from numpy.distutils.misc_util import get_numpy_include_dirs
# import numpy
import os
import codecs
import re

# Copied from wheel package
here = os.path.abspath(os.path.dirname(__file__))

__version__ = "0.1.5.3"

# bootstrap numpy
dist.Distribution().fetch_build_eggs(['numpy'])

setup(
# ext_modules=[Extension("tilecycles_c", ["c_tilecycles.cpp", "tilecycles_c.cpp"],
#                              extra_compile_args=["-std=c++11", ],
#                              include_dirs=get_numpy_include_dirs())],
#       headers=["tilecycles_c.hpp"],
      # include_dirs=get_numpy_include_dirs(),
      name='TileCycles',
      version=__version__,
      zip_safe=False,
      # py_modules=['tilecycles'],
      description='Bla bla.',
      #long_description=README + '\n\n' +  CHANGES,
      classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
],
    packages=find_packages(),

    author='Masakazu Matsumoto',
    author_email='vitroid@gmail.com',
    url='https://github.com/vitroid/TileCycles/',
    keywords=['tile by cycles', ],
    license='MIT',
    install_requires=['numpy', 'networkx', 'cycless'],
)
