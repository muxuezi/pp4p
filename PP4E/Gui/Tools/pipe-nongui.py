# non-GUI side: proceed normally, no need for special code

import time
while True:                          # non-GUI code
    print(time.asctime())            # sends to GUI process
    time.sleep(2.0)                  # no need to flush here
