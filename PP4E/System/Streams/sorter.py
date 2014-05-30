import sys                                  # or sorted(sys.stdin)
lines = sys.stdin.readlines()               # sort stdin input lines,
lines.sort()                                # send result to stdout
for line in lines: print(line, end='')      # for further processing
