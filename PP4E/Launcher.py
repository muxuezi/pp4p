#!/usr/bin/python3
"""
==========================================================================
Tools to find files, and run Python demos even if your environment has
not been manually configured yet.  For instance, provided you have already
installed Python, you can launch Tkinter GUI demos directly from the book's
examples distribution tree by double-clicking this file's icon, without
first changing your environment configuration.

Assumes Python has been installed first (double-click on the python self
installer on Windows), and tries to find where Python and the examples
distribution live on your machine.  Sets Python module and system search
paths before running scripts: this only works because env settings are
inherited by spawned programs on both Windows and Linux.

You may want to edit the list of directories searched for speed, and will
probably want to configure your PYTHONPATH eventually to avoid this
search.  This script is friendly to already-configured path settings,
and serves to demo platform-independent directory path processing.
Python programs can always be started under the Windows port by clicking
(or spawning a 'start' DOS command), but many book examples require the
module search path too for cross-directory package imports.
==========================================================================
"""

# Python 3.3 on Windows hack: requires python3 in #! line for
# standalone runs, else this file's own code may use 2.X default
# unless PY_PYTHON set in shell (caveat: portability to Unix?);

import sys, os
try:
    PyInstallDir = os.path.dirname(sys.executable)
except:
    PyInstallDir = r'C:\Python31'      # for searches, set for older pythons
BookExamplesFile = 'README-PP4E.txt'   # for pythonpath configuration

# Python 3.3 hack: set new Windows launcher's default to 3.X for any
# spawnees of spawnees (programs spawed here bypass "py" launcher)
if sys.platform.startswith('win'):
    os.environ['PY_PYTHON'] = '3'

def which(program, trace=True):
    """
    Look for program in all dirs in the system's search
    path var, PATH; return full path to program if found,
    else None. Doesn't handle aliases on Unix (where we
    could also just run a 'which' shell cmd with os.popen),
    and it might help to also check if the file is really
    an executable with os.stat and the stat module, using
    code like this: os.stat(filename)[stat.ST_MODE] & 0111
    """
    try:
        ospath = os.environ['PATH']
    except:
        ospath = '' # OK if not set
    systempath = ospath.split(os.pathsep)
    if trace: print('Looking for', program, 'on', systempath)

    for sysdir in systempath:
        filename = os.path.join(sysdir, program)      # adds os.sep between
        if os.path.isfile(filename):                  # exists and is a file?
            if trace: print('Found', filename)
            return filename
        else:
            if trace: print('Not at', filename)
    if trace: print(program, 'not on system path')
    return None


def findFirst(thisDir, targetFile, trace=False):
    """
    Search directories at and below thisDir for a file
    or dir named targetFile.  Like find.find in standard
    lib, but no name patterns, follows Unix links, and
    stops at the first file found with a matching name.
    targetFile must be a simple base name, not dir path.
    could also use os.walk or PP4E.Tools.find to do this.
    """
    if trace: print('Scanning', thisDir)
    for filename in os.listdir(thisDir):                    # skip . and ..
        if filename in [os.curdir, os.pardir]:              # just in case
            continue
        elif filename == targetFile:                        # check name match
            return os.path.join(thisDir, targetFile)        # stop at this one
        else:
            pathname = os.path.join(thisDir, filename)      # recur in subdirs
            if os.path.isdir(pathname):                     # stop at 1st match
                below = findFirst(pathname, targetFile, trace)
                if below: return below


def guessLocation(file, isOnWindows=(sys.platform[:3]=='win'), trace=True):
    """
    Try to find directory where file is installed
    by looking in standard places for the platform.
    Change tries lists as needed for your machine.
    """
    cwd = os.getcwd()                             # directory where py started
    tryhere = cwd + os.sep + file                 # or os.path.join(cwd, file)
    if os.path.exists(tryhere):                   # don't search if it is here
        return tryhere                            # findFirst(cwd,file) descends

    if isOnWindows:
        tries = []
        for pydir in [PyInstallDir]:
            if os.path.exists(pydir):
                tries.append(pydir)
        tries = tries + [cwd, r'C:\Program Files']
        for drive in 'CDEFG':
            tries.append(drive + ':\\')
    else:
        tries = [cwd, os.environ['HOME'], '/usr/bin', '/usr/local/bin']

    for dir in tries:
        if trace: print('Searching for %s in %s' % (file, dir))
        try:
            match = findFirst(dir, file)
        except OSError:
            if trace: print('Error while searching', dir)    # skip bad drives
        else:
            if match: return match
    if trace: print(file, 'not found! - configure your environment manually')
    return None


PP4EpackageRoots = [                               # python module search path
   #'%sPP4E' % os.sep,                             # pass in your own elsewhere
    '']                                            # '' adds examplesDir root


