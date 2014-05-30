# to run without PYTHONPATH setup (e.g., desktop shortcut)

# Python 3.3 hack: sets new Windows launcher's default to 3.X for spawnee;
# subprocess inherits this setting when opened with py launcher via registry;
# else may be run by an installed 2.X default if PY_PYTHON not set in shell;
# note that #!/usr/bin/python3 not required, as this file's code is 2.X+3.X;

import os                                         # Launcher.py is overkill
os.environ['PY_PYTHON'] = '3'                     # Py3.3 Windows laucher hack
os.environ['PYTHONPATH'] = r'..\..\..\..\..'      # hmm; generalize me
os.system('PyMailGui.py')                         # inherits path env var
