# test i18n header decoding/encoding methods' logic

import sys
sys.path.insert(0, '..')  # for package relative inoports

from tkinter.scrolledtext import ScrolledText
t = ScrolledText(width=170, height=40)

from mailtools.mailParser import MailParser
decodeHeader = MailParser().decodeHeader
decodeAddrHeader = MailParser().decodeAddrHeader

from mailtools.mailSender import MailSender
encodeHeader = MailSender().encodeHeader
encodeAddrHeader = MailSender().encodeAddrHeader


subjs = [
'=?koi8-r?B?79DUyc3J2sHDydEgxNfJ1sXOydEgxMXOxdbO2cgg0M/Uz8vP1yDJINPO?=',
'=?gb2312?b?0sDC7cqooba0q7Kl0+vWxtf3obdF1ty/r7XaMjc4xtotx7/Hv8GqytYgtPPR89PrsbG+qcyowarxx7Ty1Oy089DNuN/H5c/uxL8=?=',
'=?windows-1252?Q?Conhe=E7a_mais_uma_novidade_LC2!_-_Folhinhas_&_calend=E1rios_2011?=',
'=?UTF-8?Q?Introducing=20Top=20Values=3A=20A=20Special=20Selection=20of=20Great=20Money=20Savers?=',
'spam, spam, and spam']

addrs = [
'=?koi8-r?B?98HbIMHO1MnL0snaydPO2cog28HO0w==?= <l2000ena@almi.ru>',
'"=?gb2312?b?ZXdlZWtseUBpbWFzY2hpbmEuY29t?=" <eweekly@imaschina.com>',
'"=?windows-1252?Q?LC=B2_-_Personaliza=E7=F5es_Especiais?=" <contato@sosgrupo.com.br>',
'"=?UTF-8?Q?Walmart?=" <newsletters@walmart.com>', 

'"Bob Smith" <bob@bob.com>',
'"Smith, Bob" <bob@bob.com>',           # fails: "SmithBob" bob@bob.com'
'"Bob" <bob@bob.com>',
'"Bob;Sm@ith,er!" <bob@bob.com>',

'Bob Smith <bob@bob.com>',
'Bob <bob@bob.com>',
'bob@bob.com',
]


t.insert('end', '\n' + '-'*100 + '\n\n')
t.insert('end', '[test decoding subjs to text/str (recvs)]\n\n')
for subj in subjs:
    t.insert('end', subj + '\n')
    t.insert('end', decodeHeader(subj) + '\n\n')

t.insert('end', '\n' + '-'*100 + '\n\n')
t.insert('end', '[test decoding addrs to text/str (recvs)]\n\n')
for addr in addrs:
    t.insert('end', addr + '\n')
    t.insert('end', decodeAddrHeader(addr) + '\n')           # single addr
    t.insert('end', decodeAddrHeader(addr + ', ' + addr))    # multiple addrs
    t.insert('end', '\n\n')


t.insert('end', '\n' + '-'*100 + '\n\n')
t.insert('end', '[test encoding subjs, and decoding back again (sends + later recvs)]\n\n')
for subj in subjs:
    dec = decodeHeader(subj)        # i18n(1) -> str
    enc = encodeHeader(dec)         # str     -> i18n(2)
    rec = decodeHeader(enc)         # i18n(2) -> str
    t.insert('end', subj + '\n')
    t.insert('end', dec  + '\n')
    t.insert('end', enc  + '\n')
    t.insert('end', rec  + '\n')
    t.insert('end', 'encoded: ' + ('same' if enc == subj else 'differs') + '\n')
    t.insert('end', 'decoded: ' + ('same' if rec == dec  else '**differs**') + '\n\n')


t.insert('end', '\n' + '-'*100 + '\n\n')
t.insert('end', '[test encoding addrs, and decoding back again (sends + later recvs)]\n\n')
for addr in addrs:
    dec  = decodeAddrHeader(addr)    # i18n(1) -> str
    enc  = encodeAddrHeader(dec)     # str     -> i18n(2)
    rec  = decodeAddrHeader(enc)     # i18n(2) -> str
    t.insert('end', addr + '\n')
    t.insert('end', dec  + '\n')
    t.insert('end', enc  + '\n')
    t.insert('end', rec  + '\n')
    t.insert('end', 'encoded: ' + ('same' if enc == addr else 'differs') + '\n')
    t.insert('end', 'decoded: ' + ('same' if rec == dec  else '**differs**') + '\n\n')


t.insert('end', '\n' + '-'*100 + '\n\n')
t.insert('end', '[test encoding addrs, multi/mixed addrs\n\n')
for (ix, addr) in enumerate(addrs): # multi addrs, mix encooding
    addr += ', ' + (addr if ix == 0 else addrs[ix-1])
    dec  = decodeAddrHeader(addr)    # i18n(1) -> str
    enc  = encodeAddrHeader(dec)     # str     -> i18n(2)
    rec  = decodeAddrHeader(enc)     # i18n(2) -> str
    t.insert('end', addr + '\n')
    t.insert('end', dec  + '\n')
    t.insert('end', enc  + '\n')
    t.insert('end', rec  + '\n')
    t.insert('end', 'encoded: ' + ('same' if enc == addr else 'differs') + '\n')
    t.insert('end', 'decoded: ' + ('same' if rec == dec  else '**differs**') + '\n\n')


t.pack()
t.mainloop()