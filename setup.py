#!/usr/bin/env python

import re
from os.path import abspath, dirname, join
from setuptools import setup, find_packages


CURDIR = dirname(abspath(__file__))

CLASSIFIERS = '''
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3.12
Programming Language :: Python :: 3.13
Programming Language :: Python :: 3 :: Only
Topic :: Software Development :: Testing
Framework :: Robot Framework
Framework :: Robot Framework :: Library
'''.strip().splitlines()

with open(join(CURDIR, 'src', 'WebDialogs', '__init__.py')) as f:
    VERSION = re.search('\n__version__ = "(.*)"', f.read()).group(1)
    
with open(join(CURDIR, 'README.md')) as f:
    DESCRIPTION = f.read()
    
with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name             = 'robotframework-webdialogs',
    version          = VERSION,
    description      = 'k',
    long_description = DESCRIPTION,
    author           = 'Lautaro Linquimán',
    author_email     = 'lylinquiman@gmail.com',
    url              = 'https://github.com/Ymil/robotframework-webdialogs',
    license          = 'Apache License 2.0',
    keywords         = '',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    python_requires  = '>=3.8, <3.14',
    install_requires = REQUIREMENTS,
    package_dir      = {'': 'src'},
    packages         = find_packages('src'),
)