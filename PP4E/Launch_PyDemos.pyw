#!/usr/bin/python3
##################################################
# PyDemos + environment search/config first;
# run this if you haven't set up your paths yet;
# you still must install Python first, though;
#-------------------------------------------------
# Python 3.3 on Windows hack: needs python3 in #!,
# else this and Launcher code may use 2.X default
# if installed, unless PY_PYTHON is set in shell;
##################################################

import Launcher
Launcher.launchBookExamples(['PyDemos.pyw'], trace=False)
