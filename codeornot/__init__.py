# =============================================================================
# @file    __init__.py
# @brief   CASICS CodeOrNot package __init__ file
# @author  Michael Hucka <mhucka@caltech.edu>
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/casics/spiral
# =============================================================================

from .__version__ import *
from .textcheck import human_language, majority_language
from .codecheck import code_language, code_filename, noncode_filename
