# GUI reader side: route spawned program standard output to a GUI window

from PP4E.Gui.Tools.guiStreams import redirectedGuiShellCmd       # uses GuiOutput
redirectedGuiShellCmd('python -u pipe-nongui.py')                 # -u: unbuffered
