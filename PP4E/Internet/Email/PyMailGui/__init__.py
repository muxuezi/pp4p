# intentionally empty (except for a docstring, and this...)

"""
meant for future expansion; as is, same-directory internal 
imports here are not package-relative, so they assume this 
system is run as a top-level program (to import from "."), or
is listed on sys.path directly (to use absolute imports);  in 
Python 3.X, a package's directory is not included on sys.path
automatically, so use as a package would require changes to 
internal imports (e.g., moving the top-level script up one 
level, and using "from . import module" imports throughout);
"""