def configPythonPath(examplesDir, packageRoots=PP4EpackageRoots, trace=True):
    """
    Set up the Python module import search-path directory
    list as necessary to run programs in the book examples
    distribution, in case it hasn't been configured already.
    Add examples package root + any nested package roots
    that imports are relative to (just top root currently).

    os.environ assignments call os.putenv internally in 1.5+,
    so these settings will be inherited by spawned programs.
    Python source lib dir and '.' are automatically searched;
    unix|win os.sep is '/' | '\\', os.pathsep is ':' | ';'.
    sys.path is for this process only--must set os.environ.
    adds new dirs to front, in case there are two installs.
    """
    try:
        ospythonpath = os.environ['PYTHONPATH']
    except:
        ospythonpath = '' # OK if not set
    if trace: print('PYTHONPATH start:\n', ospythonpath)

    addList = []
    for root in packageRoots:
        importDir = examplesDir + root
        if importDir in sys.path:
            if trace: print('Exists', importDir)
        else:
            if trace: print('Adding', importDir)
            sys.path.append(importDir)
            addList.append(importDir)

    if addList:
        addString = os.pathsep.join(addList) + os.pathsep
        os.environ['PYTHONPATH'] = addString + ospythonpath
        if trace: print('PYTHONPATH updated:\n', os.environ['PYTHONPATH'])
    else:
        if trace: print('PYTHONPATH unchanged')


def configSystemPath(pythonDir, trace=True):
    """
    Add python executable dir to system search path if needed
    """
    try:
        ospath = os.environ['PATH']
    except:
        ospath = '' # OK if not set
    if trace: print('PATH start:\n', ospath)

    if ospath.lower().find(pythonDir.lower()) == -1:            # not found?
        os.environ['PATH'] = ospath + os.pathsep + pythonDir    # not case diff
        if trace: print('PATH updated:\n', os.environ['PATH'])
    else:
        if trace: print('PATH unchanged')


def runCommandLine(pypath, exdir, command, isOnWindows=False, trace=True):
    """
    Run python command as an independent program/process on
    this platform, using pypath as the Python executable,
    and exdir as the installed examples root directory.

    Need full path to Python on Windows, but not on Unix.
    On Windows, an os.system('start ' + command) is similar,
    except that .py files pop up a DOS console box for I/O.
    Could use launchmodes.py too but pypath is already known.
    """
    command = exdir + os.sep + command          # rooted in examples tree
    command = os.path.normpath(command)         # fix up mixed slashes
    os.environ['PP4E_PYTHON_FILE'] = pypath     # export directories for
    os.environ['PP4E_EXAMPLE_DIR'] = exdir      # use in spawned programs

    if trace: print('Spawning:', command)
    if isOnWindows:
        os.spawnv(os.P_DETACH, pypath, ('python', command))
    else:
        cmdargs = [pypath] + command.split()
        if os.fork() == 0:
            os.execv(pypath, cmdargs)           # run prog in child process


def launchBookExamples(commandsToStart, trace=True):
    """
    Toplevel entry point: find python exe and examples dir,
    configure environment, and spawn programs.  Spawned
    programs will inherit any configurations made here.
    """
    isOnWindows  = (sys.platform[:3] == 'win')
    pythonFile   = (isOnWindows and 'python.exe') or 'python'   # or if/esle
    if trace:
        print(os.getcwd(), os.curdir, os.sep, os.pathsep)
        print('starting on %s...' % sys.platform)

    # find python executable: check system path, then guess
    try:
        pypath = sys.executable     # python executable running me
    except:
        # on older pythons
        pypath = which(pythonFile) or guessLocation(pythonFile, isOnWindows)
    assert pypath
    pydir, pyfile = os.path.split(pypath)               # up 1 from file
    if trace:
        print('Using this Python executable:', pypath)
        input('Press <enter> key')

    # find examples root dir: check cwd and others
    expath = guessLocation(BookExamplesFile, isOnWindows)
    assert expath
    updir  = expath.split(os.sep)[:-2]                  # up 2 from file
    exdir  = os.sep.join(updir)                         # to PP4E pkg parent
    if trace:
        print('Using this examples root directory:', exdir)
        input('Press <enter> key')

    # export python and system paths if needed
    configSystemPath(pydir)
    configPythonPath(exdir)
    if trace:
        print('Environment configured')
        input('Press <enter> key')

    # spawn programs: inherit configs
    for command in commandsToStart:
        runCommandLine(pypath, os.path.dirname(expath), command, isOnWindows)


if __name__ == '__main__':
    #
    # if no args, spawn all in the list of programs below
    # else rest of cmd line args give single cmd to be spawned
    #
    if len(sys.argv) == 1:
        commandsToStart = [
            'Gui/TextEditor/textEditor.py',         # either slash works
            'Lang/Calculator/calculator.py',        # launcher normalizes path
            'PyDemos.pyw',
           #'PyGadgets.py',
            'echoEnvironment.pyw'
        ]
    else:
        commandsToStart = [ ' '.join(sys.argv[1:]) ]
    launchBookExamples(commandsToStart)
    if sys.platform[:3] == 'win':
        input('Press Enter') # to read msgs if clicked
