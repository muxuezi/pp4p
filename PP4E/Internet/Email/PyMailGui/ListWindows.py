"""
###############################################################################
Implementation of mail-server and save-file message list main windows:
one class per kind.  Code is factored here for reuse: server and file
list windows are customized versions of the PyMailCommon list window class;
the server window maps actions to mail transferred from a server, and the
file window applies actions to a local file.  

List windows create View, Write, Reply, and Forward windows on user actions.
The server list window is the main window opened on program startup by the 
top-level file;  file list windows are opened on demand via server and file 
list window "Open".  Msgnums may be temporarily out of sync with server if 
POP inbox changes (triggers full reload here).

Changes here in 2.1:
-now checks on deletes and loads to see if msg nums in sync with server
-added up to N attachment direct-access buttons on view windows
-threaded save-mail file loads, to avoid N-second pause for big files
-also threads save-mail file deletes so file write doesn't pause GUI

TBD:
-save-mail file saves still not threaded: may pause GUI briefly, but
 uncommon - unlike load and delete, save/send only appends the local file.
-implementation of local save-mail files as text files with separators
 is mostly a prototype: it loads all full mails into memory, and so limits
 the practical size of these files; better alternative: use 2 DBM keyed
 access files for hdrs and fulltext, plus a list to map keys to position;
 in this scheme save-mail files become directories, no longer readable.
###############################################################################
"""

from SharedNames import *     # program-wide global objects
from ViewWindows import ViewWindow, WriteWindow, ReplyWindow, ForwardWindow


###############################################################################
# main frame - general structure for both file and server message lists
###############################################################################


