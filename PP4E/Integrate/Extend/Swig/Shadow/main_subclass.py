"sublass C++ class in Python (generated shadow class)"

from number import Number                # import shadow class

class MyNumber(Number):
    def add(self, other):                # extend method
        print('in Python add...')
        Number.add(self, other)
    def mul(self, other):                # add new method
        print('in Python mul...')
        self.data = self.data * other

num = MyNumber(1)               # same tests as main.cxx, main.py
num.add(4)                      # using Python subclass of shadow class
num.display()                   # add() is specialized in Python
num.sub(2)
num.display()
print(num.square())

num.data = 99
print(num.data)
num.display()

num.mul(2)                      # mul() is implemented in Python
num.display()
print(num)                      # repr from shadow superclass
del num
