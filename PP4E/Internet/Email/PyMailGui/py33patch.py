#!/usr/bin/python3
"""
===============================================================================
[September 19, 2013]

Fix a backward-incompatible Python 3.3 library change that broke
email address displays for non-ASCII names in the PyMailGUI email
client, presented in the book Programming Python, 4th Edition (PP4E).
This patch is compatible with all Python 3.X, through version 3.3.

TO APPLY THIS PATCH: 

1) Add this file to the PyMailGUI folder, located in the
book's examples tree at PP4E\Internet\Email\PyMailGui.

2) Add an import of this file at the top of either the system's
common SharedNames.py, or its main/top-level file PyMailGui.py,
both located in the same PyMailGUI folder; or simply copy and
use the updated SharedNames.py file included with this patch:

    # python 3.3+ hack (formataddr change)
    import py33patch


THE BOOK CONTEXT (PP4E):

Pages 935-937 trace the steps that PyMaiGUI takes to extract 
email addresses for display, applying MIME and Unicode decoding.
In PyMailGUI code, this spans from Chapter 14's ViewWindow class
to Chapter 13's mailParser module.  This process is emulated in 
the self-test code below.  Only the last step--the email package's 
utils.formataddr, which puts name/addr pairs back together--has 
changed in 3.3, but is sufficient to cause the PyMailGUI breakage.

THE PYTHON CHANGE AND FIX:

Python 3.3+'s email.utils.formataddr now automatically MIME
encodes non-ASCII names in address pairs.  For some reason, 
3.3 did not make this new and very different behavior an 
optional feature disabled by default; did not provide a clear
mechanism for disabling it at all; and didn't even document 
the incompatible change for current email users.  

The most straightforward fix seems to be to copy and install the
3.2 and earlier version of this function, which this file does.
This technique is error-prone in general, but requires no other
changes, and is backward compatible with all prior 3.X releases.

ON BATTERY DEPENDENCY:

3.3+'s email package may assume you'll use a different headers
API altogether.  But carelessly breaking the existing API with
no regard to impacts on its real-world users seems just plain 
rude.  PyMailGUI has long used this utility for display, not 
for send headers, which it MIME-encodes manually when needed.

For the record, the general PyMailGUI use case has been noted 
explicitly to Python and email package developers in the past.
It's unfortunate when incompatible Python change occurs not 
only in the absence of end-user data, but in defiance of it.
===============================================================================
"""


import email.utils
from email.utils import specialsre, escapesre

def py32_formataddr(pair):
    """
    HACK: Copied from 3.2 standard lib: 3.3 auto MIME-encodes non-ASCII
    names, and offers no way to disable this new/differing functionality;
    
    The inverse of parseaddr(), this takes a 2-tuple of the form
    (realname, email_address) and returns the string value suitable
    for an RFC 2822 From, To or Cc header.

    If the first element of pair is false, then the second element is
    returned unmodified.
    """
    name, address = pair
    if name:
        quotes = ''
        if specialsre.search(name):
            quotes = '"'
        name = escapesre.sub(r'\\\g<0>', name)
        return '%s%s%s <%s>' % (quotes, name, quotes, address)
    return address

# HACK: on import, reset library to prior behavior for this process
email.utils.formataddr = py32_formataddr



#==============================================================================
# SELF-TEST if run: output (below) should be same in 3.0 through 3.3.
# Emulates what pymailgui does to display address headers in fetched emails.
# Best run/viewed in a Unicode-friendly GUI like IDLE (else see print() redef).
#==============================================================================


if __name__ == '__main__':   
    from pprint import pprint
    from email.header import decode_header
    from email.utils import getaddresses, formataddr

    """
    def print(x):
        import builtins
        builtins.print(ascii(x))  # use me if unicode errors at your console 
    """
    
    # from a couple spams: utf-8 unicode, quoted/base64 mime
    rawheader = ('=?utf-8?q?Promo=C3=A7=C3=A3o_Cielo?= <acounts@passaport.com>, ' +
                 '=?utf-8?b?5reY5a6d5Lqk5piT?= <admin@system.mail>')

    pairs = getaddresses([rawheader])            # split to name/addr pairs
    pprint(pairs)

    addrs = []
    for (name, addr) in pairs:
        print('\n' + name)
        
        abytes, aenc = decode_header(name)[0]    # MIME decode name (single part)
        print(abytes)
        
        name = abytes.decode(aenc)               # Unicode decode name (to str)
        print(name)
        
        joined = formataddr((name, addr))        # join name/addr=>3.3 change!     
        print(joined)
        addrs.append(joined)                     # one or more addrs
    
    print('\n' + ', '.join(addrs))               # combine decoded addrs


#==============================================================================
# EXPECTED OUTPUT if run directly.
# Note: this file doesn't require line2 = "# -*- coding: utf-8 -*-" for the
# non-ASCIIs in expected output stings, because utf-8 is the Python default 
# for source file ecoding, and this is the encoding in which this file was created.
#==============================================================================


# CORRECT output with patch, 3.0 through 3.3
"""
[('=?utf-8?q?Promo=C3=A7=C3=A3o_Cielo?=', 'acounts@passaport.com'),
 ('=?utf-8?b?5reY5a6d5Lqk5piT?=', 'admin@system.mail')]

=?utf-8?q?Promo=C3=A7=C3=A3o_Cielo?=
b'Promo\xc3\xa7\xc3\xa3o Cielo'
Promoção Cielo
Promoção Cielo <acounts@passaport.com>

=?utf-8?b?5reY5a6d5Lqk5piT?=
b'\xe6\xb7\x98\xe5\xae\x9d\xe4\xba\xa4\xe6\x98\x93'
淘宝交易
淘宝交易 <admin@system.mail>

Promoção Cielo <acounts@passaport.com>, 淘宝交易 <admin@system.mail>
"""


# ERROR output in 3.3 only, if disable (#-out) email.utils.formataddr reset above
"""
[('=?utf-8?q?Promo=C3=A7=C3=A3o_Cielo?=', 'acounts@passaport.com'),
 ('=?utf-8?b?5reY5a6d5Lqk5piT?=', 'admin@system.mail')]

=?utf-8?q?Promo=C3=A7=C3=A3o_Cielo?=
b'Promo\xc3\xa7\xc3\xa3o Cielo'
Promoção Cielo
=?utf-8?q?Promo=C3=A7=C3=A3o_Cielo?= <acounts@passaport.com>

=?utf-8?b?5reY5a6d5Lqk5piT?=
b'\xe6\xb7\x98\xe5\xae\x9d\xe4\xba\xa4\xe6\x98\x93'
淘宝交易
=?utf-8?b?5reY5a6d5Lqk5piT?= <admin@system.mail>

=?utf-8?q?Promo=C3=A7=C3=A3o_Cielo?= <acounts@passaport.com>, =?utf-8?b?5reY5a6d5Lqk5piT?= <admin@system.mail>
"""
