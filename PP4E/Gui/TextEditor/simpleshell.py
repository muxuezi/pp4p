# read and run Python statement strings: like PyEdit's run code menu option

namespace = {}
while True:
    try:
        line = input('>>> ')          # single-line statements only
    except EOFError:
        break
    else:
        exec(line, namespace)         # or eval() and print result
