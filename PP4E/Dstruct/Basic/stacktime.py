"compare performance of stack alternatives"

import stack2           # list-based stacks: [x]+y
import stack3           # tuple-tree stacks: (x,y)
import stack4           # in-place stacks:   y.append(x)
import timer            # general function timer utility

rept = 200
from sys import argv
pushes, pops, items = (int(arg) for arg in argv[1:])

def stackops(stackClass):
    x = stackClass('spam')                    # make a stack object
    for i in range(pushes): x.push(i)         # exercise its methods
    for i in range(items):  t = x[i]          # 3.X: range generator
    for i in range(pops):   x.pop()
                                              # or mod = __import__(n)
for mod in (stack2, stack3, stack4):          # rept*(push+pop+ix)
    print('%s:' % mod.__name__, end=' ')
    print(timer.test(rept, stackops, getattr(mod, 'Stack')))
