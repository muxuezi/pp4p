import email.header

def decodeHeader(rawheader):
    if rawheader[:2] != '=?':
        return rawheader
    else:
        try:
            hdr, enc = email.header.decode_header(rawheader)[0]
            return hdr.decode(enc)
        except:
            return rawheader

def encodeHeader(headertext, unicodeencoding=''):
    if not unicodeencoding:
        return headertext 
    else:
        try:
            hdrobj = email.header.make_header([(headertext, unicodeencoding)])
            return hdrobj.encode()
        except:
            return headertext

raw = '=?UTF-8?Q?Introducing=20Top=20Values=3A=20A=20Special=20Selection=20of=20Great=20Money=20Savers?='
print(decodeHeader(raw))
print(decodeHeader('subject line'))

text = b'A\xc4B\xe4C'
print(encodeHeader(text, 'latin-1'))
print(encodeHeader('subject line'))
