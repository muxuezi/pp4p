------------------------------------------------------------------------------
PP4E\README-PP4E.txt
Examples distribution package for _Programming Python, 4th Edition_

**Do not move this file: the Launcher.py auto-launcher tools use it
**to find the examples root, in order to set the module search path.

This file provides usage details for this package, especially its 
demo launcher scripts.  It's intended to provide extra details for
people who are relatively new to Python and configuration details.

Please also see the files:

    ..\README.txt 
    .\__init__.py 

for additional example tree documentation.



------------------------------------------------------------------------------
1. Running Program Demos Quick Start: Self-Launcher Scripts
------------------------------------------------------------------------------

If you want to see some Python demos right away, and have access
to an installed Python with the tkinter extension, you can run
one of the following demo scripts immediately:

    Launch_PyDemos.pyw          (starts the main demo laucher bar)
    Launch_PyGadgets_bar.pyw    (starts a utilities launcher toolbar)
    LaunchBrowser.py            (opens examples index in web browser)

These scripts only require that Python is installed first.  You don't
need to configure your environment first to run them, and they may be 
run from within the example package directly.  LaunchBrowser will work
if it can find a web browser on your machine, even if you don't have a 
live Internet link (though some Internet examples' features won't work
completely without a connection).

Depending on your platform, you can start the scripts above by either:

(1) Double-clicking on the scripts' file names in your file explorer, or
(2) Running the scripts from your system command-line prompt.

The first technique is usually easiest; since Python automatically 
registers itself to open ".py" and ".pyw" Python files when installed
on Windows, it just works.  To use the second scheme:

- Start a system command-line shell interface (e.g. a MS-DOS command
  console box known as Command Prompt on Windows, an xterm or terminal
  window on Linux, Unix, and Macs)

- At the command-line prompt, go to the PP4E examples directory where 
  the files reside (e.g., type  a "cd C:\MyExamplesdir\PP4E" command)

- At the command-line prompt, type one of the following commands:

    python Launch_PyDemos.pyw
    python Launch_PyGadgets_bar.pyw
    python LaunchBrowser.py

You may need to replace 'python' with the full path to your Python
program if it is not in a directory already on your PATH setting (for
3.1, it is probably at C:\Python31\python on Windows).