class PyMailCommon(mailtools.MailParser):
    """
    an abstract widget package, with main mail listbox;
    mixed in with a Tk, Toplevel, or Frame by top-level window classes;
    must be customized in mode-specific subclass with actions() and other;
    creates view and write windows on demand: they serve as MailSenders;
    """
    # class attrs shared by all list windows
    threadLoopStarted = False                     # started by first window
    queueChecksPerSecond = 20                     # tweak if CPU use too high
    queueDelay = 1000 // queueChecksPerSecond     # min msecs between timer events 
    queueBatch = 5                                # max callbacks per timer event

    # all windows use same dialogs: remember last dirs
    openDialog = Open(title=appname + ': Open Mail File')
    saveDialog = SaveAs(title=appname + ': Append Mail File')

    # 3.0: avoid downloading (fetching) same message in parallel
    beingFetched = set()

    def __init__(self):
        self.makeWidgets()                        # draw my contents: list,tools
        if not PyMailCommon.threadLoopStarted: 
            
            # start thread exit check loop
            # a timer event loop that dispatches queued GUI callbacks;
            # just one loop for all windows: server,file,views can all thread;
            # self is a Tk, Toplevel,or Frame: any widget type will suffice;
            # 3.0/4E: added queue delay/batch for progress speedup: ~100x/sec;
            
            PyMailCommon.threadLoopStarted = True
            threadtools.threadChecker(self, self.queueDelay, self.queueBatch)
               
    def makeWidgets(self):
        # add all/none checkbtn at bottom
        tools = Frame(self, relief=SUNKEN, bd=2, cursor='hand2')    # 3.0: configs
        tools.pack(side=BOTTOM, fill=X)
        self.allModeVar = IntVar()
        chk = Checkbutton(tools, text="All")
        chk.config(variable=self.allModeVar, command=self.onCheckAll)
        chk.pack(side=RIGHT)

        # add main buttons at bottom toolbar
        for (title, callback) in self.actions():
            if not callback:
                sep = Label(tools, text=title)                # 3.0: separator
                sep.pack(side=LEFT, expand=YES, fill=BOTH)    # expands with window
            else:
                Button(tools, text=title, command=callback).pack(side=LEFT)

        # add multiselect listbox with scrollbars
        listwide = mailconfig.listWidth  or 74    # 3.0: config start size 
        listhigh = mailconfig.listHeight or 15    # wide=chars, high=lines
        mails    = Frame(self)
        vscroll  = Scrollbar(mails)
        hscroll  = Scrollbar(mails, orient='horizontal')
        fontsz   = (sys.platform[:3] == 'win' and 8) or 10      # defaults
        listbg   = mailconfig.listbg   or 'white'
        listfg   = mailconfig.listfg   or 'black'
        listfont = mailconfig.listfont or ('courier', fontsz, 'normal')
        listbox  = Listbox(mails, bg=listbg, fg=listfg, font=listfont)
        listbox.config(selectmode=EXTENDED)
        listbox.config(width=listwide, height=listhigh) # 3.0: init wider
        listbox.bind('<Double-1>', (lambda event: self.onViewRawMail()))

        # crosslink listbox and scrollbars
        vscroll.config(command=listbox.yview, relief=SUNKEN)
        hscroll.config(command=listbox.xview, relief=SUNKEN)
        listbox.config(yscrollcommand=vscroll.set, relief=SUNKEN)
        listbox.config(xscrollcommand=hscroll.set)

        # pack last = clip first
        mails.pack(side=TOP, expand=YES, fill=BOTH)
        vscroll.pack(side=RIGHT,  fill=BOTH)
        hscroll.pack(side=BOTTOM, fill=BOTH)
        listbox.pack(side=LEFT, expand=YES, fill=BOTH)
        self.listBox = listbox

    #################
    # event handlers
    #################

    def onCheckAll(self):
        # all or none click         
        if self.allModeVar.get():
            self.listBox.select_set(0, END)
        else:
            self.listBox.select_clear(0, END)

    def onViewRawMail(self):
        # possibly threaded: view selected messages - raw text headers, body
        msgnums = self.verifySelectedMsgs()
        if msgnums:
            self.getMessages(msgnums, after=lambda: self.contViewRaw(msgnums))

    def contViewRaw(self, msgnums, pyedit=True):     # do we need full TextEditor?
        for msgnum in msgnums:                       # could be a nested def
            fulltext = self.getMessage(msgnum)       # fulltext is Unicode decoded
            if not pyedit:
                # display in a scrolledtext
                from tkinter.scrolledtext import ScrolledText
                window  = windows.QuietPopupWindow(appname, 'raw message viewer')
                browser = ScrolledText(window)
                browser.insert('0.0', fulltext)
                browser.pack(expand=YES, fill=BOTH)
            else:    
                # 3.0/4E: more useful PyEdit text editor
                wintitle = ' - raw message text'
                browser = textEditor.TextEditorMainPopup(self, winTitle=wintitle)
                browser.update()
                browser.setAllText(fulltext)
                browser.clearModified()

    def onViewFormatMail(self):
        """
        possibly threaded: view selected messages - pop up formatted display
        not threaded if in savefile list, or messages are already loaded
        the after action runs only if getMessages prefetch allowed and worked
        """
        msgnums = self.verifySelectedMsgs()
        if msgnums:
            self.getMessages(msgnums, after=lambda: self.contViewFmt(msgnums))

    def contViewFmt(self, msgnums):
        """
        finish View: extract main text, popup view window(s) to display;
        extracts plain text from html text if required, wraps text lines;
        html mails: show extracted text, then save in temp file and open
        in web browser;  part can also be opened manually from view window
        Split or part button;  if non-multipart, other: part must be opened
        manually with Split or part button;  verify html open per mailconfig;

        3.0: for html-only mails, main text is str here, but save its raw
        bytes in binary mode to finesse encodings;  worth the effort because 
        many mails are just html today;  this first tried N encoding guesses 
        (utf-8, latin-1, platform dflt), but now gets and saves raw bytes to
        minimize any fidelity loss;  if a part is later opened on demand, it 
        is saved in a binary file as raw bytes in the same way;

        caveat: the spawned web browser won't have any original email headers:
        it may still have to guess or be told the encoding, unless the html 
        already has its own encoding headers (these take the form of <meta>
        html tags within <head> sections if present; none are inserted in the 
        html here, as some well-formed html parts have them);  IE seems to 
        handle most html part files anyhow;  always encoding html parts to 
        utf-8 may suffice too: this encoding can handle most types of text;  
        """
        for msgnum in msgnums:
            fulltext = self.getMessage(msgnum)             # 3.0: str for parser
            message  = self.parseMessage(fulltext)
            type, content = self.findMainText(message)     # 3.0: Unicode decoded 
            if type in ['text/html', 'text/xml']:          # 3.0: get plain text
                content = html2text.html2text(content)
            content  = wraplines.wrapText1(content, mailconfig.wrapsz)
            ViewWindow(headermap   = message,
                       showtext    = content,            
                       origmessage = message)              # 3.0: decodes headers

            # non-multipart, content-type text/HTML (rude but true!)
            if type == 'text/html':
                if ((not mailconfig.verifyHTMLTextOpen) or
                    askyesno(appname, 'Open message text in browser?')):
                
                    # 3.0: get post mime decode, pre unicode decode bytes
                    type, asbytes = self.findMainText(message, asStr=False)
                    try:
                        from tempfile import gettempdir # or a Tk HTML viewer?
                        tempname = os.path.join(gettempdir(), 'pymailgui.html')
                        tmp = open(tempname, 'wb')      # already encoded
                        tmp.write(asbytes); tmp.close() # flush output now
                        webbrowser.open_new('file://' + tempname)
                    except:
                        showerror(appname, 'Cannot open in browser')

    def onWriteMail(self):
        """
        compose a new email from scratch, without fetching others;
        nothing to quote here, but adds sig, and prefills Bcc with the
        sender's address if this optional header enabled in mailconfig;
        From may be i18N encoded in mailconfig: view window will decode;
        """
        starttext = '\n'                         # use auto signature text
        if mailconfig.mysignature:
            starttext += '%s\n' % mailconfig.mysignature
        From  = mailconfig.myaddress
        WriteWindow(starttext = starttext,
                    headermap = dict(From=From, Bcc=From))    # 3.0: prefill bcc

    def onReplyMail(self):
        # possibly threaded: reply to selected emails
        msgnums = self.verifySelectedMsgs()         
        if msgnums:
            self.getMessages(msgnums, after=lambda: self.contReply(msgnums))

    def contReply(self, msgnums):
        """
        finish Reply: drop attachments, quote with '>', add signature;
        presets initial to/from values from mail or config module;
        don't use original To for From: may be many or a listname;
        To keeps name+<addr> format even if ',' separator in name;
        Uses original From for To, ignores reply-to header is any;
        3.0: replies also copy to all original recipients by default;

        3.0: now uses getaddresses/parseaddr full parsing to separate 
        addrs on commas, and handle any commas that appear nested in 
        email name parts;  multiple addresses are separated by comma 
        in GUI, we copy comma separators when displaying headers, and 
        we use getaddresses to split addrs as needed;  ',' is required 
        by servers for separator;  no longer uses parseaddr to get 1st
        name/addr pair of getaddresses result: use full From for To;

        3.0: we decode the Subject header here because we need its text,
        but the view window superclass of edit windows performs decoding
        on all displayed headers (the extra Subject decode is a no-op);
        on sends, all non-ASCII hdrs and hdr email names are in decoded
        form in the GUI, but are encoded within the mailtools package;
        quoteOrigText also decodes the initial headers it inserts into
        the quoted text block, and index lists decode for display;
        """
        for msgnum in msgnums:
            fulltext = self.getMessage(msgnum)
            message  = self.parseMessage(fulltext)         # may fail: error obj
            maintext = self.formatQuotedMainText(message)  # same as forward

            # from and to are decoded by view window
            From = mailconfig.myaddress                    # not original To
            To   = message.get('From', '')                 # 3.0: ',' sept
            Cc   = self.replyCopyTo(message)               # 3.0: cc all recipients?
            Subj = message.get('Subject', '(no subject)')
            Subj = self.decodeHeader(Subj)                 # deocde for str
            if Subj[:4].lower() != 're: ':                 # 3.0: unify case
                Subj = 'Re: ' + Subj
            ReplyWindow(starttext = maintext,
                        headermap = 
                            dict(From=From, To=To, Cc=Cc, Subject=Subj, Bcc=From))

    def onFwdMail(self):
        # possibly threaded: forward selected emails
        msgnums = self.verifySelectedMsgs()
        if msgnums:
            self.getMessages(msgnums, after=lambda: self.contFwd(msgnums))

    def contFwd(self, msgnums):
        """
        finish Forward: drop attachments, quote with '>', add signature;
        see notes about headers decoding in the Reply action methods;
        view window superclass will decode the From header we pass here;
        """
        for msgnum in msgnums:
            fulltext = self.getMessage(msgnum)
            message  = self.parseMessage(fulltext)
            maintext = self.formatQuotedMainText(message)  # same as reply

            # initial From value from config, not mail
            From = mailconfig.myaddress                    # encoded or not
            Subj = message.get('Subject', '(no subject)')
            Subj = self.decodeHeader(Subj)                 # 3.0: send encodes
            if Subj[:5].lower() != 'fwd: ':                # 3.0: unify case
                Subj = 'Fwd: ' + Subj
            ForwardWindow(starttext = maintext,
                          headermap = dict(From=From, Subject=Subj, Bcc=From))

    def onSaveMailFile(self):
        """
        save selected emails to file for offline viewing;
        disabled if target file load/delete is in progress;
        disabled by getMessages if self is a busy file too;
        contSave not threaded: disables all other actions;
        """
        # Oct 2011, examples 1.3: test for blocking action before fileselect 
        # dialog, else action's exit callback might invalidate selected message
        # numbers while file select dialog is open; getMessages blocks other 
        # changes later, with modal nature of this code; see also onDelete below;  

        if self.okayToSave():     # subclass specific test and error popup

            msgnums = self.selectedMsgs()
            if not msgnums:
                showerror(appname, 'No message selected')
            else:
                # caveat: dialog warns about replacing file
                filename = self.saveDialog.show()            # shared class attr
                if filename:                                 # don't verify num msgs
                    filename = os.path.abspath(filename)     # normalize / to \
                    self.getMessages(msgnums,
                            after=lambda: self.contSave(msgnums, filename))

    def contSave(self, msgnums, filename):
        # test busy now, after poss srvr msgs load
        if (filename in openSaveFiles.keys() and           # viewing this file?
            openSaveFiles[filename].openFileBusy):         # load/del occurring?
            showerror(appname, 'Target file busy - cannot save')
        else:
            try:                                           # caveat:not threaded
                fulltextlist = []                          # 3.0: use encoding
                mailfile = open(filename, 'a', encoding=mailconfig.fetchEncoding)
                for msgnum in msgnums:                     # < 1sec for N megs
                    fulltext = self.getMessage(msgnum)     # but poss many msgs
                    if fulltext[-1] != '\n': fulltext += '\n'
                    mailfile.write(saveMailSeparator)
                    mailfile.write(fulltext)
                    fulltextlist.append(fulltext)
                mailfile.close()
            except:
                showerror(appname, 'Error during save')
                printStack(sys.exc_info())
            else:                                          # why .keys(): EIBTI
                if filename in openSaveFiles.keys():       # viewing this file?
                    window = openSaveFiles[filename]       # update list, raise
                    window.addSavedMails(fulltextlist)     # avoid file reload
                    #window.loadMailFileThread()           # this was very slow

    def onOpenMailFile(self, filename=None):
        # process saved mail offline
        filename = filename or self.openDialog.show()      # shared class attr
        if filename:
            filename = os.path.abspath(filename)           # match on full name
            if filename in openSaveFiles.keys():           # only 1 win per file
                openSaveFiles[filename].lift()             # raise file's window
                showinfo(appname, 'File already open')     # else deletes odd
            else:
                from PyMailGui import PyMailFileWindow     # avoid duplicate win
                popup = PyMailFileWindow(filename)         # new list window
                openSaveFiles[filename] = popup            # removed in quit
                popup.loadMailFileThread()                 # try load in thread

    def onDeleteMail(self):
        """
        delete selected mails from server or file
        """
        # Oct 2011, examples 1.3: test for delete-in-progress before verification
        # pupup, else a prior delete's exit action may be run from an after() timer
        # event callback between pressing Delete and the verification dialog's OK, 
        # invalidating selected message numbers (and possibly deleting wrong mails!);
        # a similar timing issue for the file selection dialog in Save was patched 
        # too, but it seems much less harmful to save than delete incorrect mails;

        if self.okayToDelete():     # subclass specific test and error popup

            msgnums = self.selectedMsgs()                      # subclass: fillIndex
            if not msgnums:                                    # always verify here
                showerror(appname, 'No message selected')
            else:
                if askyesno(appname, 'Verify delete %d mails?' % len(msgnums)):
                    self.doDelete(msgnums)

    ##################
    # utility methods
    ##################

    def selectedMsgs(self):
        # get messages selected in main listbox
        selections = self.listBox.curselection()  # tuple of digit strs, 0..N-1
        return [int(x)+1 for x in selections]     # convert to ints, make 1..N

    warningLimit = 15
    def verifySelectedMsgs(self):
        msgnums = self.selectedMsgs()
        if not msgnums:
            showerror(appname, 'No message selected')
        else:
            numselects = len(msgnums)             
            if numselects > self.warningLimit:
                if not askyesno(appname, 'Open %d selections?' % numselects):
                    msgnums = []
        return msgnums

    def fillIndex(self, maxhdrsize=25):
        """
        fill all of main listbox from message header mappings;
        3.0: decode headers per email/mime/unicode here if encoded;
        3.0: caveat: large chinese characters can break '|' alignment;  
        """
        def makeTimeLocal(origTimeStr):
            """
            Oct 2011, examples 1.3: display sent-time relative to local 
            timezone; must do after decode and for header size calc too; 
            runs: formatdate(mktime_tz(parsedate_tz(there)), localtime=True)
            """
            from email.utils import formatdate   
            from email._parseaddr import parsedate_tz, mktime_tz
            if origTimeStr in [' ', '']: 
                return origTimeStr  # common case: parser fails

            try:
                timeTuple    = parsedate_tz(origTimeStr)
                utcTimeNum   = mktime_tz(timeTuple)
                localTimeStr = formatdate(utcTimeNum, localtime=True)
                return localTimeStr
            except:
                #import traceback; traceback.print_exc()
                #print('Local time failed:', sys.exc_info()[0], sys.exc_info()[1])
                return origTimeStr  # use orig date-time text if anything fails

        hdrmaps  = self.headersMaps()                   # may be empty
        showhdrs = ('Subject', 'From', 'Date', 'To')    # default hdrs to show
        if hasattr(mailconfig, 'listheaders'):          # mailconfig customizes
            showhdrs = mailconfig.listheaders or showhdrs
        addrhdrs = ('From', 'To', 'Cc', 'Bcc')    # 3.0: decode i18n specially

        # compute max field sizes <= hdrsize
        maxsize = {}
        for key in showhdrs:
            allLens = []                                # too big for a list comp!
            for msg in hdrmaps:
                keyval = msg.get(key, ' ')
                if key == 'Date': 
                    allLens.append(len(makeTimeLocal(self.decodeHeader(keyval))))
                elif key not in addrhdrs:
                    allLens.append(len(self.decodeHeader(keyval)))
                else:
                    allLens.append(len(self.decodeAddrHeader(keyval)))
            if not allLens: allLens = [1]
            maxsize[key] = min(maxhdrsize, max(allLens))

        # populate listbox with fixed-width left-justified fields
        self.listBox.delete(0, END)                     # show multiparts with *
        for (ix, msg) in enumerate(hdrmaps):            # via content-type hdr
            msgtype = msg.get_content_maintype()        # no is_multipart yet
            msgline = (msgtype == 'multipart' and '*') or ' '
            msgline += '%03d' % (ix+1)
            for key in showhdrs:
                mysize  = maxsize[key]
                if key == 'Date':
                    keytext = makeTimeLocal(self.decodeHeader(msg.get(key, ' ')))
                elif key not in addrhdrs:
                    keytext = self.decodeHeader(msg.get(key, ' '))
                else:
                    keytext = self.decodeAddrHeader(msg.get(key, ' '))
                msgline += ' | %-*s' % (mysize, keytext[:mysize])
            msgline += '| %.1fK' % (self.mailSize(ix+1) / 1024)   # 3.0: .0 optional
            self.listBox.insert(END, msgline)
        self.listBox.see(END)         # show most recent mail=last line

    def replyCopyTo(self, message):
        """
        3.0: replies copy all original recipients, by prefilling
        Cc header with all addreses in original To and Cc after 
        removing duplicates and new sender;  could decode i18n addrs 
        here, but the view window will decode to display (and send
        will reencode) and the unique set filtering here will work 
        either way, though a sender's i18n address is assumed to be 
        in encoded form in mailconfig (else it is not removed here);
        empty To or Cc headers are okay: split returns empty lists;
        """
        if not mailconfig.repliesCopyToAll:
            # reply to sender only
            Cc = ''
        else:
            # copy all original recipients (3.0)
            allRecipients = (self.splitAddresses(message.get('To', '')) + 
                             self.splitAddresses(message.get('Cc', ''))) 
            uniqueOthers  = set(allRecipients) - set([mailconfig.myaddress])
            Cc = ', '.join(uniqueOthers)
        return Cc or '?'

    def formatQuotedMainText(self, message):
        """
        3.0: factor out common code shared by Reply and Forward:
        fetch decoded text, extract text if html, line wrap, add > quote
        """
        type, maintext = self.findMainText(message)       # 3.0: decoded str
        if type in ['text/html', 'text/xml']:             # 3.0: get plain text
            maintext = html2text.html2text(maintext)
        maintext = wraplines.wrapText1(maintext, mailconfig.wrapsz-2) # 2 = '> '
        maintext = self.quoteOrigText(maintext, message)              # add hdrs, >
        if mailconfig.mysignature:
            maintext = ('\n%s\n' % mailconfig.mysignature) + maintext
        return maintext

    def quoteOrigText(self, maintext, message):
        """
        3.0: we need to decode any i18n (internationalizd) headers here too,
        or they show up in email+MIME encoded form in the quoted text block;
        decodeAddrHeader works on one addr or all in a comma-separated list;
        this may trigger full text encoding on sends, but the main text is 
        also already in fully decoded form: could be in any Unicode scheme;
        """
        quoted = '\n-----Original Message-----\n'
        for hdr in ('From', 'To', 'Subject', 'Date'):
            rawhdr = message.get(hdr, '?')
            if hdr not in ('From', 'To'):
                dechdr = self.decodeHeader(rawhdr)       # full value
            else:
                dechdr = self.decodeAddrHeader(rawhdr)   # name parts only
            quoted += '%s: %s\n' % (hdr, dechdr)
        quoted += '\n' + maintext
        quoted  = '\n' + quoted.replace('\n', '\n> ')
        return quoted

    ########################
    # subclass requirements
    ########################

    def getMessages(self, msgnums, after):        # used by view,save,reply,fwd
        after()                                   # redef if cache, thread test

    # plus okayToQuit?, okayToDelete?, okayToSave?, any unique actions
    def getMessage(self, msgnum): assert False    # used by many: full mail text
    def headersMaps(self): assert False           # fillIndex: hdr mappings list
    def mailSize(self, msgnum): assert False      # fillIndex: size of msgnum
    def doDelete(self): assert False              # onDeleteMail: delete button


