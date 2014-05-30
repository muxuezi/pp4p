"""
OVERVIEW
--------
This is the root directory for the examples package of the book
Programming Python 4th Edition.  Cross-directory imports in examples
are always fully-specified package imports, relative to the PP4E
root directory here ("from PP4E.System..."); no package-relative
imports ("from . import M") are used.  To run some programs directly,
and to import their code from outside this directory using package 
import syntax, add PP4E's container to your module search path.
The rest of this docstring provides extended usage details.


USING THIS PACKAGE
------------------
To enable imports from this tree, add the directory containing
this file's PP4E directory to your PYTHONPATH module search-path
setting, or copy the PP4E directory to your Python installation's
Lib\site-packages standard library subdirectory.  You may also 
include PP4E's container directory in a ".pth" path file too; see 
the  book Learning Python for more on module search path 
configuration.

As described in Learning Python, the Lib\site-packages directory
is automatically included in the Python module search path, and is 
where 3rd-party software is normally installed by setup.py distutils 
scripts.  Distutils was not used for this book's examples because I 
didn't want to force readers to bury the in the Python standard 
library.


AUTO-LAUNCHERS
--------------
See file README-PP4E.txt for details on running auto-launch scripts.
Note that the auto-launcher scripts shown and used in the book
add the PP4E directory to the module search path at run-time
automatically, so they may be run without any path configurations.
To run some of the more specific examples in this tree directly, 
though (outside the self-launchers context), you may need to
first add this directory to your path manually so that their 
cross-directory imports work properly.


IMPORTS IN CODE
---------------
Most cross-directory imports within the book examples tree use
fully-specified package imports, relative to the PP4E root
(e.g., "from PP4E.Text.utilities import name").  For both
readability and maintainability, very few package relative 
imports are used (e.g., "from .utilities import name").  

To use the code in your files outside this tree, use similar
fully-specified package imports; the PP4E root will avoid name
conflicts with other code, and fully-specified imports are not
dependent on the importing file's location.  Each subdirectory 
in this tree that has importable modules also has the required 
__init__.py file.
"""
