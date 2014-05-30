"""
###############################################################################
send messages, add attachments (see __init__ for docs, test)
###############################################################################
"""

import mailconfig                                      # client's mailconfig
import smtplib, os, mimetypes                          # mime: name to type
import email.utils, email.encoders                     # date string, base64
from .mailTool import MailTool, SilentMailTool         # 4E: package-relative

from email.message          import Message             # general message, obj->text
from email.mime.multipart   import MIMEMultipart       # type-specific messages
from email.mime.audio       import MIMEAudio           # format/encode attachments
from email.mime.image       import MIMEImage
from email.mime.text        import MIMEText
from email.mime.base        import MIMEBase
from email.mime.application import MIMEApplication     # 4E: use new app class


def fix_encode_base64(msgobj):
    """
    4E: workaround for a genuine bug in Python 3.1 email package that prevents
    mail text generation for binary parts encoded with base64 or other email 
    encodings;  the normal email.encoder run by the constructor leaves payload
    as bytes, even though it's encoded to base64 text form;  this breaks email 
    text generation which assumes this is text and requires it to be str;  net 
    effect is that only simple text part emails can be composed in Py 3.1 email
    package as is - any MIME-encoded binary part cause mail text generation to 
    fail;  this bug seems likely to go away in a future Python and email package,
    in which case this should become a no-op;  see Chapter 13 for more details;
    """

    linelen = 76  # per MIME standards
    from email.encoders import encode_base64

    encode_base64(msgobj)                # what email does normally: leaves bytes
    text = msgobj.get_payload()          # bytes fails in email pkg on text gen
    if isinstance(text, bytes):          # payload is bytes in 3.1, str in 3.2 alpha
        text = text.decode('ascii')      # decode to unicode str so text gen works

    lines = []                           # split into lines, else 1 massive line
    text  = text.replace('\n', '')       # no \n present in 3.1, but futureproof me!
    while text:
        line, text = text[:linelen], text[linelen:]
        lines.append(line)
    msgobj.set_payload('\n'.join(lines))


def fix_text_required(encodingname):
    """
    4E: workaround for str/bytes combination errors in email package;  MIMEText 
    requires different types for different Unicode encodings in Python 3.1, due
    to the different ways it MIME-encodes some types of text;  see Chapter 13;
    the only other alternative is using generic Message and repeating much code; 
    """ 
    from email.charset import Charset, BASE64, QP

    charset = Charset(encodingname)   # how email knows what to do for encoding
    bodyenc = charset.body_encoding   # utf8, others require bytes input data
    return bodyenc in (None, QP)      # ascii, latin1, others require str


