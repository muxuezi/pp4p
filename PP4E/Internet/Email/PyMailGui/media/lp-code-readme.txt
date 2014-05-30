File: lp-code-readme.txt
Home: http://rmi.net/~lutz/examples-lp.html
Date: May 3, 1999
-------------------------------------------

[Update 11/03: the source code file is now a ".tgz"
gzipped tar file (not just a tar file); use a tool 
such as winzip to extract on Windows, and run an 
initial "gzip -d lp-code.tgz" before tar on Unix.]

About this file

    This tar file contains source code for all the examples
    and exercise solutions in the book _Learning Python_.
    We're providing it as an additional resource, to help
    you save typing time as you work through the book.

Using this file

    To use this file, simply download it to your machine, and 
    untar to create the directory structure and files.  To untar
    on UNIX and UNIX-like platforms, put the downloaded file in 
    a directory that is easy for you to access (e.g., in your
    home directory), and execute a command like:

        tar xvf lp-code.tar

    On other machines, other tools may have the same effect
    (e.g., the winzip program for MS-Windows knows how to untar
    tar files too).  Untarring the file will generate a new 
    subdirectory structure that looks like this:

        lpython/                     --top level directory
        lpython/lp-code-readme.txt   --this file

        lpython/unix            --version with UNIX-style newlines
        lpython/unix/examples   --code for examples in the chapters
        lpython/unix/solutions  --code for exercise solutions

        lpython/dos             --version with MS-DOS newlines
        lpython/dos/examples    --code for examples in the chapters
        lpython/dos/solutions   --code for exercise solutions

    This structure appears in the directory where you ran the
    untar operation, and of course you should think "\" instead
    of "/" if you're on a DOS or Windows machine.  

    Once you've untarred the files, you wind up with a set of 
    text files on your machine, which you can view with your 
    favorite text editor.  To run the code, simply cut-and-paste 
    the program text into other text files (aka modules), or
    Python's interactive command line; see chapter 1 for details.

Why unix and dos directories?

    The "unix" and "dos" directories contain identical data, but
    files on the "unix" branch have UNIX-style end-of-line, and
    "dos" branch files have the MS-DOS end-of-line.  Either form
    can sometimes look odd when edited on the other kind of platform,
    so we provided both as a convenience.  If you don't know what the
    difference is, just use the version that looks best on your 
    platform and text editor.

What's in the text files?

    Within the "examples" and "solutions" subdirectories, you'll 
    find one text file per chapter.  For example:

        lpython/unix/examples/chapter1.txt
        lpython/unix/examples/chapter2.txt
        lpython/unix/examples/chapter3.txt

    and so on.  In the "solutions" directory, the per-chapter text
    files contain code snippets labeled with exercise numbers, and
    correspond to the items in appendix C.  In "examples", the code
    snippets are labeled with the page number they appear on or near.
    Some code listings are from interactive sessions; to run them 
    yourself, cut and paste all but the ">>>" or "..." prompts.

Other hints

    All of the above will make more sense once you start poking 
    around the source files.  And remember, be sure to see the 
    resources listed in the Preface of the book for updates and
    book-related contact points.
