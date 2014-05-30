import sys

def filter_files(name, function):         # filter file through function
    input  = open(name, 'r')              # create file objects
    output = open(name + '.out', 'w')     # explicit output file too
    for line in input:
        output.write(function(line))      # write the modified line
    input.close()
    output.close()                        # output has a '.out' suffix

def filter_stream(function):              # no explicit files
    while True:                           # use standard streams
        line = sys.stdin.readline()       # or: input()
        if not line: break
        print(function(line), end='')     # or: sys.stdout.write()

if __name__ == '__main__':
    filter_stream(lambda line: line)      # copy stdin to stdout if run



"""
def filter_files(name, function):
    with open(name, 'r') as input, open(name + '.out', 'w') as output:
        for line in input:
            output.write(function(line))      # write the modified line
"""

"""
def filter_stream(function):
    for line in sys.stdin:
        print(function(line), end='')
"""

