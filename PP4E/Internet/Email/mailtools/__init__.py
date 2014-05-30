"""
##################################################################################
mailtools package: interface to mail server transfers, used by pymail2, PyMailGUI, 
and PyMailCGI;  does loads, sends, parsing, composing, and deleting, with part
attachments, encodings (of both the email and Unicdode kind), etc.;  the parser,
fetcher, and sender classes here are designed to be mixed-in to subclasses which
use their methods, or used as embedded or standalone objects;

this package also includes convenience subclasses for silent mode, and more;  
loads all mail text if pop server doesn't do top;  doesn't handle threads or UI
here, and allows askPassword to differ per subclass;  progress callback funcs get
status;  all calls raise exceptions on error--client must handle in GUI/other;
this changed from file to package: nested modules imported here for bw compat;

4E: need to use package-relative import syntax throughout, because in Py 3.X 
package dir in no longer on module import search path if package is imported 
elsewhere (from another directory which uses this package);  also performs
Unicode decoding on mail text when fetched (see mailFetcher), as well as for
some text part payloads which might have been email-encoded (see mailParser);

TBD: in saveparts, should file be opened in text mode for text/ contypes?
TBD: in walkNamedParts, should we skip oddballs like message/delivery-status?
TBD: Unicode support has not been tested exhaustively: see Chapter 13 for more 
on the Py3.1 email package and its limitations, and the policies used here;
##################################################################################
"""

# collect contents of all modules here, when package dir imported directly
from .mailFetcher import *
from .mailSender  import *                 # 4E: package-relative
from .mailParser  import *

# export nested modules here, when from mailtools import *
__all__ = 'mailFetcher', 'mailSender', 'mailParser'

# self-test code is in selftest.py to allow mailconfig's path 
# to be set before running thr nested module imports above
