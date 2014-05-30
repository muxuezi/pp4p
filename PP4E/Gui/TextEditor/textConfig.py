"""
PyEdit (textEditor.py) user startup configuration module;
"""

#----------------------------------------------------------------------------------
# General configurations
# comment-out any setting in this section to accept Tk or program defaults;
# can also change font/colors from GUI menus, and resize window when open;
# imported via search path: can define per client app, skipped if not on the path;
#----------------------------------------------------------------------------------

# initial font                      # family, size, style
font = ('courier', 9, 'normal')     # e.g., style: 'bold italic'

# initial color                     # default=white, black
bg = 'lightcyan'                    # colorname or RGB hexstr
fg = 'black'                        # e.g., 'powder blue', '#690f96'

# initial size
height = 20                         # Tk default: 24 lines
width  = 80                         # Tk default: 80 characters

# search case-insensitive
caseinsens = True                   # default=1/True (on)

#----------------------------------------------------------------------------------
# 2.1: Unicode encoding behavior and names for file opens and saves;
# attempts the cases listed below in the order shown, until the first one 
# that works; set all variables to false/empty/0 to use your platform's default
# (which is 'utf-8' on Windows, or 'ascii' or 'latin-1' on others like Unix);
# savesUseKnownEncoding: 0=No, 1=Yes for Save only, 2=Yes for Save and SaveAs;
# imported from this file always: sys.path if main, else package relative;
#----------------------------------------------------------------------------------

                       # 1) tries internally known type first (e.g., email charset)
opensAskUser = True    # 2) if True, try user input next (prefill with defaults)
opensEncoding = ''     # 3) if nonempty, try this encoding next: 'latin-1', 'cp500'
                       # 4) tries sys.getdefaultencoding() platform default next 
                       # 5) uses binary mode bytes and Tk policy as the last resort

savesUseKnownEncoding = 1    # 1) if > 0, try known encoding from last open or save
savesAskUser = True          # 2) if True, try user input next (prefill with known?)
savesEncoding = ''           # 3) if nonempty, try this encoding next: 'utf-8', etc
                             # 4) tries sys.getdefaultencoding() as a last resort
