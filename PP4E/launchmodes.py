"""
###################################################################################
launch Python programs with command lines and reusable launcher scheme classes;
auto inserts "python" and/or path to Python executable at front of command line;
some of this module may assume 'python' is on your system path (see Launcher.py);

subprocess module would work too, but os.popen() uses it internally, and the goal
is to start a program running independently here, not to connect to its streams;
multiprocessing module also is an option, but this is command-lines, not functions:
doesn't make sense to start a process which would just do one of the options here;

new in this edition: runs script filename path through normpath() to change any
/ to \ for Windows tools where required; fix is inherited by PyEdit and others;
on Windows, / is generally allowed for file opens, but not by all launcher tools;
###################################################################################
"""

import sys
import os
pyfile = (sys.platform[:3] == 'win' and 'python.exe') or 'python'
pypath = sys.executable     # use sys in newer pys


def fixWindowsPath(cmdline):
    """
    change all / to \ in script filename path at front of cmdline;
    used only by classes which run tools that require this on Windows;
    on other platforms, this does not hurt (e.g., os.system on Unix);
    """
    splitline = cmdline.lstrip().split(' ')           # split on spaces
    fixedpath = os.path.normpath(splitline[0])        # fix forward slashes
    return ' '.join([fixedpath] + splitline[1:])      # put it back together


class LaunchMode:

    """
    on call to instance, announce label and run command;
    subclasses format command lines as required in run();
    command should begin with name of the Python script
    file to run, and not with "python" or its full path;
    """

    def __init__(self, label, command):
        self.what = label
        self.where = command

    # on call, ex: button press callback
    def __call__(self):
        self.announce(self.what)
        self.run(self.where)                # subclasses must define run()

    # subclasses may redefine announce()
    def announce(self, text):
        print(text)                         # methods instead of if/elif logic

    def run(self, cmdline):
        assert False, 'run must be defined'


class System(LaunchMode):

    """
    run Python script named in shell command line
    caveat: may block caller, unless & added on Unix
    """

    def run(self, cmdline):
        cmdline = fixWindowsPath(cmdline)
        os.system('%s %s' % (pypath, cmdline))


class Popen(LaunchMode):

    """
    run shell command line in a new process
    caveat: may block caller, since pipe closed too soon
    """

    def run(self, cmdline):
        cmdline = fixWindowsPath(cmdline)
        os.popen(pypath + ' ' + cmdline)           # assume nothing to be read


class Fork(LaunchMode):

    """
    run command in explicitly created new process
    for Unix-like systems only, including cygwin
    """

    def run(self, cmdline):
        assert hasattr(os, 'fork')
        cmdline = cmdline.split()                  # convert string to list
        if os.fork() == 0:                         # start new child process
            os.execvp(pypath, [pyfile] + cmdline)  # run new program in child


class Start(LaunchMode):

    """
    run command independent of caller
    for Windows only: uses filename associations
    """

    def run(self, cmdline):
        assert sys.platform[:3] == 'win'
        cmdline = fixWindowsPath(cmdline)
        os.startfile(cmdline)


class StartArgs(LaunchMode):

    """
    for Windows only: args may require real start
    forward slashes are okay here
    """

    def run(self, cmdline):
        assert sys.platform[:3] == 'win'
        os.system('start ' + cmdline)              # may create pop-up window


class Spawn(LaunchMode):

    """
    run python in new process independent of caller
    for Windows or Unix; use P_NOWAIT for dos box;
    forward slashes are okay here
    """

    def run(self, cmdline):
        os.spawnv(os.P_DETACH, pypath, (pyfile, cmdline))


class Top_level(LaunchMode):

    """
    run in new window, same process
    tbd: requires GUI class info too
    """

    def run(self, cmdline):
        assert False, 'Sorry - mode not yet implemented'

#
# pick a "best" launcher for this platform
# may need to specialize the choice elsewhere
#

if sys.platform[:3] == 'win':
    PortableLauncher = Spawn
else:
    PortableLauncher = Fork


class QuietPortableLauncher(PortableLauncher):

    def announce(self, text):
        pass


def selftest():
    file = 'echo.py'
    raw_input('default mode...')
    launcher = PortableLauncher(file, file)
    launcher()                                             # no block

    raw_input('system mode...')
    System(file, file)()                                   # blocks

    if sys.platform[:3] == 'win':
        raw_input('DOS start mode...')                         # no block
        StartArgs(file, file)()

if __name__ == '__main__':
    selftest()
