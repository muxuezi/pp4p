#!/usr/bin/python
"""
################################################################################
On view link click on main/root HTML page: make POP password input page;

this could almost be an HTML file because there are likely no input params yet,
but I wanted to use standard header/footer functions and display the site/user
names which must be fetched;  on submission, does not send the user along with 
password here, and only ever sends both as URL params or hidden fields after the
password has been encrypted by a user-uploadable encryption module; 
################################################################################
"""

# page template
pswdhtml = """
<form method=post action=%sonViewPswdSubmit.py>
<p>
Please enter POP account password below, for user "%s" and site "%s".
<p><input name=pswd type=password>
<input type=submit value="Submit"></form></p>

<hr><p><i>Security note</i>: The password you enter above will be transmitted
over the Internet to the server machine, but is not displayed, is never
transmitted in combination with a username unless it is encrypted or obfuscated,
and is never stored anywhere: not on the server (it is only passed along as hidden
fields in subsequent pages), and not on the client (no cookies are generated).
This is still not guaranteed to be totally safe; use your browser's back button
to back out of PyMailCgi at any time.</p>
"""

# generate the password input page
import commonhtml                                         # usual parms case:
user, pswd, site = commonhtml.getstandardpopfields({})    # from module here,
commonhtml.pageheader(kind='POP password input')          # from html|url later
print(pswdhtml % (commonhtml.urlroot, user, site))
commonhtml.pagefooter()