class MailSender(MailTool):
    """
    send mail: format a message, interface with an SMTP server;
    works on any machine with Python+Inet, doesn't use cmdline mail;
    a nonauthenticating client: see MailSenderAuth if login required;
    4E: tracesize is num chars of msg text traced: 0=none, big=all;
    4E: supports Unicode encodings for main text and text parts;
    4E: supports header encoding, both full headers and email names;
    """
    def __init__(self, smtpserver=None, tracesize=256):
        self.smtpServerName = smtpserver or mailconfig.smtpservername
        self.tracesize = tracesize

    def sendMessage(self, From, To, Subj, extrahdrs, bodytext, attaches,
                                      saveMailSeparator=(('=' * 80) + 'PY\n'),
                                      bodytextEncoding='us-ascii',
                                      attachesEncodings=None):
        """
        format and send mail: blocks caller, thread me in a GUI;
        bodytext is main text part, attaches is list of filenames,
        extrahdrs is list of (name, value) tuples to be added;
        raises uncaught exception if send fails for any reason;
        saves sent message text in a local file if successful;

        assumes that To, Cc, Bcc hdr values are lists of 1 or more already
        decoded addresses (possibly in full name+<addr> format); client
        must parse to split these on delimiters, or use multiline input;
        note that SMTP allows full name+<addr> format in recipients;
        4E: Bcc addrs now used for send/envelope, but header is dropped;
        4E: duplicate recipients removed, else will get >1 copies of mail;
        caveat: no support for multipart/alternative mails, just /mixed;
        """

        # 4E: assume main body text is already in desired encoding;
        # clients can decode to user pick, default, or utf8 fallback;
        # either way, email needs either str xor bytes specifically; 

        if fix_text_required(bodytextEncoding): 
            if not isinstance(bodytext, str):
                bodytext = bodytext.decode(bodytextEncoding)
        else:
            if not isinstance(bodytext, bytes):
                bodytext = bodytext.encode(bodytextEncoding)

        # make message root
        if not attaches:
            msg = Message()
            msg.set_payload(bodytext, charset=bodytextEncoding)
        else:
            msg = MIMEMultipart()
            self.addAttachments(msg, bodytext, attaches,
                                     bodytextEncoding, attachesEncodings)

        # 4E: non-ASCII hdrs encoded on sends; encode just name in address,
        # else smtp may drop the message completely; encodes all envelope
        # To names (but not addr) also, and assumes servers will allow;
        # msg.as_string retains any line breaks added by encoding headers;
 
        hdrenc = mailconfig.headersEncodeTo or 'utf-8'        # default=utf8
        Subj = self.encodeHeader(Subj, hdrenc)                # full header
        From = self.encodeAddrHeader(From, hdrenc)            # email names
        To   = [self.encodeAddrHeader(T, hdrenc) for T in To] # each recip
        Tos  = ', '.join(To)                                  # hdr+envelope

        # add headers to root
        msg['From']    = From
        msg['To']      = Tos                        # poss many: addr list
        msg['Subject'] = Subj                       # servers reject ';' sept
        msg['Date']    = email.utils.formatdate()   # curr datetime, rfc2822 utc
        recip = To
        for name, value in extrahdrs:               # Cc, Bcc, X-Mailer, etc.
            if value:
                if name.lower() not in ['cc', 'bcc']:
                    value = self.encodeHeader(value, hdrenc)
                    msg[name] = value
                else:
                    value = [self.encodeAddrHeader(V, hdrenc) for V in value]
                    recip += value                     # some servers reject ['']
                    if name.lower() != 'bcc':          # 4E: bcc gets mail, no hdr
                        msg[name] = ', '.join(value)   # add commas between cc

        recip = list(set(recip))                       # 4E: remove duplicates
        fullText = msg.as_string()                     # generate formatted msg

        # sendmail call raises except if all Tos failed,
        # or returns failed Tos dict for any that failed

        self.trace('Sending to...' + str(recip))
        self.trace(fullText[:self.tracesize])                # SMTP calls connect
        server = smtplib.SMTP(self.smtpServerName, timeout=20)  # this may fail too
        self.getPassword()                                   # if srvr requires
        self.authenticateServer(server)                      # login in subclass
        try:
            failed = server.sendmail(From, recip, fullText)  # except or dict
        except:
            server.close()                                   # 4E: quit may hang!
            raise                                            # reraise except
        else:
            server.quit()                                    # connect + send OK
        self.saveSentMessage(fullText, saveMailSeparator)    # 4E: do this first 
        if failed:
            class SomeAddrsFailed(Exception): pass
            raise SomeAddrsFailed('Failed addrs:%s\n' % failed)
        self.trace('Send exit')

    def addAttachments(self, mainmsg, bodytext, attaches,
                                      bodytextEncoding, attachesEncodings):
        """
        format a multipart message with attachments;
        use Unicode encodings for text parts if passed;
        """
        # add main text/plain part
        msg = MIMEText(bodytext, _charset=bodytextEncoding)
        mainmsg.attach(msg)

        # add attachment parts
        encodings = attachesEncodings or (['us-ascii'] * len(attaches))
        for (filename, fileencode) in zip(attaches, encodings):
            # filename may be absolute or relative
            if not os.path.isfile(filename):             # skip dirs, etc.
                continue

            # guess content type from file extension, ignore encoding
            contype, encoding = mimetypes.guess_type(filename)
            if contype is None or encoding is not None:  # no guess, compressed?
                contype = 'application/octet-stream'     # use generic default
            self.trace('Adding ' + contype)

            # build sub-Message of appropriate kind
            maintype, subtype = contype.split('/', 1)
            if maintype == 'text':                       # 4E: text needs encoding
                if fix_text_required(fileencode):        # requires str or bytes
                    data = open(filename, 'r', encoding=fileencode)
                else:
                    data = open(filename, 'rb')
                msg = MIMEText(data.read(), _subtype=subtype, _charset=fileencode)
                data.close()

            elif maintype == 'image':
                data = open(filename, 'rb')              # 4E: use fix for binaries
                msg  = MIMEImage(
                       data.read(), _subtype=subtype, _encoder=fix_encode_base64)
                data.close()

            elif maintype == 'audio':
                data = open(filename, 'rb')
                msg  = MIMEAudio(
                       data.read(), _subtype=subtype, _encoder=fix_encode_base64)
                data.close()

            elif maintype == 'application':              # new  in 4E
                data = open(filename, 'rb')
                msg  = MIMEApplication(
                       data.read(), _subtype=subtype, _encoder=fix_encode_base64)
                data.close()

            else:
                data = open(filename, 'rb')              # application/* could 
                msg  = MIMEBase(maintype, subtype)       # use this code too
                msg.set_payload(data.read())
                data.close()                             # make generic type
                fix_encode_base64(msg)                   # was broken here too!
               #email.encoders.encode_base64(msg)        # encode using base64

            # set filename and attach to container
            basename = os.path.basename(filename)
            msg.add_header('Content-Disposition',
                           'attachment', filename=basename)
            mainmsg.attach(msg)

        # text outside mime structure, seen by non-MIME mail readers
        mainmsg.preamble = 'A multi-part MIME format message.\n'
        mainmsg.epilogue = ''  # make sure message ends with a newline

    def saveSentMessage(self, fullText, saveMailSeparator):
        """
        append sent message to local file if send worked for any;
        client: pass separator used for your application, splits;
        caveat: user may change the file at same time (unlikely);
        """
        try:
            sentfile = open(mailconfig.sentmailfile, 'a', 
                                  encoding=mailconfig.fetchEncoding)    # 4E
            if fullText[-1] != '\n': fullText += '\n'
            sentfile.write(saveMailSeparator)
            sentfile.write(fullText)
            sentfile.close()
        except:
            self.trace('Could not save sent message')    # not a show-stopper

    def encodeHeader(self, headertext, unicodeencoding='utf-8'):
        """
        4E: encode composed non-ascii message headers content per both email
        and Unicode standards, according to an optional user setting or UTF-8;
        header.encode adds line breaks in header string automatically if needed; 
        """
        try:
            headertext.encode('ascii')
        except:
            try:
                hdrobj = email.header.make_header([(headertext, unicodeencoding)])
                headertext = hdrobj.encode()
            except:
                pass         # auto splits into multiple cont lines if needed
        return headertext    # smtplib may fail if it won't encode to ascii

    def encodeAddrHeader(self, headertext, unicodeencoding='utf-8'):
        """
        4E: try to encode non-ASCII names in email addresess per email, MIME, 
        and Unicode standards; if this fails drop name and use just addr part;
        if cannot even get addresses, try to decode as a whole, else smtplib 
        may run into errors when it tries to encode the entire mail as ASCII;
        utf-8 default should work for most, as it formats code points broadly;

        inserts newlines if too long or hdr.encode split names to multiple lines,
        but this may not catch some lines longer than the cutoff (improve me); 
        as used, Message.as_string formatter won't try to break lines further;
        see also decodeAddrHeader in mailParser module for the inverse of this;
        """
        try:
            pairs = email.utils.getaddresses([headertext])   # split addrs + parts
            encoded = []
            for name, addr in pairs:
                try:
                    name.encode('ascii')         # use as is if okay as ascii
                except UnicodeError:             # else try to encode name part
                    try:
                        uni  = name.encode(unicodeencoding) 
                        hdr  = email.header.make_header([(uni, unicodeencoding)])
                        name = hdr.encode()
                    except:
                        name = None              # drop name, use address part only
                joined = email.utils.formataddr((name, addr))  # quote name if need
                encoded.append(joined)

            fullhdr = ', '.join(encoded)
            if len(fullhdr) > 72 or '\n' in fullhdr:      # not one short line?
                fullhdr = ',\n '.join(encoded)            # try multiple lines
            return fullhdr
        except:
            return self.encodeHeader(headertext)

    def authenticateServer(self, server):
        pass  # no login required for this server/class

    def getPassword(self):
        pass  # no login required for this server/class


