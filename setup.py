#!/usr/bin/env python3
# =============================================================================
# @file    setup.py
# @brief   CodeOrNot setup file
# @author  Michael Hucka <mhucka@caltech.edu>
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/casics/codeornot
# =============================================================================

import os
from   setuptools import setup, find_packages
import sys
import codeornot

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as f:
    reqs = f.read().rstrip().splitlines()

setup(
    name=codeornot.__version__.__title__.lower(),
    description=codeornot.__version__.__description__,
    long_description='CodeOrNot implements heuristic methods for determining the type of file or repository content.',
    keywords="program-analysis text-processing machine-learning",
    version=codeornot.__version__.__version__,
    url=codeornot.__version__.__url__,
    author=codeornot.__version__.__author__,
    author_email=codeornot.__version__.__email__,
    license=codeornot.__version__.__license__,
    packages=['codeornot'],
    install_requires=reqs,
    platforms='any',
)
