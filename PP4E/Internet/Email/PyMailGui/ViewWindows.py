"""
###############################################################################
Implementation of View, Write, Reply, Forward windows: one class per kind.
Code is factored here for reuse: a Write window is a customized View window,
and Reply and Forward are custom Write windows.  Windows defined in this
file are created by the list windows, in response to user actions.

Caveat:'split' pop ups for opening parts/attachments feel nonintuitive.
2.1: this caveat was addressed, by adding quick-access attachment buttons.
New in 3.0: platform-neutral grid() for mail headers, not packed col frames.
New in 3.0: supports Unicode encodings for main text + text attachments sent.
New in 3.0: PyEdit supports arbitrary Unicode for message parts viewed.
New in 3.0: supports Unicode/mail encodings for headers in  mails sent.

TBD: could avoid verifying quits unless text area modified (like PyEdit2.0),
but these windows are larger, and would not catch headers already changed.
TBD: should Open dialog in write windows be program-wide? (per-window now).
###############################################################################
"""

from SharedNames import *     # program-wide global objects


###############################################################################
# message view window - also a superclass of write, reply, forward
###############################################################################


class ViewWindow(windows.PopupWindow, mailtools.MailParser):
    """
    a Toplevel, with extra protocol and embedded TextEditor;
    inherits saveParts,partsList from mailtools.MailParser;
    mixes in custom subclass logic by direct inheritance here;
    """
    # class attributes
    modelabel       = 'View'                   # used in window titles
    from mailconfig import okayToOpenParts     # open any attachments at all?
    from mailconfig import verifyPartOpens     # ask before open each part?
    from mailconfig import maxPartButtons      # show up to this many + '...'
    from mailconfig import skipTextOnHtmlPart  # 3.0: just browser, not PyEdit?
    tempPartDir     = 'TempParts'              # where 1 selected part saved

    # all view windows use same dialog: remembers last dir
    partsDialog = Directory(title=appname + ': Select parts save directory')

    def __init__(self, headermap, showtext, origmessage=None):
        """
        header map is origmessage, or custom hdr dict for writing;
        showtext is main text part of the message: parsed or custom;
        origmessage is parsed email.message.Message for view mail windows
        """
        windows.PopupWindow.__init__(self, appname, self.modelabel)
        self.origMessage = origmessage         
        self.makeWidgets(headermap, showtext)

    def makeWidgets(self, headermap, showtext):
        """
        add headers, actions, attachments, text editor
        3.0: showtext is assumed to be decoded Unicode str here;
        it will be encoded on sends and saves as directed/needed;
        """
        actionsframe = self.makeHeaders(headermap)
        if self.origMessage and self.okayToOpenParts:
            self.makePartButtons()
        self.editor  = textEditor.TextEditorComponentMinimal(self)
        myactions    = self.actionButtons()
        for (label, callback) in myactions:
            b = Button(actionsframe, text=label, command=callback)
            b.config(bg='beige', relief=RIDGE, bd=2)
            b.pack(side=TOP, expand=YES, fill=BOTH)

        # body text, pack last=clip first
        self.editor.pack(side=BOTTOM)               # may be multiple editors
        self.update()                               # 3.0: else may be @ line2
        self.editor.setAllText(showtext)            # each has own content
        lines = len(showtext.splitlines())
        lines = min(lines + 3, mailconfig.viewheight or 20)
        self.editor.setHeight(lines)                # else height=24, width=80
        self.editor.setWidth(80)                    # or from PyEdit textConfig
        if mailconfig.viewbg:
            self.editor.setBg(mailconfig.viewbg)    # colors, font in mailconfig
        if mailconfig.viewfg:
            self.editor.setFg(mailconfig.viewfg)
        if mailconfig.viewfont:                     # also via editor Tools menu
            self.editor.setFont(mailconfig.viewfont)

    def makeHeaders(self, headermap):
        """
        add header entry fields, return action buttons frame;
        3.0: uses grid for platform-neutral layout of label/entry rows;
        packed row frames with fixed-width labels would work well too;

        3.0: decoding of i18n headers (and email names in address headers)
        is performed here if still required as they are added to the GUI;
        some may have been decoded already for reply/forward windows that 
        need to use decoded text, but the extra decode here is harmless for
        these, and is required for other headers and cases such as fetched 
        mail views;  always, headers are in decoded form when displayed in
        the GUI, and will be encoded within mailtools on Sends if they are 
        non-ASCII (see Write);  i18n header decoding also occurs in list 
        window mail indexes, and for headers added to quoted mail text;
        text payloads in the mail body are also decoded for display and 
        encoded for sends elsewhere in the system (list windows, Write);

        3.0: creators of edit windows prefill Bcc header with sender email
        address to be picked up here, as a convenience for common usages if
        this header is enabled in mailconfig;  Reply also now prefills the
        Cc header with all unique original recipients less From, if enabled;
        """
        top    = Frame(self); top.pack   (side=TOP,   fill=X)
        left   = Frame(top);  left.pack  (side=LEFT,  expand=NO,  fill=BOTH)
        middle = Frame(top);  middle.pack(side=LEFT,  expand=YES, fill=X)

        # headers set may be extended in mailconfig (Bcc, others?)
        self.userHdrs = ()
        showhdrs = ('From', 'To', 'Cc', 'Subject')
        if hasattr(mailconfig, 'viewheaders') and mailconfig.viewheaders:
            self.userHdrs = mailconfig.viewheaders
            showhdrs += self.userHdrs
        addrhdrs = ('From', 'To', 'Cc', 'Bcc')    # 3.0: decode i18n specially
            
        self.hdrFields = []
        for (i, header) in enumerate(showhdrs):
            lab = Label(middle, text=header+':', justify=LEFT)
            ent = Entry(middle)
            lab.grid(row=i, column=0, sticky=EW)
            ent.grid(row=i, column=1, sticky=EW)
            middle.rowconfigure(i, weight=1)
            hdrvalue = headermap.get(header, '?')    # might be empty
            # 3.0: if encoded, decode per email+mime+unicode
            if header not in addrhdrs:
                hdrvalue = self.decodeHeader(hdrvalue)
            else:
                hdrvalue = self.decodeAddrHeader(hdrvalue)
            ent.insert('0', hdrvalue)
            self.hdrFields.append(ent)               # order matters in onSend
        middle.columnconfigure(1, weight=1)
        return left

    def actionButtons(self):                         # must be method for self
        return [('Cancel', self.destroy),            # close view window silently
                ('Parts',  self.onParts),            # multiparts list or the body
                ('Split',  self.onSplit)]

    def makePartButtons(self):
        """
        add up to N buttons that open attachments/parts
        when clicked; alternative to Parts/Split (2.1);
        okay that temp dir is shared by all open messages:
        part file not saved till later selected and opened;
        partname=partname is required in lambda in Py2.4;
        caveat: we could try to skip the main text part;
        """
        def makeButton(parent, text, callback):
            link = Button(parent, text=text, command=callback, relief=SUNKEN)
            if mailconfig.partfg: link.config(fg=mailconfig.partfg)
            if mailconfig.partbg: link.config(bg=mailconfig.partbg)
            link.pack(side=LEFT, fill=X, expand=YES)

        parts = Frame(self)
        parts.pack(side=TOP, expand=NO, fill=X)
        for (count, partname) in enumerate(self.partsList(self.origMessage)):
            if count == self.maxPartButtons:
                makeButton(parts, '...', self.onSplit)
                break
            openpart = (lambda partname=partname: self.onOnePart(partname))
            makeButton(parts, partname, openpart)

    def onOnePart(self, partname):
        """
        locate selected part for button and save and open;
        okay if multiple mails open: resaves each time selected;
        we could probably just use web browser directly here;
        caveat: tempPartDir is relative to cwd - poss anywhere;
        caveat: tempPartDir is never cleaned up: might be large,
        could use tempfile module (just like the HTML main text 
        part display code in onView of the list window class);
        """
        try:
            savedir  = self.tempPartDir
            message  = self.origMessage
            (contype, savepath) = self.saveOnePart(savedir, partname, message)
        except:
            showerror(appname, 'Error while writing part file')
            printStack(sys.exc_info())
        else:
            self.openParts([(contype, os.path.abspath(savepath))])   # reuse

    def onParts(self):
        """
        show message part/attachments in pop-up window;
        uses same file naming scheme as save on Split;
        if non-multipart, single part = full body text
        """
        partnames = self.partsList(self.origMessage)
        msg = '\n'.join(['Message parts:\n'] + partnames)
        showinfo(appname, msg)

    def onSplit(self):
        """
        pop up save dir dialog and save all parts/attachments there;
        if desired, pop up HTML and multimedia parts in web browser,
        text in TextEditor, and well-known doc types on windows;
        could show parts in View windows where embedded text editor
        would provide a save button, but most are not readable text;
        """
        savedir = self.partsDialog.show()          # class attr: at prior dir
        if savedir:                                # tk dir chooser, not file
            try:
                partfiles = self.saveParts(savedir, self.origMessage)
            except:
                showerror(appname, 'Error while writing part files')
                printStack(sys.exc_info())
            else:
                if self.okayToOpenParts: self.openParts(partfiles)

    def askOpen(self, appname, prompt):
        if not self.verifyPartOpens:
            return True
        else:
            return askyesno(appname, prompt)   # pop-up dialog

    def openParts(self, partfiles):
        """
        auto-open well known and safe file types, but only if verified 
        by the user in a pop up; other types must be opened manually 
        from save dir;  at this point, the named parts have been already
        MIME-decoded and saved as raw bytes in binary-mode files, but text 
        parts may be in any Unicode encoding;  PyEdit needs to know the
        encoding to decode, webbrowsers may have to guess or be told;

        caveat: punts for type application/octet-stream even if it has 
        safe filename extension such as .html; caveat: image/audio/video
        could be opened with the book's playfile.py; could also do that 
        if text viewer fails: would start notepad on Windows via startfile;
        webbrowser may handle most cases here too, but specific is better;
        """

        def textPartEncoding(fullfilename):
            """
            3.0: map a text part filename back to charset param in content-type 
            header of part's Message, so we can pass this on to the PyEdit 
            constructor for proper text display;  we could return the charset
            along with content-type from mailtools for text parts, but fewer
            changes are needed if this is handled as a special case here;

            part content is saved in binary mode files by mailtools to avoid 
            encoding issues, but here the original part Message is not directly 
            available; we need this mapping step to extract a Unicode encoding 
            name if present; 4E's PyEdit now allows an explicit encoding name for 
            file opens, and resolves encoding on saves; see Chapter 11 for PyEdit
            policies: it may ask user for an encoding if charset absent or fails;
            caveat: move to mailtools.mailParser to reuse for <meta> in PyMailCGI?
            """
            partname = os.path.basename(fullfilename)
            for (filename, contype, part) in self.walkNamedParts(self.origMessage):
                if filename == partname:
                    return part.get_content_charset()     # None if not in header
            assert False, 'Text part not found'           # should never happen

        for (contype, fullfilename) in partfiles:
            maintype  = contype.split('/')[0]                      # left side
            extension = os.path.splitext(fullfilename)[1]          # not [-4:]
            basename  = os.path.basename(fullfilename)             # strip dir

            # HTML and XML text, web pages, some media
            if contype  in ['text/html', 'text/xml']:
                browserOpened = False
                if self.askOpen(appname, 'Open "%s" in browser?' % basename):
                    try:
                        webbrowser.open_new('file://' + fullfilename)
                        browserOpened = True
                    except:
                        showerror(appname, 'Browser failed: trying editor')
                if not browserOpened or not self.skipTextOnHtmlPart:
                    try:  
                        # try PyEdit to see encoding name and effect
                        encoding = textPartEncoding(fullfilename)
                        textEditor.TextEditorMainPopup(parent=self,
                                   winTitle=' - %s email part' % (encoding or '?'),
                                   loadFirst=fullfilename, loadEncode=encoding)
                    except:
                        showerror(appname, 'Error opening text viewer')

            # text/plain, text/x-python, etc.; 4E: encoding, may fail
            elif maintype == 'text':
                if self.askOpen(appname, 'Open text part "%s"?' % basename):
                    try:
                        encoding = textPartEncoding(fullfilename)
                        textEditor.TextEditorMainPopup(parent=self,
                                   winTitle=' - %s email part' % (encoding or '?'),
                                   loadFirst=fullfilename, loadEncode=encoding)
                    except:
                        showerror(appname, 'Error opening text viewer')

            # multimedia types: Windows opens mediaplayer, imageviewer, etc.
            elif maintype in ['image', 'audio', 'video']:
                if self.askOpen(appname, 'Open media part "%s"?' % basename):
                    try:
                        webbrowser.open_new('file://' + fullfilename)
                    except:
                        showerror(appname, 'Error opening browser')

            # common Windows documents: Word, Excel, Adobe, archives, etc.
            elif (sys.platform[:3] == 'win' and
                  maintype == 'application' and                      # 3.0: +x types
                  extension in ['.doc', '.docx', '.xls', '.xlsx',    # generalize me
                                '.pdf', '.zip',  '.tar', '.wmv']):
                    if self.askOpen(appname, 'Open part "%s"?' % basename):
                        os.startfile(fullfilename)

            else:  # punt!
                msg = 'Cannot open part: "%s"\nOpen manually in: "%s"'
                msg = msg % (basename, os.path.dirname(fullfilename))
                showinfo(appname, msg)


