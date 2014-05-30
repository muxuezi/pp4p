#############################################################################
# Isolate all imports of modules that live outside of the PyMailCgi 
# directory, so that their location must only be changed here if moved;
# we use a custom version of mailconfig.py here: a pymailgui2 subset
#############################################################################
     
#from  PP3E.Internet.Email.PyMailGui2 import mailconfig

import mailconfig
from  PP3E.Internet.Email import mailtools  # PP3E/.. must be on your PYTHONPATH
