"""
####################################################################
Send email by building a URL like this from inputs:
http://servername/pathname/
          onEditPageSend.py?site=smtp.rmi.net&
                            From=lutz@rmi.net&
                            To=lutz@rmi.net&
                            Subject=test+url&
                            text=Hello+Mark;this+is+Mark
####################################################################
"""
from urllib.request import urlopen
from urllib.parse   import quote_plus

url = 'http://localhost:8000/cgi-bin/onEditPageSend.py'
url += '?site=%s'    % quote_plus(input('Site>'))
url += '&From=%s'    % quote_plus(input('From>'))
url += '&To=%s'      % quote_plus(input('To  >'))
url += '&Subject=%s' % quote_plus(input('Subj>'))
url += '&text=%s'    % quote_plus(input('text>'))    # or input loop

print('Reply html:')
print(urlopen(url).read().decode())   # confirmation or error page HTML
