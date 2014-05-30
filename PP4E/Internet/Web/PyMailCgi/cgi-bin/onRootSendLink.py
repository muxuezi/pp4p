#!/usr/bin/python
"""
################################################################################
On 'send' click in main root window: display composition page
################################################################################
"""
import commonhtml
from externs import mailconfig

commonhtml.editpage(kind='Write', headers={'From': mailconfig.myaddress})
