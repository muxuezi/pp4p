****UPDATE FOR 4TH EDITION****
This is a Python 2.X system which was an example
in the 2nd edition.  Its code may or may not be 
updated to Python 3.X, but its chapter will not.
It's included here as supplemental example only.
----


****UPDATE FOR 3RD EDITION****
This is an old example site from the 2nd Edition,
and is no longer maintained, or covered in the 
book.  Its code and original chapter (Chapter/)
are included here as an optional supplement.
----


This directory contains the PyErrata error reporting
system.  The root page is defined by pyerrata.html;
other files are either more html pages (.html), cgi
scripts coded in Python (.cgi), or Python support 
modules (.py) used by the cgi scripts.  Subdirectories:

- AdminTools: command-line tools for processing reports
- DbaseFiles: data storage for flat file database mode
- DbaseShelve: data storage for shelve database mode
- Mutex: a mutual exclusion file locking utility, for shelves

Note: pickle and shelve files in the Dbase* directories are
not necessarily compatible across all platforms or Python 
releases.  You may need to recreate these from scratch in
your server install.
