"""
###############################################################
launch FTP putfile function with a reusable form GUI class;
see getfilegui for notes: most of the same caveats apply;
the get and put forms have been factored into a single
class such that changes need be made in only one place;
###############################################################
"""

from tkinter import mainloop
import putfile, getfilegui

class FtpPutfileForm(getfilegui.FtpForm):
    title = 'FtpPutfileGui'
    mode  = 'Upload'
    def do_transfer(self, filename, servername, remotedir, userinfo):
        putfile.putfile(filename, servername, remotedir, userinfo, verbose=False)

if __name__ == '__main__':
    FtpPutfileForm()
    mainloop()
