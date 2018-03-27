CASICS CodeOrNot
================

<img width="100px" align="right" src=".graphics/casics-logo-small.svg">

CASICS _CodeOrNot_ is a Python 3 package implementing heuristic methods for determining whether a file or directory contains software source (or not).  The analysis is oriented towards detecting code: a repository containing a mix of documents and even one source code file will be considered to contain code, and conversely, if there is no sign of source code, it will be labeled as "not" being source code.

*Authors*:      [Michael Hucka](http://github.com/mhucka)<br>
*Repository*:   [https://github.com/casics/codeornot](https://github.com/casics/codeornot)<br>
*License*:      Unless otherwise noted, this content is licensed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) license.

☀ Introduction
-----------------------------

In performing source code repository analysis for classification tasks, a basic first step is to decide whether a source code repository actually contains code.  Some repositories contain documents or other files and are not actually repositories for software; those are cases that a system for analyzing source code could skip.  CodeOrNot is a Python 3 package that uses heuristics to answer the question "does it contain code, or not?"

Some cases are quite easy to decide: if a collection of files contains even one `.c` file, it can be reasonably assumed to contain C code, and thus the answer returned by CodeOrNot will be "code".  Some other cases are more difficult.  For example, files may contain code but not have file name extensions, and so determining whether they contain code or not requires examining the content.  Other examples are gray zones: should a repository containining LaTeX files and a single `Makefile` be considered to contain code?  After all, a `Makefile` can contain code&mdash;does that count?  (The position taken by CodeOrNot is no, a single `Makefile` is not enough to consider the repository to be a code repository.)

CodeOrNot also provides some simple utilities modules that may be useful in other contexts:

* The `textcheck` module provides functions such as `majority_language()`, which takes a list of text strings and reports the most likely human language in which the text strings are written.  (It does this by using a combination of [ftfy](https://github.com/LuminosoInsight/python-ftfy),  [cld2](https://github.com/CLD2Owners/cld2), and a majority vote.)

* The `codecheck` module provides functions such as `code_filename()` and `noncode_filename`, which can be used to infer whether a file is likely to be code or noncode based on its name.  These work by using built-in lists of file name rules.

⁇ Getting help and support
--------------------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/casics/codeornot/issues) for this repository.

♬ Contributing &mdash; info for developers
------------------------------------------

A lot remains to be done on CASICS in many areas.  We would be happy to receive your help and participation if you are interested.  Please feel free to contact the developers either via GitHub or the mailing list [casics-team@googlegroups.com](casics-team@googlegroups.com).

Everyone is asked to read and respect the [code of conduct](CONDUCT.md) when participating in this project.

❤️ Acknowledgments
------------------

This material is based upon work supported by the [National Science Foundation](https://nsf.gov) under Grant Number 1533792 (Principal Investigator: Michael Hucka).  Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.

<br>
<div align="center">
  <a href="https://www.nsf.gov">
    <img width="105" height="105" src=".graphics/NSF.svg">
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src=".graphics/caltech-round.svg">
  </a>
</div>
