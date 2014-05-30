# no output for 10 seconds unless Python -u flag used or sys.stdout.flush()
# but writer's output appears here every 2 seconds when either option is used
from __future__ import print_function
import os
for line in os.popen('python -u pipe-unbuff-writer.py'):    # iterator reads lines
    print(line, end='')                                     # blocks without -u!
