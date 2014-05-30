fetchEncoding = 'utf8'      # 'latin1' works for msg2

def decodeToUnicode(messageBytes):
        text = None
        kinds =  [fetchEncoding]                  # try user setting first
########kinds += ['ascii', 'latin1', 'utf8']      # then try common types?
        for kind in kinds:                        # may cause mail saves to fail
            try:
                text = [line.decode(kind) for line in messageBytes]
                break
            except UnicodeDecodeError:
                pass

        if not text:
            # try returning headers + error msg, else except may kill client;
            # still try to decode headers per ascii, other, platform default;

            blankline = messageBytes.index(b'')
            hdrsonly  = messageBytes[:blankline]
            commons   = ['ascii', 'latin1', 'utf8']
            for common in commons:
                try:
                    text = [line.decode(common) for line in hdrsonly] 
                    break
                except UnicodeDecodeError:
                    pass
            else:                                                  # none worked
                try:
                    text = [line.decode() for line in hdrsonly]    # platform dflt?
                except UnicodeDecodeError:
                    text = ['From: (sender of unknown Unicode format headers)']
            text += ['', '--Sorry: mailtools cannot decode this mail content!--']
        return text


msg1 = [b'xxx', b'yyy', b'zzz', b'', b'mmm', b'nnn']
msg2 = [b'xxx', b'yyy', b'zzz', b'', b'm\xe4m', b'nnn']
msg3 = [b'xxx', b'yyy', b'zzz', b'', b'm\xFFm', b'nnn']

print('\n'.join(decodeToUnicode(msg1)))
print('-'*75)
print('\n'.join(decodeToUnicode(msg2)))
print('-'*75)
print('\n'.join(decodeToUnicode(msg3)))