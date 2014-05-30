#!/usr/local/bin/python

def summer(numCols, fileName):
    sums = [0] * numCols                             # make list of zeros
    for line in open(fileName):                      # scan file's lines
        cols = line.split()                          # split up columns
        for i in range(numCols):                     # around blanks/tabs
            sums[i] += eval(cols[i])                 # add numbers to sums
    return sums

if __name__ == '__main__':
    import sys
    print(summer(eval(sys.argv[1]), sys.argv[2]))    # '% summer.py cols file'
