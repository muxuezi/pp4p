"""
##############################################################################
manage message and header loads and context, but not GUI;
a MailFetcher, with a list of already loaded headers and messages;
the caller must handle any required threading or GUI interfaces;

3.0 change: use full message text  Unicode encoding name in local 
mailconfig module; decoding happens deep in mailtools, when a message
is fetched - mail text is always Unicode str from that point on;
this may change in a future Python/email: see Chapter 13 for details; 

3.0 change: inherits the new mailconfig.fetchlimit feature of mailtools,
which can be used to limit the maximum number of most recent headers or 
full mails (if no TOP) fetched on each load request; note that this 
feature is independent of the loadfrom used here to limit loads to 
newly-arrived mails only, though it is applied at the same time: at
most fetchlimit newly-arrived mails are loaded;

3.0 change: though unlikely, it's not impossible that a user may trigger a 
new fetch of a message that is currently being fetched in a thread, simply
by clicking the same message again (msg fetches, but not full index loads, 
may overlap with other fetches and sends); this seems to be thread safe here,
but can lead to redundant and possibly parallel downloads of the same mail 
which are pointless and seem odd (selecting all mails and pressing View 
twice downloads most messages twice!); fixed by keeping track of fetches in
progress in the main GUI thread so that this overlap is no longer possible:
a message being fetched disables any fetch request which it is part of, and
parallel fetches are still allowed as long as their targets do not intersect;
##############################################################################
"""

from PP4E.Internet.Email import mailtools
from popuputil import askPasswordWindow


class MessageInfo:
    """
    an item in the mail cache list
    """
    def __init__(self, hdrtext, size):
        self.hdrtext  = hdrtext            # fulltext is cached msg
        self.fullsize = size               # hdrtext is just the hdrs
        self.fulltext = None               # fulltext=hdrtext if no TOP


class MessageCache(mailtools.MailFetcher):
    """
    keep track of already loaded headers and messages;
    inherits server transfer methods from MailFetcher;
    useful in other apps: no GUI or thread assumptions;

    3.0: raw mail text bytes are decoded to str to be 
    parsed with Py3.1's email pkg and saved to files;
    uses the local mailconfig module's encoding setting;
    decoding happens automatically in mailtools on fetch;
    """
    def __init__(self):
        mailtools.MailFetcher.__init__(self)   # 3.0: inherits fetchEncoding
        self.msglist = []                      # 3.0: inherits fetchlimit

    def loadHeaders(self, forceReloads, progress=None):
        """
        three cases to handle here: the initial full load,
        load newly arrived, and forced reload after delete;
        don't refetch viewed msgs if hdrs list same or extended;
        retains cached msgs after a delete unless delete fails;
        2.1: does quick check to see if msgnums still in sync
        3.0: this is now subject to mailconfig.fetchlimit max;
        """
        if forceReloads:
            loadfrom = 1
            self.msglist = []                         # msg nums have changed
        else:
            loadfrom = len(self.msglist)+1            # continue from last load

        # only if loading newly arrived
        if loadfrom != 1:
            self.checkSynchError(self.allHdrs())      # raises except if bad

        # get all or newly arrived msgs
        reply = self.downloadAllHeaders(progress, loadfrom)
        headersList, msgSizes, loadedFull = reply

        for (hdrs, size) in zip(headersList, msgSizes):
            newmsg = MessageInfo(hdrs, size)
            if loadedFull:                            # zip result may be empty
                newmsg.fulltext = hdrs                # got full msg if no 'top'
            self.msglist.append(newmsg)

    def getMessage(self, msgnum):                     # get raw msg text
        cacheobj = self.msglist[msgnum-1]             # add to cache if fetched
        if not cacheobj.fulltext:                     # harmless if threaded
            fulltext = self.downloadMessage(msgnum)   # 3.0: simpler coding
            cacheobj.fulltext = fulltext
        return cacheobj.fulltext

    def getMessages(self, msgnums, progress=None):
        """
        prefetch full raw text of multiple messages, in thread;
        2.1: does quick check to see if msgnums still in sync;
        we can't get here unless the index list already loaded;
        """
        self.checkSynchError(self.allHdrs())          # raises except if bad
        nummsgs = len(msgnums)                        # adds messages to cache
        for (ix, msgnum) in enumerate(msgnums):       # some poss already there
             if progress: progress(ix+1, nummsgs)     # only connects if needed
             self.getMessage(msgnum)                  # but may connect > once

    def getSize(self, msgnum):                        # encapsulate cache struct
        return self.msglist[msgnum-1].fullsize        # it changed once already!

    def isLoaded(self, msgnum):
        return self.msglist[msgnum-1].fulltext

    def allHdrs(self):
        return [msg.hdrtext for msg in self.msglist]

    def deleteMessages(self, msgnums, progress=None):
        """
        if delete of all msgnums works, remove deleted entries
        from mail cache, but don't reload either the headers list
        or already viewed mails text: cache list will reflect the
        changed msg nums on server;  if delete fails for any reason,
        caller should forceably reload all hdrs next, because _some_
        server msg nums may have changed, in unpredictable ways;
        2.1: this now checks msg hdrs to detect out of synch msg
        numbers, if TOP supported by mail server; runs in thread
        """
        try:
            self.deleteMessagesSafely(msgnums, self.allHdrs(), progress)
        except mailtools.TopNotSupported:
            mailtools.MailFetcher.deleteMessages(self, msgnums, progress)

        # no errors: update index list
        indexed = enumerate(self.msglist)
        self.msglist = [msg for (ix, msg) in indexed if ix+1 not in msgnums]


class GuiMessageCache(MessageCache):
    """
    add any GUI-specific calls here so cache usable in non-GUI apps
    """

    def setPopPassword(self, appname):
        """
        get password from GUI here, in main thread
        forceably called from GUI to avoid pop ups in threads
        """
        if not self.popPassword:
            prompt = 'Password for %s on %s?' % (self.popUser, self.popServer)
            self.popPassword = askPasswordWindow(appname, prompt)

    def askPopPassword(self):
        """
        but don't use GUI pop up here: I am run in a thread!
        when tried pop up in thread, caused GUI to hang;
        may be called by MailFetcher superclass, but only
        if passwd is still empty string due to dialog close
        """
        return self.popPassword
