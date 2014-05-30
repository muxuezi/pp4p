"""
################################################################################
PyMailGUI user configuration settings.

Email scripts get their server names and other email config options from
this module: change me to reflect your machine names, sig, and preferences.
This module also specifies some widget style preferences applied to the GUI,
as well as message Unicode encoding policy and more in version 3.0.  See
also: local textConfig.py, for customizing PyEdit pop-ups made by PyMailGUI. 

Warning: PyMailGUI won't run without most variables here: make a backup copy!
Caveat: somewhere along the way this started using mixed case inconsistently...;
TBD: we could get some user settings from the command line too, and a configure
dialog GUI would be better, but this common module file suffices for now.
################################################################################
"""

#-------------------------------------------------------------------------------
# (required for load, delete) POP3 email server machine, user;
#-------------------------------------------------------------------------------

#popservername = '?Please set your mailconfig.py attributes?'

popservername = 'pop.secureserver.net'             # see altconfigs/ for others
popusername   = 'PP4E@learning-python.com'

#-------------------------------------------------------------------------------
# (required for send) SMTP email server machine name;
# see Python smtpd module for a SMTP server class to run locally ('localhost');
# note: your ISP may require that you be directly connected to their system:
# I once could email through Earthlink on dial up, but not via Comcast cable;
#-------------------------------------------------------------------------------

smtpservername = 'smtpout.secureserver.net'    # default port 25

# see below for more smt options

#-------------------------------------------------------------------------------
# (optional) personal information used by PyMailGUI to fill in edit forms;
# if not set, does not fill in initial form values;
# signature  -- can be a triple-quoted block, ignored if empty string;
# address    -- used for initial value of "From" field if not empty,
# no longer tries to guess From for replies--varying success;
#-------------------------------------------------------------------------------

myaddress   = 'PP4E@learning-python.com'
mysignature = ('Thanks,\n'
               '--Mark Lutz  (http://learning-python.com, http://rmi.net/~lutz)')

#-------------------------------------------------------------------------------
# (may be required for send) SMTP user/password if authenticated;
# set user to None or '' if no login/authentication is required, and set 
# pswd to either the name of a file holding your SMTP password or an empty 
# string to force programs to ask for the password (in a console, or GUI)
#-------------------------------------------------------------------------------

smtpuser  = None                           # per your ISP
smtppasswdfile  = ''                       # set to '' to be asked

#smtpuser = popusername


# Oct 2011, more SMTP options:
#
# updated to use auth smtp port number or broadband server, when my broadband isp
# stopped allowing sends through non-auth godaddy smtp on default port 25; to use 
# a specific smtp port number, simply append it at the end of the server name string
# as here: Python's smtplib automatically parses this off and uses it, and PyMailGUI
# automatically uses authentication and asks for passwords if needed;

# FAILS (after broadband isp change)
smtpservername = 'smtpout.secureserver.net'    # default port 25 

# Godaddy: straight and encrypted and outgoing smtp ports,
# but neither one of these seem to work as advertised

#FAILS
smtpservername = 'smtpout.secureserver.net:587'    # per smtplib.py server parsing
#FAILS (hangs)
smtpservername = 'smtpout.secureserver.net:465'    # SSL encrypted SMTP port

# The next server requires authentication, and uses port 587. Connect using your 
# mailboxname@yourdomain.com as the "username" and the password for that mailbox.
# this worked well in most contexts (e.g., hotels), until later broken at earthlink;

#WORKS (pymailgui asks for pswd once per session on first send)
smtpuser = 'lutz@rmi.net'
smtppasswdfile = ''   # ask: xxxxx
smtpservername = 'smtpauth.hosting.earthlink.net:587'

# Your ISP or local network's outgoing mail server (this is my broadband provider).
# Caveat: there's a chance that sending from rmi.net through mail.mailmt.com will
# trigger a SPF fail and/or be marked as spam; this may also fail on the road?

#WORKS (but may require direct connection?)
smtpuser  = None                           # per your ISP
smtppasswdfile  = ''                       # set to '' to be asked
smtpservername = 'mail.mailmt.com'

# dec2011: comcast xfinity network
# see also: mailconfig.**** in altconfigs dir
smtpuser       = '-CONFIGURE-'                 # nonblank=authenticated
smtppasswdfile = ''                            # '' = ask in GUI
smtpservername = 'smtp.comcast.net:587'        # ssl encrypted port (?)

