#!/usr/bin/env python
"""
##############################################################################
use FTP to download or upload all files in a single directory from/to a
remote site and directory;  this version has been refactored to use classes
and OOP for namespace and a natural structure;  we could also structure this
as a download superclass, and an upload subclass which redefines the clean
and transfer methods, but then there is no easy way for another client to
invoke both an upload and download;  for the uploadall variant and possibly
others, also make single file upload/download code in orig loops methods;
##############################################################################
"""

import os, sys, ftplib
from getpass   import getpass
from mimetypes import guess_type, add_type

# defaults for all clients
dfltSite = 'home.rmi.net'
dfltRdir = '.'
dfltUser = 'lutz'

class FtpTools:

    # allow these 3 to be redefined
    def getlocaldir(self):
        return (len(sys.argv) > 1 and sys.argv[1]) or '.'

    def getcleanall(self):
        return input('Clean target dir first?')[:1] in ['y','Y']

    def getpassword(self):
        return getpass(
               'Password for %s on %s:' % (self.remoteuser, self.remotesite))

    def configTransfer(self, site=dfltSite, rdir=dfltRdir, user=dfltUser):
        """
        get upload or download parameters
        from module defaults, args, inputs, cmdline
        anonymous ftp: user='anonymous' pass=emailaddr
        """
        self.nonpassive = False             # passive FTP on by default in 2.1+
        self.remotesite = site              # transfer to/from this site
        self.remotedir  = rdir              # and this dir ('.' means acct root)
        self.remoteuser = user
        self.localdir   = self.getlocaldir()
        self.cleanall   = self.getcleanall()
        self.remotepass = self.getpassword()

    def isTextKind(self, remotename, trace=True):
        """
        use mimetypes to guess if filename means text or binary
        for 'f.html,   guess is ('text/html', None): text
        for 'f.jpeg'   guess is ('image/jpeg', None): binary
        for 'f.txt.gz' guess is ('text/plain', 'gzip'): binary
        for unknowns,  guess may be (None, None): binary
        mimetypes can also guess name from type: see PyMailGUI
        """
        add_type('text/x-python-win', '.pyw')                    # not in tables
        mimetype, encoding = guess_type(remotename, strict=False)# allow extras
        mimetype  = mimetype or '?/?'                            # type unknown?
        maintype  = mimetype.split('/')[0]                       # get 1st part
        if trace: print(maintype, encoding or '')
        return maintype == 'text' and encoding == None           # not compressed

    def connectFtp(self):
        print('connecting...')
        connection = ftplib.FTP(self.remotesite)           # connect to FTP site
        connection.login(self.remoteuser, self.remotepass) # log in as user/pswd
        connection.cwd(self.remotedir)                     # cd to dir to xfer
        if self.nonpassive:                                # force active mode
            connection.set_pasv(False)                     # most do passive
        self.connection = connection

    def cleanLocals(self):
        """
        try to delete all local files first to remove garbage
        """
        if self.cleanall:
            for localname in os.listdir(self.localdir):    # local dirlisting
                try:                                       # local file delete
                    print('deleting local', localname)
                    os.remove(os.path.join(self.localdir, localname))
                except:
                    print('cannot delete local', localname)

    def cleanRemotes(self):
        """
        try to delete all remote files first to remove garbage
        """
        if self.cleanall:
            for remotename in self.connection.nlst():       # remote dir listing
                try:                                        # remote file delete
                    print('deleting remote', remotename)
                    self.connection.delete(remotename)
                except:
                    print('cannot delete remote', remotename)

    def downloadOne(self, remotename, localpath):
        """
        download one file by FTP in text or binary mode
        local name need not be same as remote name
        """
        if self.isTextKind(remotename):
            localfile = open(localpath, 'w', encoding=self.connection.encoding)
            def callback(line): localfile.write(line + '\n')
            self.connection.retrlines('RETR ' + remotename, callback)
        else:
            localfile = open(localpath, 'wb')
            self.connection.retrbinary('RETR ' + remotename, localfile.write)
        localfile.close()

    def uploadOne(self, localname, localpath, remotename):
        """
        upload one file by FTP in text or binary mode
        remote name need not be same as local name
        """
        if self.isTextKind(localname):
            localfile = open(localpath, 'rb')
            self.connection.storlines('STOR ' + remotename, localfile)
        else:
            localfile = open(localpath, 'rb')
            self.connection.storbinary('STOR ' + remotename, localfile)
        localfile.close()

    def downloadDir(self):
        """
        download all files from remote site/dir per config
        ftp nlst() gives files list, dir() gives full details
        """
        remotefiles = self.connection.nlst()         # nlst is remote listing
        for remotename in remotefiles:
            if remotename in ('.', '..'): continue
            localpath = os.path.join(self.localdir, remotename)
            print('downloading', remotename, 'to', localpath, 'as', end=' ')
            self.downloadOne(remotename, localpath)
        print('Done:', len(remotefiles), 'files downloaded.')

    def uploadDir(self):
        """
        upload all files to remote site/dir per config
        listdir() strips dir path, any failure ends script
        """
        localfiles = os.listdir(self.localdir)       # listdir is local listing
        for localname in localfiles:
            localpath = os.path.join(self.localdir, localname)
            print('uploading', localpath, 'to', localname, 'as', end=' ')
            self.uploadOne(localname, localpath, localname)
        print('Done:', len(localfiles), 'files uploaded.')

    def run(self, cleanTarget=lambda:None, transferAct=lambda:None):
        """
        run a complete FTP session
        default clean and transfer are no-ops
        don't delete if can't connect to server
        """
        self.connectFtp()
        cleanTarget()
        transferAct()
        self.connection.quit()

if __name__ == '__main__':
    ftp = FtpTools()
    xfermode = 'download'
    if len(sys.argv) > 1:
        xfermode = sys.argv.pop(1)   # get+del 2nd arg
    if xfermode == 'download':
        ftp.configTransfer()
        ftp.run(cleanTarget=ftp.cleanLocals,  transferAct=ftp.downloadDir)
    elif xfermode == 'upload':
        ftp.configTransfer(site='learning-python.com', rdir='books', user='lutz')
        ftp.run(cleanTarget=ftp.cleanRemotes, transferAct=ftp.uploadDir)
    else:
        print('Usage: ftptools.py ["download" | "upload"] [localdir]')
