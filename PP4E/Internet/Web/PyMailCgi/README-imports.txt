Note: in the book, the example titles of imported module files
give their paths as cgi-bin/, not this directory, and this is
hw the examples are shipped: all modules are in cgi-bin/ along 
with the CGI scripts that use them.  This latter structure is 
more portable, because CGI scripts spawned as processes on most
platforms will have their current working directory set to cgi-bin/
for imports.  This includes the Python-coded web server of the book
when running on Windows.
