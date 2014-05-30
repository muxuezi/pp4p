fetchEncoding = 'utf8'      # 'latin1' works for msg2

def decodeToUnicode(messageBytes):
    try:
        text = [line.decode(fetchEncoding) for line in messageBytes]
    except UnicodeDecodeError:
        # return headers + error message, else except may kill client;
        # headers must still be decodeable per ascii or platform default
        blankline = messageBytes.index(b'')
        hdrsonly  = messageBytes[:blankline]
        try:
            text = [line.decode('ascii') for line in hdrsonly]
        except UnicodeDecodeError:
            text = [line.decode() for line in hdrsonly]
        text += ['', '--Sorry: mailtools cannot decode this mail content!--']
    return text

msg1 = [b'xxx', b'yyy', b'zzz', b'', b'mmm', b'nnn']
msg2 = [b'xxx', b'yyy', b'zzz', b'', b'm\xe4m', b'nnn']

print('\n'.join(decodeToUnicode(msg1)))
print('-'*75)
print('\n'.join(decodeToUnicode(msg2)))