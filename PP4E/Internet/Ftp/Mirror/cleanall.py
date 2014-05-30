#!/usr/bin/env python
"""
##############################################################################
extend the FtpTools class to delete files and subdirectories from a remote
directory tree; supports nested directories too;  depends on the dir()
command output format, which may vary on some servers! - see Python's
Tools\Scripts\ftpmirror.py for hints;  extend me for remote tree downloads;
##############################################################################
"""

from ftptools import FtpTools

class CleanAll(FtpTools):
    """
    delete an entire remote tree of subdirectories
    """
    def __init__(self):
        self.fcount = self.dcount = 0

    def getlocaldir(self):
        return None  # irrelevent here

    def getcleanall(self):
        return True  # implied here

    def cleanDir(self):
        """
        for each item in current remote directory,
        del simple files, recur into and then del subdirectories
        the dir() ftp call passes each line to a func or method
        """
        lines = []                                   # each level has own lines
        self.connection.dir(lines.append)            # list current remote dir
        for line in lines:
            parsed  = line.split()                   # split on whitespace
            permiss = parsed[0]                      # assume 'drw... ... filename'
            fname   = parsed[-1]
            if fname in ('.', '..'):                 # some include cwd and parent
                continue
            elif permiss[0] != 'd':                  # simple file: delete
                print('file', fname)
                self.connection.delete(fname)
                self.fcount += 1
            else:                                    # directory: recur, del
                print('directory', fname)
                self.connection.cwd(fname)           # chdir into remote dir
                self.cleanDir()                      # clean subdirectory
                self.connection.cwd('..')            # chdir remote back up
                self.connection.rmd(fname)           # delete empty remote dir
                self.dcount += 1
                print('directory exited')

if __name__ == '__main__':
    ftp = CleanAll()
    ftp.configTransfer(site='learning-python.com', rdir='training', user='lutz')
    ftp.run(cleanTarget=ftp.cleanDir)
    print('Done:', ftp.fcount, 'files and', ftp.dcount, 'directories cleaned.')
