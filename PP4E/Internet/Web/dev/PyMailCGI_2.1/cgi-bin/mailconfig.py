###############################################################################
# user configuration settings for various email programs (PyMailCGI version);
# email scripts get their server names and other email config options from
# this module: change me to reflect your machine names, sig, and preferences;
###############################################################################

#------------------------------------------------------------------------------
# (required for load, delete) POP3 email server machine, user 
#------------------------------------------------------------------------------

# popservername = '?Please set your mailconfig.py attributes?'

popservername  = 'pop.earthlink.net'       # or starship.python.net, 'localhost'
popusername    = 'pp3e'                    # password fetched or asked when run

#------------------------------------------------------------------------------
# (required for send) SMTP email server machine name
# see Python smtpd module for a smtp server class to run locally
# note: your isp may require that you be directy connected to their system:
# I can email through earthlink on dialup, but cannot via comcast cable
#------------------------------------------------------------------------------

smtpservername = 'smtp.comcast.net'     # or 'smtp.mindspring.com', 'localhost' 

#------------------------------------------------------------------------------
# (may be required for send) SMTP user/password if authenticated
# set user to None or '' if no login/authenticaion is required
# set pswd to name of a file holding your smtp password, or an
# empty string to force programs to ask (in a console, or gui)
#------------------------------------------------------------------------------

smtpuser  = None                           # per your isp
smtppasswdfile  = ''                       # set to '' to be asked

#------------------------------------------------------------------------------
# (optional) PyMailGUI: name of local one-line text file with your pop
# password; if empty or file cannot be read, pswd is requested when first
# connecting; pswd not encrypted: leave this empty on shared machines;
# PyMailCGI always asks for pswd (runs on a possibly remote server);
#------------------------------------------------------------------------------

poppasswdfile  = r'c:\temp\pymailgui.txt'      # set to '' to be asked

#------------------------------------------------------------------------------
# (optional) personal information used by PyMailGui to fill in edit forms;
# if not set, does not fill in initial form values;
# sig  -- can be a triple-quoted block, ignored if empty string;
# addr -- used for initial value of "From" field if not empty,
# no longer tries to guess From for replies--varying success;
#------------------------------------------------------------------------------

myaddress   = 'pp3e@earthlink.net'
mysignature = '--Mark Lutz  (http://www.rmi.net/~lutz)'

#------------------------------------------------------------------------------
# (optional) local file where sent messages are saved;
# PyMailGUI 'Open' button allows this file to be opened and viewed
#------------------------------------------------------------------------------

sentmailfile   = r'.\sentmail.txt'             # . means in current working dir

#------------------------------------------------------------------------------
# (optional) local file where pymail saves pop mail;
# PyMailGUI insead asks for a name with a popup dialog
#------------------------------------------------------------------------------

savemailfile   = r'c:\temp\savemail.txt'       # not used in PyMailGui: dialog

#------------------------------------------------------------------------------
# (optional) customize headers displayed in PyMailGUI list and view windows;
# listheaders replaces default, viewheaders extends it; both must be tuple of
# strings, or None to use default hdrs;
#------------------------------------------------------------------------------

listheaders = ('Subject', 'From', 'Date', 'To', 'X-Mailer')
viewheaders = ('Bcc',)

#------------------------------------------------------------------------------
# (optional) PyMailGUI fonts and colors for text server/file message list
# windows, and message content view windows; use ('family', size, 'style') for
# font; 'colorname' or hexstr '#RRGGBB' for color (background, foreground);
# set to None to accept defaults;  font/color of message view windows can
# also be set interactively with the texteditor's Tools menu;
#------------------------------------------------------------------------------

listbg   = 'indianred'         # None, 'white', '#RRGGBB' (see setcolor example)
listfg   = 'black'
listfont = ('courier', 9, 'bold')       # None, ('courier', 12, 'bold italic')
                                        # use fized-width font for list columns
viewbg   = '#dbbedc'
viewfg   = 'black'
viewfont = ('courier', 10, 'bold')

# see Tk color names: aquamarine paleturqoise powderblue goldenrod burgundy ....

#listbg = listfg = listfont = None
#viewbg = viewfg = viewfont = None      # to use defaults


#------------------------------------------------------------------------------
# (optional) column at which mail's original text should be wrapped for view,
# reply, and forward;  wraps at first delimiter to left of this position;
# composed text is not auto-wrapped: user or recipient's mail tool must wrap
# new text if desired; to disable wrapping, set this to a high value (1024?);
#------------------------------------------------------------------------------

wrapsz = 100

#end
