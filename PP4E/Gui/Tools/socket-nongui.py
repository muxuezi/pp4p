# non-GUI side: connect stream to socket and proceed normally

import time, sys
if len(sys.argv) > 1:                            # link to gui only if requested
    from socket_stream_redirect0 import *        # connect my sys.stdout to socket
    redirectOut()                                # GUI must be started first as is

# non-GUI code
while True:                                      # print data to stdout:
    print(time.asctime())                        # sent to GUI process via socket
    sys.stdout.flush()                           # must flush to send: buffered!
    time.sleep(2.0)                              # no unbuffered mode, -u irrelevant
