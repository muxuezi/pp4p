"""
###############################################################################
parsing and attachment extract, analyse, save (see __init__ for docs, test)
###############################################################################
"""

import os, mimetypes, sys                       # mime: map type to name
import email.parser                             # parse text to Message object
import email.header                             # 4E: headers decode/encode 
import email.utils                              # 4E: addr header parse/decode
from email.message import Message               # Message may be traversed
from .mailTool import MailTool                  # 4E: package-relative

class MailParser(MailTool):
    """
    methods for parsing message text, attachments

    subtle thing: Message object payloads are either a simple
    string for non-multipart messages, or a list of Message
    objects if multipart (possibly nested); we don't need to
    distinguish between the two cases here, because the Message
    walk generator always returns self first, and so works fine
    on non-multipart messages too (a single object is walked);

    for simple messages, the message body is always considered
    here to be the sole part of the mail;  for multipart messages,
    the parts list includes the main message text, as well as all
    attachments;  this allows simple messages not of type text to
    be handled like attachments in a UI (e.g., saved, opened);
    Message payload may also be None for some oddball part types;

    4E note: in Py 3.1, text part payloads are returned as bytes 
    for decode=1, and might be str otherwise; in mailtools, text
    is stored as bytes for file saves, but main-text bytes payloads
    are decoded to Unicode str per mail header info or platform 
    default+guess; clients may need to convert other payloads:
    PyMailGUI uses headers to decode parts saved to binary files;

    4E supports fetched message header auto-decoding per its own
    content, both for general headers such as Subject, as well as
    for names in address header such as From and To; client must 
    request this after parse, before display: parser doesn't decode;
    """

    def walkNamedParts(self, message):
        """
        generator to avoid repeating part naming logic;
        skips multipart headers, makes part filenames;
        message is already parsed email.message.Message object;
        doesn't skip oddball types: payload may be None, must
        handle in part saves; some others may warrant skips too;
        """
        for (ix, part) in enumerate(message.walk()):    # walk includes message
            fulltype = part.get_content_type()          # ix includes parts skipped
            maintype = part.get_content_maintype()
            if maintype == 'multipart':                 # multipart/*: container
                continue                                
            elif fulltype == 'message/rfc822':          # 4E: skip message/rfc822
                continue                                # skip all message/* too?
            else:
                filename, contype = self.partName(part, ix)
                yield (filename, contype, part)

    def partName(self, part, ix):
        """
        extract filename and content type from message part;
        filename: tries Content-Disposition, then Content-Type
        name param, or generates one based on mimetype guess;
        """
        filename = part.get_filename()                # filename in msg hdrs?
        contype  = part.get_content_type()            # lowercase maintype/subtype
        if not filename:
            filename = part.get_param('name')         # try content-type name
        if not filename:
            if contype == 'text/plain':               # hardcode plain text ext
                ext = '.txt'                          # else guesses .ksh!
            else:
                ext = mimetypes.guess_extension(contype)
                if not ext: ext = '.bin'              # use a generic default
            filename = 'part-%03d%s' % (ix, ext)
        return (filename, contype)

    def saveParts(self, savedir, message):
        """
        store all parts of a message as files in a local directory;
        returns [('maintype/subtype', 'filename')] list for use by
        callers, but does not open any parts or attachments here;
        get_payload decodes base64, quoted-printable, uuencoded data;
        mail parser may give us a None payload for oddball types we
        probably should skip over: convert to str here to be safe;
        """
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        partfiles = []
        for (filename, contype, part) in self.walkNamedParts(message):
            fullname = os.path.join(savedir, filename)
            fileobj  = open(fullname, 'wb')             # use binary mode
            content  = part.get_payload(decode=1)       # decode base64,qp,uu
            if not isinstance(content, bytes):          # 4E: need bytes for rb
                content = b'(no content)'               # decode=1 returns bytes,
            fileobj.write(content)                      # but some payloads None
            fileobj.close()                             # 4E: not str(content)
            partfiles.append((contype, fullname))       # for caller to open
        return partfiles

    def saveOnePart(self, savedir, partname, message):
        """
        ditto, but find and save just one part by name
        """
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        fullname = os.path.join(savedir, partname)
        (contype, content) = self.findOnePart(partname, message)
        if not isinstance(content, bytes):          # 4E: need bytes for rb
            content = b'(no content)'               # decode=1 returns bytes,
        open(fullname, 'wb').write(content)         # but some payloads None
        return (contype, fullname)                  # 4E: not str(content)

    def partsList(self, message):
        """"
        return a list of filenames for all parts of an
        already parsed message, using same filename logic
        as saveParts, but do not store the part files here
        """
        validParts = self.walkNamedParts(message)
        return [filename for (filename, contype, part) in validParts]

    def findOnePart(self, partname, message):
        """
        find and return part's content, given its name;
        intended to be used in conjunction with partsList;
        we could also mimetypes.guess_type(partname) here;
        we could also avoid this search by saving in dict;
        4E: content may be str or bytes--convert as needed;
        """
        for (filename, contype, part) in self.walkNamedParts(message):
            if filename == partname:
                content = part.get_payload(decode=1)          # does base64,qp,uu
                return (contype, content)                     # may be bytes text

    def decodedPayload(self, part, asStr=True):
        """
        4E: decode text part bytes to Unicode str for display, line wrap, 
        etc.; part is a Message; (decode=1) undoes MIME email encodings 
        (base64, uuencode, qp), bytes.decode() performs additional Unicode 
        text string decodings; tries charset encoding name in message 
        headers first (if present, and accurate), then tries platform 
        defaults and a few guesses before giving up with error string;
        """
        payload = part.get_payload(decode=1)           # payload may be bytes
        if asStr and isinstance(payload, bytes):       # decode=1 returns bytes
            tries = []
            enchdr = part.get_content_charset()        # try msg headers first!
            if enchdr:
                tries += [enchdr]                      # try headers first   
            tries += [sys.getdefaultencoding()]        # same as bytes.decode()
            tries += ['latin1', 'utf8']                # try 8-bit, incl ascii
            for trie in tries:                         # try utf8 (windows dflt)
                try:
                    payload = payload.decode(trie)     # give it a shot, eh?
                    break
                except (UnicodeError, LookupError):    # lookuperr: bad name
                    pass
            else:
                payload = '--Sorry: cannot decode Unicode text--' 
        return payload

    def findMainText(self, message, asStr=True):
        """
        for text-oriented clients, return first text part's str;
        for the payload of a simple message, or all parts of
        a multipart message, looks for text/plain, then text/html,
        then text/*, before deducing that there is no text to
        display;  this is a heuristic, but covers most simple,
        multipart/alternative, and multipart/mixed messages;
        content-type defaults to text/plain if not in simple msg;

        handles message nesting at top level by walking instead
        of list scans;  if non-multipart but type is text/html,
        returns the HTML as the text with an HTML type: caller
        may open in web browser, extract plain text, etc;  if 
        nonmultipart and not text, there is  no text to display: 
        save/open message content in UI; caveat: does not try 
        to concatenate multiple inline text/plain parts if any;
        4E: text payloads may be bytes--decodes to str here;
        4E: asStr=False to get raw bytes for HTML file saves;
        """

        # try to find a plain text
        for part in message.walk():                            # walk visits message
            type = part.get_content_type()                     # if nonmultipart
            if type == 'text/plain':                           # may be base64,qp,uu
                return type, self.decodedPayload(part, asStr)  # bytes to str too?

        # try to find an HTML part
        for part in message.walk():
            type = part.get_content_type()                     # caller renders html
            if type == 'text/html':
                return type, self.decodedPayload(part, asStr)

        # try any other text type, including XML
        for part in message.walk():
            if part.get_content_maintype() == 'text':
                return part.get_content_type(), self.decodedPayload(part, asStr)

        # punt: could use first part, but it's not marked as text
        failtext = '[No text to display]' if asStr else b'[No text to display]'
        return 'text/plain', failtext

    def decodeHeader(self, rawheader):
        """
        4E: decode existing i18n message header text per both email and Unicode 
        standards, according to its content; return as is if unencoded or fails;
        client must call this to display: parsed Message object does not decode;
        i18n header example: '=?UTF-8?Q?Introducing=20Top=20Values=20..Savers?=';
        i18n header example: 'Man where did you get that =?UTF-8?Q?assistant=3F?=';

        decode_header handles any line breaks in header string automatically, may
        return multiple parts if any substrings of hdr are encoded, and returns all
        bytes in parts list if any encodings found (with unencoded parts encoded as
        raw-unicode-escape and enc=None) but returns a single part with enc=None
        that is str instead of bytes in Py3.1 if the entire header is unencoded 
        (must handle mixed types here); see Chapter 13 for more details/examples;

        the following first attempt code was okay unless any encoded substrings, or
        enc was returned as None (raised except which returned rawheader unchanged):
        hdr, enc = email.header.decode_header(rawheader)[0]
        return hdr.decode(enc) # fails if enc=None: no encoding or encoded substrs
        """
        try:
            parts = email.header.decode_header(rawheader)
            decoded = []
            for (part, enc) in parts:                      # for all substrings
                if enc == None:                            # part unencoded?
                    if not isinstance(part, bytes):        # str: full hdr unencoded
                        decoded += [part]                  # else do unicode decode
                    else:
                        decoded += [part.decode('raw-unicode-escape')]
                else:
                    decoded += [part.decode(enc)]
            return ' '.join(decoded)
        except:
            return rawheader         # punt!

    def decodeAddrHeader(self, rawheader):
        """
        4E: decode existing i18n address header text per email and Unicode,
        according to its content; must parse out first part of email address
        to get i18n part: '"=?UTF-8?Q?Walmart?=" <newsletters@walmart.com>';
        From will probably have just 1 addr, but To, Cc, Bcc may have many;

        decodeHeader handles nested encoded substrings within an entire hdr,
        but we can't simply call it for entire hdr here because it fails if 
        encoded name substring ends in " quote instead of whitespace or endstr; 
        see also encodeAddrHeader in mailSender module for the inverse of this;

        the following first attempt code failed to handle encoded substrings in
        name, and raised exc for unencoded bytes parts if any encoded substrings;
        namebytes, nameenc = email.header.decode_header(name)[0]  (do email+MIME)
        if nameenc: name = namebytes.decode(nameenc)              (do Unicode?)
        """
        try:
            pairs = email.utils.getaddresses([rawheader])  # split addrs and parts
            decoded = []                                   # handles name commas 
            for (name, addr) in pairs:
                try:
                    name = self.decodeHeader(name)                # email+MIME+Uni
                except:
                    name = None   # but uses encooded name if exc in decodeHeader
                joined = email.utils.formataddr((name, addr))     # join parts
                decoded.append(joined)
            return ', '.join(decoded)                             # >= 1 addrs 
        except:
            return self.decodeHeader(rawheader)    # try decoding entire string

    def splitAddresses(self, field):
        """
        4E: use comma separator for multiple addrs in the UI, and 
        getaddresses to split correctly and allow for comma in the 
        name parts of addresses; used by PyMailGUI to split To, Cc, 
        Bcc as needed for user inputs and copied headers;  returns 
        empty list if field is empty, or any exception occurs;
        """
        try:
            pairs = email.utils.getaddresses([field])                # [(name,addr)]
            return [email.utils.formataddr(pair) for pair in pairs]  # [name <addr>]
        except:
            return ''   # syntax error in user-entered field?, etc.

    # returned when parses fail
    errorMessage = Message()
    errorMessage.set_payload('[Unable to parse message - format error]')

    def parseHeaders(self, mailtext):
        """
        parse headers only, return root email.message.Message object
        stops after headers parsed, even if nothing else follows (top)
        email.message.Message object is a mapping for mail header fields
        payload of message object is None, not raw body text
        """
        try:
            return email.parser.Parser().parsestr(mailtext, headersonly=True)
        except:
            return self.errorMessage

    def parseMessage(self, fulltext):
        """
        parse entire message, return root email.message.Message object
        payload of message object is a string if not is_multipart()
        payload of message object is more Messages if multiple parts
        the call here same as calling email.message_from_string()
        """
        try:
            return email.parser.Parser().parsestr(fulltext)       # may fail!
        except:
            return self.errorMessage     # or let call handle? can check return

    def parseMessageRaw(self, fulltext):
        """
        parse headers only, return root email.message.Message object
        stops after headers parsed, for efficiency (not yet used here)
        payload of message object is raw text of mail after headers
        """
        try:
            return email.parser.HeaderParser().parsestr(fulltext)
        except:
            return self.errorMessage
