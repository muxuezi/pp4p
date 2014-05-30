"""
user configuration settings for various email programs (PyMailCGI version);
email scripts get their server names and other email config options from
this module: change me to reflect your machine names, sig, and preferences;
"""

from PP4E.Internet.Email.mailconfig import *     # reuse ch13 configs
fetchlimit = 50    # 4E: maximum number headers/emails to fetch on loads (dflt=25)