###############################################################################
# message edit windows - write, reply, forward
###############################################################################


if mailconfig.smtpuser:                              # user set in mailconfig?
    MailSenderClass = mailtools.MailSenderAuth       # login/password required
else:
    MailSenderClass = mailtools.MailSender


class WriteWindow(ViewWindow, MailSenderClass):
    """
    customize view display for composing new mail
    inherits sendMessage from mailtools.MailSender
    """
    modelabel = 'Write'

    def __init__(self, headermap, starttext):
        ViewWindow.__init__(self, headermap, starttext)
        MailSenderClass.__init__(self)
        self.attaches   = []                     # each win has own open dialog
        self.openDialog = None                   # dialog remembers last dir

    def actionButtons(self):
        return [('Cancel', self.quit),           # need method to use self
                ('Parts',  self.onParts),        # PopupWindow verifies cancel
                ('Attach', self.onAttach),
                ('Send',   self.onSend)]         # 4E: don't pad: centered

    def onParts(self):
        # caveat: deletes not currently supported
        if not self.attaches:
            showinfo(appname, 'Nothing attached')
        else:
            msg = '\n'.join(['Already attached:\n'] + self.attaches)
            showinfo(appname, msg)

    def onAttach(self):
        """
        attach a file to the mail: name added here will be
        added as a part on Send, inside the mailtools pkg;
        4E: could ask Unicode type here instead of on send
        """
        if not self.openDialog:
            self.openDialog = Open(title=appname + ': Select Attachment File')
        filename = self.openDialog.show()        # remember prior dir
        if filename:
            self.attaches.append(filename)       # to be opened in send method

    def resolveUnicodeEncodings(self):
        """
        3.0/4E: to prepare for send, resolve Unicode encoding for text parts:
        both main text part, and any text part attachments;  the main text part
        may have had a known encoding if this is a reply or forward, but not for
        a write, and it may require a different encoding after editing anyhow;
        smtplib in 3.1 requires that full message text be encodable per ASCII
        when sent (if it's a str), so it's crucial to get this right here; else
        fails if reply/fwd to UTF8 text when config=ascii if any non-ascii chars;
        try user setting and reply but fall back on general UTF8 as a last resort;
        """

        def isTextKind(filename):
            contype, encoding = mimetypes.guess_type(filename)
            if contype is None or encoding is not None:    # 4E utility
                return False                               # no guess, compressed?
            maintype, subtype = contype.split('/', 1)      # check for text/?
            return maintype == 'text'                   

        # resolve many body text encoding
        bodytextEncoding = mailconfig.mainTextEncoding
        if bodytextEncoding == None:
            asknow = askstring('PyMailGUI', 'Enter main text Unicode encoding name')
            bodytextEncoding = asknow or 'latin-1'    # or sys.getdefaultencoding()?

        # last chance: use utf-8 if can't encode per prior selections
        if bodytextEncoding != 'utf-8':
            try:
                bodytext = self.editor.getAllText()
                bodytext.encode(bodytextEncoding)
            except (UnicodeError, LookupError):       # lookup: bad encoding name
                bodytextEncoding = 'utf-8'            # general code point scheme

        # resolve any text part attachment encodings
        attachesEncodings = []
        config = mailconfig.attachmentTextEncoding
        for filename in self.attaches:
            if not isTextKind(filename):
                attachesEncodings.append(None)        # skip non-text: don't ask
            elif config != None:
                attachesEncodings.append(config)      # for all text parts if set
            else:
                prompt = 'Enter Unicode encoding name for %' % filename
                asknow = askstring('PyMailGUI', prompt)
                attachesEncodings.append(asknow or 'latin-1')

            # last chance: use utf-8 if can't decode per prior selections
            choice = attachesEncodings[-1]
            if choice != None and choice != 'utf-8':
                try:
                    attachbytes = open(filename, 'rb').read()
                    attachbytes.decode(choice)
                except (UnicodeError, LookupError, IOError):
                    attachesEncodings[-1] = 'utf-8'
        return bodytextEncoding, attachesEncodings

    def onSend(self):
        """
        threaded: mail edit window Send button press;
        may overlap with any other thread, disables none but quit;
        Exit,Fail run by threadChecker via queue in after callback;
        caveat: no progress here, because send mail call is atomic;
        assumes multiple recipient addrs are separated with ',';
        mailtools module handles encodings, attachments, Date, etc; 
        mailtools module also saves sent message text in a local file

        3.0: now fully parses To,Cc,Bcc (in mailtools) instead of 
        splitting on the separator naively;  could also use multiline
        input widgets instead of simple entry;  Bcc added to envelope,
        not headers;

        3.0: Unicode encodings of text parts is resolved here, because
        it may require GUI prompts;  mailtools performs the actual 
        encoding for parts as needed and requested;

        3.0: i18n headers are already decoded in the GUI fields here; 
        encoding of any non-ASCII i18n headers is performed in mailtools,
        not here, because no GUI interaction is required;
        """
       
        # resolve Unicode encoding for text parts;
        bodytextEncoding, attachesEncodings = self.resolveUnicodeEncodings()

        # get components from GUI; 3.0: i18n headers are decoded
        fieldvalues = [entry.get() for entry in self.hdrFields]
        From, To, Cc, Subj = fieldvalues[:4]
        extraHdrs = [('Cc', Cc), ('X-Mailer', appname + ' (Python)')]
        extraHdrs += list(zip(self.userHdrs, fieldvalues[4:]))
        bodytext = self.editor.getAllText()

        # split multiple recipient lists on ',', fix empty fields
        Tos = self.splitAddresses(To)
        for (ix, (name, value)) in enumerate(extraHdrs):
            if value:                                           # ignored if ''
                if value == '?':                                # ? not replaced
                    extraHdrs[ix] = (name, '')
                elif name.lower() in ['cc', 'bcc']:             # split on ','
                    extraHdrs[ix] = (name, self.splitAddresses(value))

        # withdraw to disallow send during send
        # caveat: might not be foolproof - user may deiconify if icon visible 
        self.withdraw()
        self.getPassword()      # if needed; don't run pop up in send thread!
        popup = popuputil.BusyBoxNowait(appname, 'Sending message')
        sendingBusy.incr()
        threadtools.startThread(
            action  = self.sendMessage,
            args    = (From, Tos, Subj, extraHdrs, bodytext, self.attaches,
                                         saveMailSeparator,
                                         bodytextEncoding,
                                         attachesEncodings),
            context = (popup,),
            onExit  = self.onSendExit,
            onFail  = self.onSendFail)

    def onSendExit(self, popup):
        """
        erase wait window, erase view window, decr send count;
        sendMessage call auto saves sent message in local file;
        can't use window.addSavedMails: mail text unavailable;
        """
        popup.quit()
        self.destroy()
        sendingBusy.decr()

        # poss \ when opened, / in mailconfig
        sentname = os.path.abspath(mailconfig.sentmailfile)  # also expands '.'
        if sentname in openSaveFiles.keys():                 # sent file open?
            window = openSaveFiles[sentname]                 # update list,raise
            window.loadMailFileThread()

    def onSendFail(self, exc_info, popup):
        # pop-up error, keep msg window to save or retry, redraw actions frame
        popup.quit()
        self.deiconify()
        self.lift()
        showerror(appname, 'Send failed: \n%s\n%s' % exc_info[:2])
        printStack(exc_info)
        MailSenderClass.smtpPassword = None        # try again; 3.0/4E: not self
        sendingBusy.decr()

    def askSmtpPassword(self):
        """
        get password if needed from GUI here, in main thread;
        caveat: may try this again in thread if no input first
        time, so goes into a loop until input is provided; see
        pop paswd input logic for a nonlooping alternative
        """
        password = ''
        while not password:
            prompt = ('Password for %s on %s?' %
                     (self.smtpUser, self.smtpServerName))
            password = popuputil.askPasswordWindow(appname, prompt)
        return password


class ReplyWindow(WriteWindow):
    """
    customize write display for replying
    text and headers set up by list window
    """
    modelabel = 'Reply'


class ForwardWindow(WriteWindow):
    """
    customize reply display for forwarding
    text and headers set up by list window
    """
    modelabel = 'Forward'
