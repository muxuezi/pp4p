import email.utils
class mailconfig: pass
From = 'PP4E@rmi.net'
mailconfig.myaddress = 'PP4E@rmi.net'; mailconfig.repliesCopyToAll = True


class C:
    def splitAddresses(self, field):
            """
            3.0: use comma separator for mutiple addrs in the GUI,
            and getaddresses to split correctly and allow for comma
            in the name parts of addresses (see notes at onReply);
            caveat: move to mailtools.mailParser so can be reused?
            """
            pairs = email.utils.getaddresses([field])                # [(name,addr)]
            return [email.utils.formataddr(pair) for pair in pairs]  # [name <addr>]

    def replyCopyTo(self, message):
        """
        3.0: replies copy all original recipients, by prefilling
        Cc header with all addreses in original To and Cc after 
        removing duplicates and new sender;  could decode i18 addrs 
        here, but the view window will decode to display (and send
        will reencode), and the unique set filtering here works 
        either way, though  the sender's address is assumed to be 
        in encoded form in mailconfig (else it is not removed here);
        empty To or Cc headers are okay: split returns empty lists;
        """
        if not mailconfig.repliesCopyToAll:
            # reply to sender only
            Cc = '?'
        else:
            # copy all original recipients (3.0)
            allRecipients = (self.splitAddresses(message.get('To', '')) + 
                             self.splitAddresses(message.get('Cc', ''))) 
            uniqueOthers  = set(allRecipients) - set([From])
            Cc = ', '.join(uniqueOthers)
        return Cc
 

        """
        sender = From
        recipHdrs   = (message.get(hdr, '') for hdr in ('To', 'Cc')) 
        joinHdrs    = ', '.join(filter(bool, recipHdrs))               # nonempties
        splitAddrs  = email.utils.getaddresses([joinHdrs])             # (name,addr)
        uniqueAddrs = {email.utils.formataddr(x) for x in splitAddrs}  # name <addr>
        othersAddrs = uniqueAddrs - set([sender])                      # less sender
        return ', '.join(othersAddrs)
        """


print(C().splitAddresses('a@a.a, b@b.b'))
print(C().splitAddresses(''))

def test(dict):
    print('=> [%s]' % C().replyCopyTo(dict))

test(dict(Cc='Bob <bob@bob.com>, lutz@rmi.net, PP4E@rmi.net', To='"spam,e" <eric@spam.com>, PP4E@rmi.net'))
test(dict(To='"spam,e" <eric@spam.com>, PP4E@rmi.net'))
test(dict(Cc='Bob <bob@bob.com>, lutz@rmi.net, PP4E@rmi.net'))
test(dict(To='PP4E@rmi.net, <lutz@rmi.net>, "spam" <spam@spam.com>'))
test(dict(To='PP4E@rmi.net'))
test(dict())




"""
    rcptpairs = email.utils.getaddresses([rcptorig])                 # [(name,addr)]

    rcptuniq  = {email.utils.formataddr(pair) for pair in rcptpairs} # {name <addr>}
    rcptuniq  = {map(email.utils.formataddr, rcptpairs)}             # {name <addr>} 
 
    rcptuniq  = {email.utils.formataddr(pair) 
                 for pair in email.utils.getaddresses([rcptjoin]) 

    rcptuniq  = {map(email.utils.formataddr, rcptpairs)}             # {name <addr>} 


    rcptuniq = set(map(email.utils.formataddr, rcptpairs)) - set(From)
"""