print('servers:', popservername, smtpservername)


#-------------------------------------------------------------------------------
# (optional) PyMailGUI: name of local one-line text file with your POP
# password; if empty or file cannot be read, pswd is requested when first
# connecting; pswd not encrypted: leave this empty on shared machines;
# PyMailCGI always asks for pswd (runs on a possibly remote server);
#-------------------------------------------------------------------------------

poppasswdfile  = r'c:\temp\pymailgui.txt'      # set to '' to be asked

#-------------------------------------------------------------------------------
# (required) local file where sent messages are always saved;
# PyMailGUI 'Open' button allows this file to be opened and viewed;
# don't use '.' form if may be run from another dir: e.g., pp4e demos
#-------------------------------------------------------------------------------

#sentmailfile = r'.\sentmail.txt'             # . means in current working dir

#sourcedir    = r'C:\...\PP4E\Internet\Email\PyMailGui\'
#sentmailfile = sourcedir + 'sentmail.txt'

# determine automatically from one of my source files
import wraplines, os
mysourcedir   = os.path.dirname(os.path.abspath(wraplines.__file__))
sentmailfile  = os.path.join(mysourcedir, 'sentmail.txt')

#-------------------------------------------------------------------------------
# (defunct) local file where pymail saves POP mail (full text);
# PyMailGUI instead asks for a name in GUI with a pop-up dialog;
# Also asks for Split directory, and part buttons save in ./TempParts;
#-------------------------------------------------------------------------------

#savemailfile = r'c:\temp\savemail.txt'       # not used in PyMailGUI: dialog

#-------------------------------------------------------------------------------
# (optional) customize headers displayed in PyMailGUI list and view windows;
# listheaders replaces default, viewheaders extends it; both must be tuple of
# strings, or None to use default hdrs;
#-------------------------------------------------------------------------------

listheaders = ('Subject', 'From', 'Date', 'To', 'X-Mailer')
viewheaders = ('Bcc',)

#-------------------------------------------------------------------------------
# (optional) PyMailGUI fonts and colors for text server/file message list
# windows, message content view windows, and view window attachment buttons;
# use ('family', size, 'style') for font; 'colorname' or hexstr '#RRGGBB' for
# color (background, foreground);  None means use defaults;  font/color of
# view windows can also be set interactively with texteditor's Tools menu;
# see also the setcolor.py example in the GUI part (ch8) for custom colors;
#-------------------------------------------------------------------------------

listbg   = 'indianred'                  # None, 'white', '#RRGGBB'
listfg   = 'black'
listfont = ('courier', 9, 'bold')       # None, ('courier', 12, 'bold italic')
                                        # use fixed-width font for list columns
viewbg     = 'light blue'               # was '#dbbedc'
viewfg     = 'black'
viewfont   = ('courier', 10, 'bold')
viewheight = 18                         # max lines for height when opened (20)

partfg   = None
partbg   = None

# see Tk color names: aquamarine paleturquoise powderblue goldenrod burgundy ....
#listbg = listfg = listfont = None
#viewbg = viewfg = viewfont = viewheight = None      # to use defaults
#partbg = partfg = None

#-------------------------------------------------------------------------------
# (optional) column at which mail's original text should be wrapped for view,
# reply, and forward;  wraps at first delimiter to left of this position;
# composed text is not auto-wrapped: user or recipient's mail tool must wrap
# new text if desired; to disable wrapping, set this to a high value (1024?);
#-------------------------------------------------------------------------------

wrapsz = 90

#-------------------------------------------------------------------------------
# (optional) control how PyMailGUI opens mail parts in the GUI;
# for view window Split actions and attachment quick-access buttons;
# if not okayToOpenParts, quick-access part buttons will not appear in
# the GUI, and Split saves parts in a directory but does not open them;
# verifyPartOpens used by both Split action and quick-access buttons:
# all known-type parts open automatically on Split if this set to False;
# verifyHTMLTextOpen used by web browser open of HTML main text part:
#-------------------------------------------------------------------------------

okayToOpenParts    = True      # open any parts/attachments at all?
verifyPartOpens    = False     # ask permission before opening each part?
verifyHTMLTextOpen = False     # if main text part is HTML, ask before open?

#-------------------------------------------------------------------------------
# (optional) the maximum number of quick-access mail part buttons to show
# in the middle of view windows; after this many, a "..." button will be
# displayed, which runs the "Split" action to extract additional parts;
#-------------------------------------------------------------------------------

