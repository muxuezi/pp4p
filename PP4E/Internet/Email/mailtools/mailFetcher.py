"""
###############################################################################
retrieve, delete, match mail from a POP server (see __init__ for docs, test)
###############################################################################
"""

import poplib, mailconfig, sys               # client's mailconfig on sys.path 
print('user:', mailconfig.popusername)       # script dir, pythonpath, changes

from .mailParser import MailParser                 # for headers matching (4E: .)
from .mailTool   import MailTool, SilentMailTool   # trace control supers (4E: .)

# index/server msgnum out of synch tests
class DeleteSynchError(Exception): pass            # msg out of synch in del
class TopNotSupported(Exception): pass             # can't run synch test
class MessageSynchError(Exception): pass           # index list out of sync

class MailFetcher(MailTool):
    """
    fetch mail: connect, fetch headers+mails, delete mails
    works on any machine with Python+Inet; subclass me to cache
    implemented with the POP protocol; IMAP requires new class;
    4E: handles decoding of full mail text on fetch for parser;
    """
    def __init__(self, popserver=None, popuser=None, poppswd=None, hastop=True):
        self.popServer   = popserver or mailconfig.popservername
        self.popUser     = popuser   or mailconfig.popusername
        self.srvrHasTop  = hastop
        self.popPassword = poppswd  # ask later if None

    def connect(self):
        self.trace('Connecting...')
        self.getPassword()                          # file, GUI, or console
        server = poplib.POP3(self.popServer, timeout=20)
        server.user(self.popUser)                   # connect,login POP server
        server.pass_(self.popPassword)              # pass is a reserved word
        self.trace(server.getwelcome())             # print returned greeting
        return server
    
    # use setting in client's mailconfig on import search path;
    # to tailor, this can be changed in class or per instance;
    fetchEncoding = mailconfig.fetchEncoding

    def decodeFullText(self, messageBytes):
        """
        4E, Py3.1: decode full fetched mail text bytes to str Unicode string; 
        done at fetch, for later display or parsing (full mail text is always 
        Unicode thereafter);  decode with per-class or per-instance setting, or 
        common types;  could also try headers inspection, or intelligent guess 
        from structure; in Python 3.2/3.3, this step may not be required: if so, 
        change to return message line list intact; for more details see Chapter 13;

        an 8-bit encoding such as latin-1 will likely suffice for most emails, as
        ASCII is the original standard;  this method applies to entire/full message 
        text, which is really just one part of the email encoding story: Message 
        payloads and Message headers may also be encoded per email, MIME, and 
        Unicode standards; see Chapter 13 and mailParser and mailSender for more;
        """
        text = None
        kinds =  [self.fetchEncoding]             # try user setting first
        kinds += ['ascii', 'latin1', 'utf8']      # then try common types
        kinds += [sys.getdefaultencoding()]       # and platform dflt (may differ)
        for kind in kinds:                        # may cause mail saves to fail
            try:
                text = [line.decode(kind) for line in messageBytes]
                break
            except (UnicodeError, LookupError):   # LookupError: bad name
                pass

        if text == None:
            # try returning headers + error msg, else except may kill client;
            # still try to decode headers per ascii, other, platform default;

            blankline = messageBytes.index(b'')
            hdrsonly  = messageBytes[:blankline]
            commons   = ['ascii', 'latin1', 'utf8']
            for common in commons:
                try:
                    text = [line.decode(common) for line in hdrsonly] 
                    break
                except UnicodeError:
                    pass
            else:                                                  # none worked
                try:
                    text = [line.decode() for line in hdrsonly]    # platform dflt?
                except UnicodeError:
                    text = ['From: (sender of unknown Unicode format headers)']
            text += ['', '--Sorry: mailtools cannot decode this mail content!--']
        return text

    def downloadMessage(self, msgnum):
        """
        load full raw text of one mail msg, given its
        POP relative msgnum; caller must parse content
        """
        self.trace('load ' + str(msgnum))
        server = self.connect()
        try:
            resp, msglines, respsz = server.retr(msgnum)
        finally:
            server.quit()
        msglines = self.decodeFullText(msglines)   # raw bytes to Unicode str
        return '\n'.join(msglines)                 # concat lines for parsing

    def downloadAllHeaders(self, progress=None, loadfrom=1):
        """
        get sizes, raw header text only, for all or new msgs
        begins loading headers from message number loadfrom
        use loadfrom to load newly arrived mails only
        use downloadMessage to get a full msg text later
        progress is a function called with (count, total);
        returns: [headers text], [mail sizes], loadedfull?

        4E: add mailconfig.fetchlimit to support large email
        inboxes: if not None, only fetches that many headers, 
        and returns others as dummy/empty mail; else inboxes
        like one of mine (4K emails) are not practical to use;
        4E: pass loadfrom along to downloadAllMsgs (a buglet);
        """
        if not self.srvrHasTop:                    # not all servers support TOP
            # naively load full msg text
            return self.downloadAllMsgs(progress, loadfrom)  
        else:
            self.trace('loading headers')
            fetchlimit = mailconfig.fetchlimit
            server = self.connect()                # mbox now locked until quit
            try:
                resp, msginfos, respsz = server.list()   # 'num size' lines list
                msgCount = len(msginfos)                 # alt to srvr.stat[0]
                msginfos = msginfos[loadfrom-1:]         # drop already loadeds
                allsizes = [int(x.split()[1]) for x in msginfos]
                allhdrs  = []
                for msgnum in range(loadfrom, msgCount+1):          # poss empty
                    if progress: progress(msgnum, msgCount)         # run callback
                    if fetchlimit and (msgnum <= msgCount - fetchlimit):
                        # skip, add dummy hdrs
                        hdrtext = 'Subject: --mail skipped--\n\n' 
                        allhdrs.append(hdrtext)
                    else:
                        # fetch, retr hdrs only
                        resp, hdrlines, respsz = server.top(msgnum, 0)
                        hdrlines = self.decodeFullText(hdrlines)
                        allhdrs.append('\n'.join(hdrlines))
            finally:
                server.quit()                          # make sure unlock mbox
            assert len(allhdrs) == len(allsizes)
            self.trace('load headers exit')
            return allhdrs, allsizes, False

    def downloadAllMessages(self, progress=None, loadfrom=1):
        """
        load full message text for all msgs from loadfrom..N,
        despite any caching that may be being done in the caller;
        much slower than downloadAllHeaders, if just need hdrs;

        4E: support mailconfig.fetchlimit: see downloadAllHeaders;
        could use server.list() to get sizes of skipped emails here
        too, but clients probably don't care about these anyhow; 
        """
        self.trace('loading full messages')
        fetchlimit = mailconfig.fetchlimit
        server = self.connect()
        try:
            (msgCount, msgBytes) = server.stat()          # inbox on server
            allmsgs  = []
            allsizes = []
            for i in range(loadfrom, msgCount+1):         # empty if low >= high
                if progress: progress(i, msgCount)
                if fetchlimit and (i <= msgCount - fetchlimit):
                    # skip, add dummy mail
                    mailtext = 'Subject: --mail skipped--\n\nMail skipped.\n' 
                    allmsgs.append(mailtext)
                    allsizes.append(len(mailtext))
                else:
                    # fetch, retr full mail
                    (resp, message, respsz) = server.retr(i)  # save text on list
                    message = self.decodeFullText(message)
                    allmsgs.append('\n'.join(message))        # leave mail on server
                    allsizes.append(respsz)                   # diff from len(msg)
        finally:
            server.quit()                                     # unlock the mail box
        assert len(allmsgs) == (msgCount - loadfrom) + 1      # msg nums start at 1
       #assert sum(allsizes) == msgBytes                      # not if loadfrom > 1
        return allmsgs, allsizes, True                        # not if fetchlimit

    def deleteMessages(self, msgnums, progress=None):
        """
        delete multiple msgs off server; assumes email inbox
        unchanged since msgnums were last determined/loaded;
        use if msg headers not available as state information;
        fast, but poss dangerous: see deleteMessagesSafely
        """
        self.trace('deleting mails')
        server = self.connect()
        try:
            for (ix, msgnum) in enumerate(msgnums):   # don't reconnect for each
                if progress: progress(ix+1, len(msgnums))
                server.dele(msgnum)
        finally:                                      # changes msgnums: reload
            server.quit()

    def deleteMessagesSafely(self, msgnums, synchHeaders, progress=None):
        """
        delete multiple msgs off server, but use TOP fetches to
        check for a match on each msg's header part before deleting;
        assumes the email server supports the TOP interface of POP,
        else raises TopNotSupported - client may call deleteMessages;

        use if the mail server might change the inbox since the email
        index was last fetched, thereby changing POP relative message
        numbers;  this can happen if email is deleted in a different
        client;  some ISPs may also move a mail from inbox to the
        undeliverable box in response to a failed download;

        synchHeaders must be a list of already loaded mail hdrs text,
        corresponding to selected msgnums (requires state);  raises
        exception if any out of synch with the email server;  inbox is
        locked until quit, so it should not change between TOP check
        and actual delete: synch check must occur here, not in caller;
        may be enough to call checkSynchError+deleteMessages, but check
        each msg here in case deletes and inserts in middle of inbox;
        """
        if not self.srvrHasTop:
            raise TopNotSupported('Safe delete cancelled')

        self.trace('deleting mails safely')
        errmsg  = 'Message %s out of synch with server.\n'
        errmsg += 'Delete terminated at this message.\n'
        errmsg += 'Mail client may require restart or reload.'

        server = self.connect()                       # locks inbox till quit
        try:                                          # don't reconnect for each
            (msgCount, msgBytes) = server.stat()      # inbox size on server
            for (ix, msgnum) in enumerate(msgnums):
                if progress: progress(ix+1, len(msgnums))
                if msgnum > msgCount:                            # msgs deleted
                    raise DeleteSynchError(errmsg % msgnum)
                resp, hdrlines, respsz = server.top(msgnum, 0)   # hdrs only
                hdrlines = self.decodeFullText(hdrlines)
                msghdrs = '\n'.join(hdrlines)
                if not self.headersMatch(msghdrs, synchHeaders[msgnum-1]):
                    raise DeleteSynchError(errmsg % msgnum)
                else:
                    server.dele(msgnum)               # safe to delete this msg
        finally:                                      # changes msgnums: reload
            server.quit()                             # unlock inbox on way out

    def checkSynchError(self, synchHeaders):
        """
        check to see if already loaded hdrs text in synchHeaders
        list matches what is on the server, using the TOP command in
        POP to fetch headers text; use if inbox can change due to
        deletes in other client, or automatic action by email server;
        raises except if out of synch, or error while talking to server;

        for speed, only checks last in last: this catches inbox deletes,
        but assumes server won't insert before last (true for incoming
        mails); check inbox size first: smaller if just deletes;  else
        top will differ if deletes and newly arrived messages added at
        end;  result valid only when run: inbox may change after return;
        """
        self.trace('synch check')
        errormsg  = 'Message index out of synch with mail server.\n'
        errormsg += 'Mail client may require restart or reload.'
        server = self.connect()
        try:
            lastmsgnum = len(synchHeaders)                      # 1..N
            (msgCount, msgBytes) = server.stat()                # inbox size
            if lastmsgnum > msgCount:                           # fewer now?
                raise MessageSynchError(errormsg)               # none to cmp
            if self.srvrHasTop:
                resp, hdrlines, respsz = server.top(lastmsgnum, 0)  # hdrs only
                hdrlines = self.decodeFullText(hdrlines)
                lastmsghdrs = '\n'.join(hdrlines)
                if not self.headersMatch(lastmsghdrs, synchHeaders[-1]):
                    raise MessageSynchError(errormsg)
        finally:
            server.quit()

    def headersMatch(self, hdrtext1, hdrtext2):
        """"
        may not be as simple as a string compare: some servers add
        a "Status:" header that changes over time; on one ISP, it
        begins as "Status: U" (unread), and changes to "Status: RO"
        (read, old) after fetched once - throws off synch tests if
        new when index fetched, but have been fetched once before
        delete or last-message check;  "Message-id:" line is unique
        per message in theory, but optional, and can be anything if
        forged; match more common: try first; parsing costly: try last
        """
        # try match by simple string compare
        if hdrtext1 == hdrtext2:
            self.trace('Same headers text')
            return True

        # try match without status lines
        split1 = hdrtext1.splitlines()       # s.split('\n'), but no final ''
        split2 = hdrtext2.splitlines()
        strip1 = [line for line in split1 if not line.startswith('Status:')]
        strip2 = [line for line in split2 if not line.startswith('Status:')]
        if strip1 == strip2:
            self.trace('Same without Status')
            return True

        # try mismatch by message-id headers if either has one
        msgid1 = [line for line in split1 if line[:11].lower() == 'message-id:']
        msgid2 = [line for line in split2 if line[:11].lower() == 'message-id:']
        if (msgid1 or msgid2) and (msgid1 != msgid2):
            self.trace('Different Message-Id')
            return False

        # try full hdr parse and common headers if msgid missing or trash
        tryheaders  = ('From', 'To', 'Subject', 'Date')
        tryheaders += ('Cc', 'Return-Path', 'Received')
        msg1 = MailParser().parseHeaders(hdrtext1)
        msg2 = MailParser().parseHeaders(hdrtext2)
        for hdr in tryheaders:                          # poss multiple Received
            if msg1.get_all(hdr) != msg2.get_all(hdr):  # case insens, dflt None
                self.trace('Diff common headers')
                return False

        # all common hdrs match and don't have a diff message-id
        self.trace('Same common headers')
        return True

    def getPassword(self):
        """
        get POP password if not yet known
        not required until go to server
        from client-side file or subclass method
        """
        if not self.popPassword:
            try:
                localfile = open(mailconfig.poppasswdfile)
                self.popPassword = localfile.readline()[:-1]
                self.trace('local file password' + repr(self.popPassword))
            except:
                self.popPassword = self.askPopPassword()

    def askPopPassword(self):
        assert False, 'Subclass must define method'


################################################################################
# specialized subclasses
################################################################################

class MailFetcherConsole(MailFetcher):
    def askPopPassword(self):
        import getpass
        prompt = 'Password for %s on %s?' % (self.popUser, self.popServer)
        return getpass.getpass(prompt)

class SilentMailFetcher(SilentMailTool, MailFetcher):
    pass   # replaces trace
