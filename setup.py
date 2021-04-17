#!/usr/bin/env python

# from distutils.core import setup, Extension
from setuptools import setup, Extension
import os
import codecs
import re

#Copied from wheel package
here = os.path.abspath(os.path.dirname(__file__))

__version__ = "0.1.3"

# bootstrap numpy
from setuptools import dist
dist.Distribution().fetch_build_eggs(['numpy'])
import numpy
from numpy.distutils.misc_util import get_numpy_include_dirs

setup(ext_modules=[Extension("tilecycles", ["c_tilecycles.cpp", "tilecycles.cpp"],
                             extra_compile_args = ["-std=c++11",],
                             include_dirs=get_numpy_include_dirs())],
      headers=["tilecycles.hpp"],
      # include_dirs=get_numpy_include_dirs(),
      name='TileCycles',
      version=__version__,
      zip_safe=False,
      py_modules=['tilecycles_py'],
      description='Bla bla.',
      #long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        ],
      author='Masakazu Matsumoto',
      author_email='vitroid@gmail.com',
      url='https://github.com/vitroid/TileCycles/',
      keywords=['tile by cycles',],
      license='MIT',
      install_requires=['numpy',],
      # entry_points = {
      #         'console_scripts': [
      #             'pairlist = pairlist:main'
      #         ]
      #     }
)




# from setuptools import setup, Extension
# from Cython.Build import cythonize
# import numpy
#
# sourcefiles = ["tilecycles_cython.pyx"] #, 'mt19937-64.c']
# extensions = [Extension("tilecycles_cython", sourcefiles)]
#
# setup(
#     ext_modules=cythonize(extensions),
#     include_dirs=[numpy.get_include()]
# )