Both of these Launch_* scripts are self-configuring.  They assume that 
you have already installed Python (they're written in Python, afterall), 
but they automatically locate your Python program and examples root 
directory, and configure the Python module and system search paths as 
needed to run the book examples.  The Launch scripts should work both 
straight off the example package, or after copying the examples directory
to your hard drive (which you'll want to do eventually to make changes,
and allow Python to save bytecode files if the package is on CD).
See comments in file Launcher.py for more details.



------------------------------------------------------------------------------
2. The Quick Guide to Installing Python
------------------------------------------------------------------------------

To run Python demos on your machine, you first need a Python interpreter.
On Windows, if there is no Python on your computer (check the Programs
entry in your Start button), there is a fully executable Python with Tk GUI 
support available at www.python.org.  It's packaged as a self-installer
program (a ".msi"  installer today), so it's essentially just a double-click
to install.  In more detail, here is the Python installation procedure: 

(1) Fetch the Windows installer for Python 3.X at the "Downloads" like at 
    www.python.org; for the 3.1 releases, it's a ".msi" self-installer.

(2) Navigate to the downloaded installer file, unless your browser prompts
    you to open it immediately after the download. 

(3) Open the installer, or double-click on the "*.msi" file you fetched
    (the self-install program)

(4) Answer 'yes', 'next', 'default', 'continue', or "I confess..." to all
    the questions you will be asked while the installer runs (that is, a 
    default install). Tk GUI support is automaticaly installed along with Python.

Once that's finished, you have a Python on your machine; you can tell because
there will be Python intry in the programs menu in your Start button.  Now,
go click on the Launch_PyDemos.pyw file icon in the example package's 
top-level Examples\PP4E directory to start some Python demos right away.
When you're ready, read on in this file to find out how to configure your
environment permanently, for faster start-ups.

On Mac OS X, UNIX and Linux, you probably already have a Python 
installed (it comes standard on Macs and most Linux), but you can also
install Python from Linux RPM files, or build Python from its source code 
packages available at www.python.org.  To build from the source, ungzip,
untar, config, and make.  LInux users: if your Python does not have Tk
GUI support preinstalled, try a "yum tkinter" command to fetch it.

Note that as I write these words, most Mac OS X and Linux machines, as 
well as the Cygwin package on Windows, still have Python 2.X.  Until they
are updated, you'll need to get and install a 3.X version of Python to run 
this book's 3.1 examples; see www.python.org or your favorite web search
engine for details.  On Unix-like systems, Python 3.X can be built from 
its cource-code distribution; this is how I got it to work in Cygwin on
Windows (which was also shipping Python 2.5 at the time).
 
Also note that although the book's examples were verified to run under 
Python 3.1, the latest Python is generally the best Python: you can 
always fetch the current release from www.python.org.  If newer Python
releases break examples over time, patches or updates will be posted at
the book's update pages, and may find there way ibnto this examples 
distribution package over time.



------------------------------------------------------------------------------
3. Running Program Demo Launchers Manually
------------------------------------------------------------------------------

You can also run the demo scripts by typing these command lines, after 
adding the directory containing the PP4E root to your module search path,
and cd'ing to the PP4E directory where your example files reside:

    python PyDemos.pyw              (start main demo bar interface)
    python PyGadgets_bar.pyw        (start real tools launch bar)
    python PyGadgets.py             ( start real tools immediately)

The advantage of this scheme is that it avoids the automatic search and 
configuration steps performed by the Launch_* scripts mentioned earlier,
and so may start a bit faster.  The self-launcher sctips run these files
automatically, after setting up your Python and system search paths.

PyDemos starts an interface from which you can run many of the 
larger GUI-based examples that appear in the book.  Since most 
of the examples are scattered throughout the PP4E subdirectories,
this file also serves as a quick locator for major GUI examples.
In its current version 2, PyDemos also has buttons which pop up 
the source code files for its example programs in text edit windows.

Another top-level script, PyGadgets.py can be started similarly; 
it runs a handful of programs in non-demo mode.  Its relative,
PyGadgets_bar.pyw pops up a button bar to start gadgets on demand.
You can find screen shots of these demo programs in action in
the book's GUI chapters.

The Internet examples on the PyDemos bar are started with the 
LaunchBrowser.py script, which tries to also find a web browser
on your machine (which mostly just uses the standard library's
webbrowser module today); see that script for more details.  
If you start LaunchBrowser.py directly, it brings up the 
PyInternetDemos.html root page by opening a local file on your 
machine.  In general, here are the major top-level programs in 
the PP4E directory:

PyDemos.pyw
    Button bar for starting and viewing major GUI and Web examples 
PyGadgets.py
    Starts programs in non-demo mode for regular use 
PyGadgets_bar.pyw
    Button bar for starting PyGadgets programs on demand 
Launcher.py
    Tools for starting programs without manual environment settings:
    adds Python to PATH, sets PYTHONPATH, spawns Python programs
Launch_*.py*
    Starts PyDemos and PyGadgets with Launcher.py--run these 
    for a quick look without manual configuration
LaunchBrowser.py 
    Opens example web pages with an automatically-located web
    browser, either live on the net, or local web page files

Please note that all of the launcher and demo scripts are written to be
portable, but they have only been tested on a small number of patforms.  
The Tk GUI toolkit many of the demos use also works on the Mac (classic, 
and OSX on both Aqua and X), and Python runs on almost every platform in 
existence.  These scripts may require minor changes on some platforms, 
though, and may need to be configured a bit for unique machine set-ups.

Also note that some of the GUI demos assume that the PIL 3rd-party 
open source extension has been installed (it's included in the "extensions" 
folder in this package,  but can be fetched via a web search); if you 
haven't installed PIL the demo launchers will run, but demos they spawn 
that view or process image files will not.



----------------------------------------------------------------------------
4. More About PyDemos and PyGadgets
------------------------------------------------------------------------------

Among other things, PyDemos lets you start a clock, calculator, image
viewer, drawing tool, text-editor, slideshow, and N-across game, all 
coded in Python.  It also has source code view buttons, and includes 
buttons which attempt to start a web browser and server automatically for
the major Internet example start pages.  See file PyDemos.pyw for more 
details about the launcher, and see the book for more details about the
demo programs.

Depending on your system's configuration, you may also be able to
run the PyDemos.pyw file by double-clicking on it in your system's
file browser, provided the PP4E is contained in a directory on the 
module search path (see below).  

To make the demos easily accessible, you can also drag out a 
double-clickable shortcut to PyDemos.pyw (or Launch_PyDemos.pyw) onto
your Windows desktop; shortcuts work on other platforms as well, though
this is very platform specific.  The PyGadgets script starts a subset 
of the programs the PyDemos can; PyGadgets starts programs for real use,
not demonstration.



------------------------------------------------------------------------------
5. More About the Internet Demos
------------------------------------------------------------------------------

If you don't have a Python with Tkinter installed (or don't have 
Python at all, for that matter), you may also run the book's 
browser-based Internet examples.  In this 4th Edition, these examples
are not maintained at a web site, but may be run by launching a web 
server locally on your machine.  See the server-side scripting chapter
in the book for details.  

