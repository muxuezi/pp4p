"Scan C header files to extract parts of #define and #include lines"

import sys, re
pattDefine = re.compile(                             # compile to pattobj
    '^#[\t ]*define[\t ]+(\w+)[\t ]*(.*)')           # "# define xxx yyy..."
                                                     # \w like [a-zA-Z0-9_]
pattInclude = re.compile(
    '^#[\t ]*include[\t ]+[<"]([\w\./]+)')           # "# include <xxx>..."

def scan(fileobj):
    count = 0
    for line in fileobj:                             # scan by lines: iterator
        count += 1
        matchobj = pattDefine.match(line)            # None if match fails
        if matchobj:
            name = matchobj.group(1)                 # substrings for (...) parts
            body = matchobj.group(2)
            print(count, 'defined', name, '=', body.strip())
            continue
        matchobj = pattInclude.match(line)
        if matchobj:
            start, stop = matchobj.span(1)           # start/stop indexes of (...)
            filename = line[start:stop]              # slice out of line
            print(count, 'include', filename)        # same as matchobj.group(1)

if len(sys.argv) == 1:
    scan(sys.stdin)                    # no args: read stdin
else:
    scan(open(sys.argv[1], 'r'))       # arg: input filename