###############################################################################
# main window - when viewing messages in local save file (or sent-mail file)
###############################################################################


class PyMailFile(PyMailCommon):
    """
    customize PyMailCommon for viewing saved-mail file offline;
    mixed with a Tk, Toplevel, or Frame, adds main mail listbox;
    maps load, fetch, delete actions to local text file storage;
    file opens and deletes here run in threads for large files;

    save and send not threaded, because only append to file; save 
    is disabled if source or target file busy with load/delete; 
    save disables load, delete, save just because it is not run 
    in a thread (blocks GUI);

    TBD: may need thread and O/S file locks if saves ever do run in
    threads: saves could disable other threads with openFileBusy, but
    file may not be open in GUI;  file locks not sufficient, because 
    GUI updated too;  TBD: appends to sent-mail file may require O/S 
    locks: as is, user gets error pop up if sent during load/del;

    3.0: mail save files are now Unicode text, encoded per an encoding
    name setting in the mailconfig module; this may not support worst 
    case scenarios of unusual or mixed encodings, but most full mail 
    text is ascii, and the Python 3.1 email package is partly broken;
    """
    def actions(self):
        return [ ('Open',   self.onOpenMailFile),
                 ('Write',  self.onWriteMail),
                 ('  ',     None),                           # 3.0:  separators
                 ('View',   self.onViewFormatMail),
                 ('Reply',  self.onReplyMail),
                 ('Fwd',    self.onFwdMail),
                 ('Save',   self.onSaveMailFile),
                 ('Delete', self.onDeleteMail),
                 ('  ',     None),
                 ('Quit',   self.quit) ]

    def __init__(self, filename):
        # caller: do loadMailFileThread next
        PyMailCommon.__init__(self)
        self.filename = filename
        self.openFileBusy = threadtools.ThreadCounter()      # one per window

    def loadMailFileThread(self):
        """
        load or reload file and update window index list;
        called on Open, startup, and possibly on Send if
        sent-mail file appended is currently open;  there
        is always a bogus first item after the text split;
        alt: [self.parseHeaders(m) for m in self.msglist];
        could pop up a busy dialog, but quick for small files;

        2.1: this is now threaded--else runs < 1sec for N meg
        files, but can pause GUI N seconds if very large file;
        Save now uses addSavedMails to append msg lists for
        speed, not this reload;  still called from Send just
        because msg text unavailable - requires refactoring;
        delete threaded too: prevent open and delete overlap;
        """
        if self.openFileBusy:
            # don't allow parallel open/delete changes
            errmsg = 'Cannot load, file is busy:\n"%s"' % self.filename
            showerror(appname, errmsg)
        else:
            #self.listBox.insert(END, 'loading...')      # error if user clicks
            savetitle = self.title()                     # set by window class
            self.title(appname + ' - ' + 'Loading...')
            self.openFileBusy.incr()
            threadtools.startThread(
                action   = self.loadMailFile,
                args     = (),
                context  = (savetitle,),
                onExit   = self.onLoadMailFileExit,
                onFail   = self.onLoadMailFileFail)

    def loadMailFile(self):
        # run in a thread while GUI is active
        # open, read, parser may all raise excs: caught in thread utility
        file = open(self.filename, 'r', encoding=mailconfig.fetchEncoding)   # 3.0
        allmsgs = file.read()
        self.msglist  = allmsgs.split(saveMailSeparator)[1:]       # full text
        self.hdrlist  = list(map(self.parseHeaders, self.msglist)) # msg objects

    def onLoadMailFileExit(self, savetitle):
        # on thread success
        self.title(savetitle)         # reset window title to filename
        self.fillIndex()              # updates GUI: do in main thread
        self.lift()                   # raise my window
        self.openFileBusy.decr()

    def onLoadMailFileFail(self, exc_info, savetitle):
        # on thread exception
        showerror(appname, 'Error opening "%s"\n%s\n%s' %
                           ((self.filename,) +  exc_info[:2]))
        printStack(exc_info)
        self.destroy()                # always close my window?
        self.openFileBusy.decr()      # not needed if destroy

    def addSavedMails(self, fulltextlist):
        """
        optimization: extend loaded file lists for mails
        newly saved to this window's file; in past called
        loadMailThread to reload entire file on save - slow;
        must be called in main GUI thread only: updates GUI;
        sends still reloads sent file if open: no msg text;
        """
        self.msglist.extend(fulltextlist)
        self.hdrlist.extend(map(self.parseHeaders, fulltextlist))  # 3.x iter ok
        self.fillIndex()
        self.lift()

    def okayToSave(self):
        # Oct 2011: test before file selection popup
        if self.openFileBusy:
            # dont allow parallel open/delete changes
            errmsg = 'Cannot save, file is busy:\n"%s"' % self.filename
            showerror(appname, errmsg)
            return False
        else:
            return True

    def okayToDelete(self):
        # Oct 2011: test before verification popup too
        if self.openFileBusy:
            # dont allow parallel open/delete changes
            errmsg = 'Cannot delete, file is busy:\n"%s"' % self.filename
            showerror(appname, errmsg)
            return False
        else:
            return True

    def doDelete(self, msgnums):
        """
        simple-minded, but sufficient: rewrite all
        nondeleted mails to file; can't just delete
        from self.msglist in-place: changes item indexes;
        Py2.3 enumerate(L) same as zip(range(len(L)), L)
        2.1: now threaded, else N sec pause for large files
        """
        if self.openFileBusy:   # test probably not needed here too, but harmless
            # dont allow parallel open/delete changes
            errmsg = 'Cannot delete, file is busy:\n"%s"' % self.filename
            showerror(appname, errmsg)
        else:
            savetitle = self.title()
            self.title(appname + ' - ' + 'Deleting...')
            self.openFileBusy.incr()
            threadtools.startThread(
                action   = self.deleteMailFile,
                args     = (msgnums,),
                context  = (savetitle,),
                onExit   = self.onDeleteMailFileExit,
                onFail   = self.onDeleteMailFileFail)

    def deleteMailFile(self, msgnums):
        # run in a thread while GUI active
        indexed = enumerate(self.msglist)
        keepers = [msg for (ix, msg) in indexed if ix+1 not in msgnums]
        allmsgs = saveMailSeparator.join([''] + keepers)
        file = open(self.filename, 'w', encoding=mailconfig.fetchEncoding)   # 3.0
        file.write(allmsgs)
        self.msglist = keepers
        self.hdrlist = list(map(self.parseHeaders, self.msglist))

    def onDeleteMailFileExit(self, savetitle):
        self.title(savetitle)
        self.fillIndex()              # updates GUI: do in main thread
        self.lift()                   # reset my title, raise my window
        self.openFileBusy.decr()

    def onDeleteMailFileFail(self, exc_info, savetitle):
        showerror(appname, 'Error deleting "%s"\n%s\n%s' %
                           ((self.filename,) +  exc_info[:2]))
        printStack(exc_info)
        self.destroy()                # always close my window?
        self.openFileBusy.decr()      # not needed if destroy

    def getMessages(self, msgnums, after):
        """
        used by view,save,reply,fwd: file load and delete
        threads may change the msg and hdr lists, so disable
        all other operations that depend on them to be safe;
        this test is for self: saves also test target file;
        """
        if self.openFileBusy:
            errmsg = 'Cannot fetch, file is busy:\n"%s"' % self.filename
            showerror(appname, errmsg)
        else:
            after()                      # mail already loaded

    def getMessage(self, msgnum):
        return self.msglist[msgnum-1]    # full text of 1 mail

    def headersMaps(self):
        return self.hdrlist              # email.message.Message objects

    def mailSize(self, msgnum):
        return len(self.msglist[msgnum-1])

    def quit(self):
        # don't destroy during update: fillIndex next
        if self.openFileBusy:
            showerror(appname, 'Cannot quit during load or delete')
        else:
            if askyesno(appname, 'Verify Quit Window?'):
                # delete file from open list
                del openSaveFiles[self.filename]
                Toplevel.destroy(self)