The PyDemos script attempts to spawn a locally running web server coded
in Python, to handle page requests from a spawned web browser.  To
disable this, see the '-file' and '-live' switches in the script's code.

It is possible to upload the book's web examples to a remote site, 
provided there is a web server there which supports Python 3.X-coded 
CGI scripts.  Among other things, the web-based book examples include 
CGI tutorial scripts and an email interface (PyMailCGI, as well as the
PyMailGUI email client). 

Naturally, many examples in the book aren't GUI or browser-based; see 
the text and PP4E directory for additional example files.



------------------------------------------------------------------------------
6. Examples Package Directory Organization
------------------------------------------------------------------------------

The example files in this distribution are organized by major topics
in the book (one directory for Internet code, one for System examples,
and so on).  The subdirectories within each topics directory usually 
correspond to a particular section or chapter in the book (e.g., the
Internet\Sockets directory contains Network Scripting chapter code).
There is also a top-level Tools directory in PP4E, which contains
Python scripts used to manage the entire tree.

Most example tree directories are module packages, to allow qualified
cross-directory imports.  __init__.py files identify a containing 
directory as a Python module package, and so allow it to be listed in a
script's import statements.  In fact, the entire examples distribution 
is one module package, to make it easy for examples to specify modules 
used elsewhere in the book, and to avoid filename clashes with other 
Python code on your system.  

In general, imports in all examples either refer to a file in the same 
directory as the importer, or are fully-qualified package import paths 
rooted at PP4E.  For instance, if an example in PP4E\Integrate\Extend
uses a module defined in PP4E\Gui, it runs an import of one of these 
forms --  within PP4E\Integrate\Extend\somefile.py:

    import PP4E.Gui.somemodule
    from   PP4E.Gui.somemodule import name

Your code outside the examples tree can do likewise to reuse example code.
No book tree directories other than PP4E need be added to the module search
path setting (e.g., PYTHONPATH, ".pth" files).  This is by design: although 
adding nested subdirectories may allow simpler imports like:

    import Gui.somemodule
    import somemodule

this would also cause potential name clashes if you install another 
package with a "Gui" package directory or "somemodule" name--either the 
book examples or that other package would find the wrong code.  This 
would also make the search path, and its configuration, more complex.

By placing all book examples under the PP4E directory, and making all
cross-directory imports relative to this root, such module name clashes
are avoided.  Because of this structure, the examples directory is fairly
self-contained; the PP4E root makes imported names unique, ensures that
imports of PP4E are accurate, and avoids the pitfalls of directory moves 
when package-relative imnports ("from . import M)" are used.  Relative 
imports assume much about the sructure of source trees; the same case
can be made about package imports, but paths are at least more explicit.

For this to work, though, the module search path must generally include
the name of the directory containing the PP4E directory.  See the next
section for hints on setting this up.

See also file ..\README.txt (that is, in the parent directoy of PP4E)
for more details on Python package imports.



------------------------------------------------------------------------------
7. Configuration Details
------------------------------------------------------------------------------

Because the PP4E examples directory is used as a module package library 
by various programs, you will eventually want to set your PYTHONPATH (or 
".pth" file entries) to find it correctly in the module search path.  

Change your module search path to include the directory containing the 
PP4E examples directory.  This adds only one directory to PYTHONPATH (the
one containing PP4E).  You dont need to do this to run the self-launcher
Launch_* scripts, but will in order to run some other examples directly,
or import example file code into your own programs.

Please see the text Learning Python (or other resources) for details 
on setting your PYTHONPATH environment variable or ".pth" files.  On 
Windows, the Control Panel/System icon provides a GUI for this; on
Unix-like macines, you'll typically set this in your .login, .chsrc, 
or similar start-up file.

Under Jython, the Java implementation of Python, the module search path 
may take different forms (e.g., command-line arguments, assignments in 
Java registry files). See Jython documentation for more details, as this
is prone to change over time.  Other alternate implementations such as
IronPython for .NET may have unique configuration options as well.

You may also wish to configure the system search path (used to find the 
Python executable in command lines), using similar techniques.  If not
set, you may have to type the full path to Python in command lines.



------------------------------------------------------------------------------
8. Updates
------------------------------------------------------------------------------

Watch for updates, supplements, and patches, at this site:

    http://www.rmi.net/~lutz/about-pp4e.html          (current)

The following alternate site will be used if the preceding ever fails:

    http://learning-python.com/books/about-pp4e.html  (alternate)

O'Reilly's page for this book will also track book errata:

    http://www.oreilly.com    (look for the Python books page)

Changes to this examples distribution package for bugs, enhancements,
or changes required for new Python releases, may also be logged in 
the changes\CHANGES.txt files two level up in this tree, if present.

Happy Pythoneering,
--Mark Lutz, Summer 2010 (updated November 2010)

