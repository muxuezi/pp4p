import sys
from PP4E.launchmodes import QuietPortableLauncher

numclients = 8
def start(cmdline): 
    QuietPortableLauncher(cmdline, cmdline)()

# start('echo-server.py')              # spawn server locally if not yet started

args = ' '.join(sys.argv[1:])          # pass server name if running remotely
for i in range(numclients):
    start('echo-client.py %s' % args)  # spawn 8? clients to test the server