###############################################################################
# main window - when viewing messages on the mail server
###############################################################################


class PyMailServer(PyMailCommon):
    """
    customize PyMailCommon for viewing mail still on server;
    mixed with a Tk, Toplevel, or Frame, adds main mail listbox;
    maps load, fetch, delete actions to email server inbox;
    embeds a MessageCache, which is a mailtools MailFetcher;
    """
    def actions(self):
        return [ ('Load',   self.onLoadServer),
                 ('Open',   self.onOpenMailFile),
                 ('Write',  self.onWriteMail),
                 ('  ',     None),                           # 3.0:  separators
                 ('View',   self.onViewFormatMail),
                 ('Reply',  self.onReplyMail),
                 ('Fwd',    self.onFwdMail),
                 ('Save',   self.onSaveMailFile),
                 ('Delete', self.onDeleteMail),
                 ('  ',     None),
                 ('Quit',   self.quit) ]

    def __init__(self):
        PyMailCommon.__init__(self)
        self.cache = messagecache.GuiMessageCache()    # embedded, not inherited
       #self.listBox.insert(END, 'Press Load to fetch mail')

    def makeWidgets(self):                             # help bar: main win only
        self.addHelpBar()
        PyMailCommon.makeWidgets(self)

    def addHelpBar(self):
        msg = 'PyMailGUI - a Python/tkinter email client  (help)'
        title = Button(self, text=msg)
        title.config(bg='steelblue', fg='white', relief=RIDGE)
        title.config(command=self.onShowHelp)
        title.pack(fill=X)

    def onShowHelp(self):
        """
        load,show text block string
        3.0: now uses HTML and webbrowser module here too
        user setting in mailconfig selects text, HTML, or both
        always displays one or the other: html if both false
        """
        if mailconfig.showHelpAsText:
            from PyMailGuiHelp import helptext
            popuputil.HelpPopup(appname, helptext, showsource=self.onShowMySource)

        if mailconfig.showHelpAsHTML or (not mailconfig.showHelpAsText):
            from PyMailGuiHelp import showHtmlHelp
            showHtmlHelp()    # 3.0: HTML version without source file links

    def onShowMySource(self, showAsMail=False):
        """
        display my sourcecode file, plus imported modules here & elsewhere
        """
        import PyMailGui, ListWindows, ViewWindows, SharedNames, textConfig
        from PP4E.Internet.Email.mailtools import (    # mailtools now a pkg
             mailSender, mailFetcher, mailParser)      # can't use * in def
        mymods = (
            PyMailGui, ListWindows, ViewWindows, SharedNames,
            PyMailGuiHelp, popuputil, messagecache, wraplines, html2text,
            mailtools, mailFetcher, mailSender, mailParser,
            mailconfig, textConfig, threadtools, windows, textEditor)
        for mod in mymods:
            source = mod.__file__
            if source.endswith('.pyc'):
                source = source[:-4] + '.py'       # assume a .py in same dir
            if showAsMail:
                # this is a bit cheesey...
                code   = open(source).read()       # 3.0: platform encoding
                user   = mailconfig.myaddress
                hdrmap = {'From': appname, 'To': user, 'Subject': mod.__name__}
                ViewWindow(showtext=code,
                           headermap=hdrmap,
                           origmessage=email.message.Message())
            else:                 
                # more useful PyEdit text editor
                # 4E: assume in UTF8 Unicode encoding (else PeEdit may ask!)
                wintitle = ' - ' + mod.__name__
                textEditor.TextEditorMainPopup(self, source, wintitle, 'utf-8')

    def onLoadServer(self, forceReload=False):
        """
        threaded: load or reload mail headers list on request;
        Exit,Fail,Progress run by threadChecker after callback via queue;
        load may overlap with sends, but disables all but send;
        could overlap with loadingMsgs, but may change msg cache list;
        forceReload on delete/synch fail, else loads recent arrivals only;
        2.1: cache.loadHeaders may do quick check to see if msgnums
        in synch with server, if we are loading just newly arrived hdrs;
        """
        if loadingHdrsBusy or deletingBusy or loadingMsgsBusy:
            showerror(appname, 'Cannot load headers during load or delete')
        else:
            loadingHdrsBusy.incr()
            self.cache.setPopPassword(appname) # don't update GUI in the thread!
            popup = popuputil.BusyBoxNowait(appname, 'Loading message headers')
            threadtools.startThread(
                action     = self.cache.loadHeaders,
                args       = (forceReload,),
                context    = (popup,),
                onExit     = self.onLoadHdrsExit,
                onFail     = self.onLoadHdrsFail,
                onProgress = self.onLoadHdrsProgress)

    def onLoadHdrsExit(self, popup):
        self.fillIndex()
        popup.quit()
        self.lift()
        loadingHdrsBusy.decr()                     # allow other actions to run 

    def onLoadHdrsFail(self, exc_info, popup):
        popup.quit()
        showerror(appname, 'Load failed: \n%s\n%s' % exc_info[:2])
        printStack(exc_info)                       # send stack trace to stdout
        loadingHdrsBusy.decr()
        if exc_info[0] == mailtools.MessageSynchError:    # synch inbox/index
            self.onLoadServer(forceReload=True)           # new thread: reload
        else:
            self.cache.popPassword = None          # force re-input next time

    def onLoadHdrsProgress(self, i, n, popup):
        popup.changeText('%d of %d' % (i, n))

    def okayToSave(self):
        # Oct 2011: test before file selection popup
        if loadingHdrsBusy or deletingBusy or loadingMsgsBusy:
            showerror(appname, 'Cannot save during load or delete')
            return False
        else:
            return True

    def okayToDelete(self):
        # Oct 2011: test before verification popup too
        if loadingHdrsBusy or deletingBusy or loadingMsgsBusy:
            showerror(appname, 'Cannot delete during load or delete')
            return False
        else:
            return True

    def doDelete(self, msgnumlist):
        """
        threaded: delete from server now - changes msg nums;
        may overlap with sends only, disables all except sends;
        2.1: cache.deleteMessages now checks TOP result to see
        if headers match selected mails, in case msgnums out of
        synch with mail server: poss if mail deleted by other client,
        or server deletes inbox mail automatically - some ISPs may
        move a mail from inbox to undeliverable on load failure;
        """
        if loadingHdrsBusy or deletingBusy or loadingMsgsBusy:  # retest is harmless
            showerror(appname, 'Cannot delete during load or delete')
        else:
            deletingBusy.incr()
            popup = popuputil.BusyBoxNowait(appname, 'Deleting selected mails')
            threadtools.startThread(
                action     = self.cache.deleteMessages,
                args       = (msgnumlist,),
                context    = (popup,),
                onExit     = self.onDeleteExit,
                onFail     = self.onDeleteFail,
                onProgress = self.onDeleteProgress)

    def onDeleteExit(self, popup):
        self.fillIndex()                     # no need to reload from server
        popup.quit()                         # refill index with updated cache
        self.lift()                          # raise index window, release lock
        deletingBusy.decr()

    def onDeleteFail(self, exc_info, popup):
        popup.quit()
        showerror(appname, 'Delete failed: \n%s\n%s' % exc_info[:2])
        printStack(exc_info)
        deletingBusy.decr()                  # delete or synch check failure
        self.onLoadServer(forceReload=True)  # new thread: some msgnums changed

    def onDeleteProgress(self, i, n, popup):
        popup.changeText('%d of %d' % (i, n))

    def getMessages(self, msgnums, after):
        """
        threaded: prefetch all selected messages into cache now;
        used by save, view, reply, and forward to prefill cache;
        may overlap with other loadmsgs and sends, disables delete,load;
        only runs "after" action if the fetch allowed and successful;
        2.1: cache.getMessages tests if index in synch with server,
        but we only test if we have to go to server, not if cached;

        3.0: see messagecache note: now avoids potential fetch of mail
        currently being fetched, if user clicks again while in progress;
        any message being fetched by any other request in progress must
        disable entire toLoad batch: else, need to wait for N other loads;
        fetches are still allowed to overlap in time, as long as disjoint;
        """
        if loadingHdrsBusy or deletingBusy:
            showerror(appname, 'Cannot fetch message during load or delete')
        else:
            toLoad = [num for num in msgnums if not self.cache.isLoaded(num)]
            if not toLoad:
                after()         # all already loaded
                return          # process now, no wait pop up
            else:
                if set(toLoad) & self.beingFetched:   # 3.0: any in progress?
                    showerror(appname, 'Cannot fetch any message being fetched')
                else: 
                    self.beingFetched |= set(toLoad)
                    loadingMsgsBusy.incr()
                    from popuputil import BusyBoxNowait
                    popup = BusyBoxNowait(appname, 'Fetching message contents')
                    threadtools.startThread(
                        action     = self.cache.getMessages,
                        args       = (toLoad,),
                        context    = (after, popup, toLoad),
                        onExit     = self.onLoadMsgsExit,
                        onFail     = self.onLoadMsgsFail,
                        onProgress = self.onLoadMsgsProgress)

    def onLoadMsgsExit(self, after, popup, toLoad):
        self.beingFetched -= set(toLoad)
        popup.quit()
        after()
        loadingMsgsBusy.decr()    # allow other actions after onExit done

    def onLoadMsgsFail(self, exc_info, after, popup, toLoad):
        self.beingFetched -= set(toLoad)
        popup.quit()
        showerror(appname, 'Fetch failed: \n%s\n%s' % exc_info[:2])
        printStack(exc_info)
        loadingMsgsBusy.decr()
        if exc_info[0] == mailtools.MessageSynchError:      # synch inbox/index
            self.onLoadServer(forceReload=True)             # new thread: reload

    def onLoadMsgsProgress(self, i, n, after, popup, toLoad):
        popup.changeText('%d of %d' % (i, n))

    def getMessage(self, msgnum):
        return self.cache.getMessage(msgnum)                # full mail text

    def headersMaps(self):
        # list of email.message.Message objects, 3.x requires list() if map()
        # return [self.parseHeaders(h) for h in self.cache.allHdrs()]
        return list(map(self.parseHeaders, self.cache.allHdrs()))

    def mailSize(self, msgnum):
        return self.cache.getSize(msgnum)

    def okayToQuit(self):
        # any threads still running?
        filesbusy = [win for win in openSaveFiles.values() if win.openFileBusy]
        busy = loadingHdrsBusy or deletingBusy or sendingBusy or loadingMsgsBusy
        busy = busy or filesbusy
        return not busy