################################################################################
# specialized subclasses
################################################################################

class MailSenderAuth(MailSender):
    """
    use for servers that require login authorization;
    client: choose MailSender or MailSenderAuth super
    class based on mailconfig.smtpuser setting (None?)
    """
    smtpPassword = None    # 4E: on class, not self, shared by poss N instances

    def __init__(self, smtpserver=None, smtpuser=None):
        MailSender.__init__(self, smtpserver)
        self.smtpUser = smtpuser or mailconfig.smtpuser
        # self.smtpPassword = None   # 4E: makes pyMailGUI ask for each send!

    def authenticateServer(self, server):
        server.login(self.smtpUser, self.smtpPassword)

    def getPassword(self):
        """
        get SMTP auth password if not yet known;
        may be called by superclass auto, or client manual:
        not needed until send, but don't run in GUI thread;
        get from client-side file or subclass method
        """
        if not self.smtpPassword:
            try:
                localfile = open(mailconfig.smtppasswdfile)
                MailSenderAuth.smtpPassword = localfile.readline()[:-1]     # 4E
                self.trace('local file password' + repr(self.smtpPassword))
            except:
                MailSenderAuth.smtpPassword = self.askSmtpPassword()        # 4E

    def askSmtpPassword(self):
        assert False, 'Subclass must define method'

class MailSenderAuthConsole(MailSenderAuth):
    def askSmtpPassword(self):
        import getpass
        prompt = 'Password for %s on %s?' % (self.smtpUser, self.smtpServerName)
        return getpass.getpass(prompt)

class SilentMailSender(SilentMailTool, MailSender):
    pass   # replaces trace
