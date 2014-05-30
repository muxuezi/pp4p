# view the sys.modules table in FormGui (no, really!)
     
class modrec:
    def todict(self, value):
        return value.__dict__     # not dir(value): need dict
    def fromdict(self, value):
        assert False, 'Module updates not supported'
     
import sys
from formgui import FormGui
from formtable import Table
FormGui(Table(sys.modules, modrec())).mainloop()
