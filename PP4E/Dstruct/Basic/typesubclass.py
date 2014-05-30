"customize built-in types to extend, instead of starting from scratch"

class Stack(list):
    "a list with extra methods"
    def top(self):
        return self[-1]

    def push(self, item):
        list.append(self, item)

    def pop(self):
        if not self:
            return None                 # avoid exception
        else:
            return list.pop(self)

class Set(list):
    " a list with extra methods and operators"
    def __init__(self, value=[]):      # on object creation
        list.__init__(self)
        self.concat(value)

    def intersect(self, other):         # other is any sequence type
        res = []                        # self is the instance subject
        for x in self:
            if x in other:
                res.append(x)
        return Set(res)                 # return a new Set

    def union(self, other):
        res = Set(self)                 # new set with a copy of my list
        res.concat(other)               # insert uniques from other
        return res

    def concat(self, value):            # value: a list, string, Set...
        for x in value:                 # filters out duplicates
           if not x in self:
                self.append(x)

    # len, getitem, iter inherited, use list repr
    def __and__(self, other):   return self.intersect(other)
    def __or__(self, other):    return self.union(other)
    def __str__(self):          return '<Set:' + repr(self) + '>'

class FastSet(dict):
    pass    # this doesn't simplify much


def selfTest():
    # normal use cases
    stk = Stack()
    print(stk)
    for c in 'spam': stk.push(c)
    print(stk, stk.top())
    while stk: print(stk, stk.pop())
    print(stk, stk.pop())

    print()
    set = Set('spam')
    print(set, 'p' in set)
    print(set & Set('slim'))
    print(set | 'slim')
    print(Set('slim') | Set('spam'))

    # downside? these work too
    print()
    stk = Stack('spam')
    print(stk)
    stk.insert(1, 'X')     # should only access top, can add duplicates
    print(stk)
    stk.sort()             # stack not usually ordered
    print(stk)

    set = Set('spam')
    set.reverse()          # order should not matter
    print(set, set[1])

if __name__ == '__main__':
    selfTest()


"""
Expected Python 3.1 output:
C:\...\PP4E\Dstruct\Basic> typesubclass.py
[]
['s', 'p', 'a', 'm'] m
['s', 'p', 'a'] m
['s', 'p'] a
['s'] p
[] s
[] None

<Set:['s', 'p', 'a', 'm']> True
<Set:['s', 'm']>
<Set:['s', 'p', 'a', 'm', 'l', 'i']>
<Set:['s', 'l', 'i', 'm', 'p', 'a']>

['s', 'p', 'a', 'm']
['s', 'X', 'p', 'a', 'm']
['X', 'a', 'm', 'p', 's']
<Set:['m', 'a', 'p', 's']> a
"""