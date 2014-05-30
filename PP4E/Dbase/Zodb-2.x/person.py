#######################################################################
# define persistent object classes; this must be in an imported
# file on your path, not in __main__ per Python pickling rules
# unless will only ever be used in module __main__ in the future;
# attribute assignments, in class or otherwise, update database;
# for mutable object changes, set object's _p_changed to true to
# auto update, or manually reassign to database key after changes;
#######################################################################

from persistent import Persistent             # new module name in 3.3

class Person(Persistent):
    def __init__(self, name, job=None, rate=0):
        self.name = name
        self.job  = job
        self.rate = rate
    def changeRate(self, newrate):
        self.rate = newrate                   # auto updates database
    def calcPay(self, hours=40):
        return self.rate * hours
    def __str__(self):
        myclass = self.__class__.__name__
        format = '<%s:\t name=%s, job=%s, rate=%d, pay=%d>'
        values = (myclass, self.name, self.job, self.rate, self.calcPay())
        return format % values

class Engineer(Person):
    def calcPay(self):
        return self.rate / 52   # yearly salary