maxPartButtons = 8             # how many part buttons in view windows


# *** 3.0 additions follow ***
#-------------------------------------------------------------------------------
# (required, for fetch) the Unicode encoding used to decode fetched full message 
# bytes, and to encode and decode message text stored in text-mode save files; see
# the book's Chapter 13 for details: this is a limited and temporary approach to
# Unicode encodings until a new bytes-friendly email package parser is provided
# which can handle Unicode encodings more accurately on a message-level basis;
# note: 'latin1' (an 8-bit encoding which is a superset of 7-bit ascii) was 
# required to decode message in some old email save files I had, not 'utf8';
#-------------------------------------------------------------------------------

fetchEncoding = 'latin-1'    # how to decode and store full message text (ascii?)

#-------------------------------------------------------------------------------
# (optional, for send) Unicode encodings for composed mail's main text plus all
# text attachments; set these to None to be prompted for encodings on mail send, 
# else uses values here across entire session; default='latin-1' if GUI Cancel;
# in all cases, falls back on UTF-8 if your encoding setting or input does not
# work for the text being sent (e.g., ascii chosen for reply to non-ascii text,
# or non-ascii attachments); the email package is pickier than Python about 
# names: latin-1 is known (uses qp MIME), but latin1 isn't (uses base64 MIME);
# set these to sys.getdefaultencoding() result to choose the platform default;
# encodings of text parts of fetched email are automatic via message headers;
#-------------------------------------------------------------------------------

mainTextEncoding       = 'ascii'   # main mail body text part sent (None=ask)
attachmentTextEncoding = 'ascii'   # all text part attachments sent (utf-8, latin-1)

#-------------------------------------------------------------------------------
# (optional, for send) set this to a Unicode encoding name to be applied to 
# non-ASCII headers, as well as non-ASCII names in email addresses in headers,
# in composed messages when they are sent;  None means use the UTF-8 default,
# which should work for most use cases; email names that fail to decode are 
# dropped (the address part is used);  note that header decoding is performed 
# automatically for display, according to header content, not user setting;
#-------------------------------------------------------------------------------

headersEncodeTo = None     # how to encode non-ASCII headers sent (None=UTF-8)

#-------------------------------------------------------------------------------
# (optional) select text, HTML, or both versions of the help document;
# always shows one or the other: displays HTML if both of these are turned off
#-------------------------------------------------------------------------------

showHelpAsText = True      # scrolled text, with button for opening source files
showHelpAsHTML = True      # HTML in a web browser, without source file links

#-------------------------------------------------------------------------------
# (optional) if True, don't show a selected HTML text message part in a PyEdit 
# popup too if it is being displayed in a web browser; if False show both, to
# see Unicode encoding name and effect in a  text widget (browser may not know);
#-------------------------------------------------------------------------------

skipTextOnHtmlPart = False       # don't show html part in PyEdit popup too

#-------------------------------------------------------------------------------
# (optional) the maximum number of mail headers or messages that will be 
# downloaded on each load request; given this setting N, PyMailGUI fetches at 
# most N of the most recently arrived mails; older mails outside this set are 
# not fetched from the server, but are displayed as empty/dummy emails; if this
# is assigned to None (or 0), loads will have no such limit; use this if you 
# have very many mails in your inbox, and your Internet or mail server speed 
# makes full loads too slow to be practical; PyMailGUI also loads only 
# newly-arrived headers, but this setting is independent of that feature; 
#-------------------------------------------------------------------------------

fetchlimit = 50            # maximum number headers/emails to fetch on loads

#-------------------------------------------------------------------------------
# (optional) initial width, height of mail index lists (chars x lines);  just 
# a convenience, since the window can be resized/expanded freely once opened; 
#-------------------------------------------------------------------------------

listWidth = None           # None = use default 74
listHeight = None          # None = use default 15

#-------------------------------------------------------------------------------
# (optional, for reply) if True, the Reply operation prefills the reply's Cc 
# with all original mail recipients, after removing duplicates and the new sender;
# if False, no CC prefill occurs, and the reply is configured to reply to the 
# original sender only; the Cc line may always be edited later, in either case.
#-------------------------------------------------------------------------------

repliesCopyToAll = True   # True=reply to sender + all recipients, else sender

#end
