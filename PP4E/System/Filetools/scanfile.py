def scanner(name, function):
    file = open(name, 'r')               # create a file object
    while True:
        line = file.readline()           # call file methods
        if not line: break               # until end-of-file
        function(line)                   # call a function object
    file.close()


"""
def scanner(name, function):
    for line in open(name, 'r'):         # scan line by line
        function(line)                   # call a function object
"""


"""
def scanner(name, function):
    [function(line) for line in open(name, 'r')]
"""
