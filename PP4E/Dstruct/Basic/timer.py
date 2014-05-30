"generic code timer tool"
def test(reps, func, *args):        # or best of N? see Learning Python
    import time
    start = time.clock()            # current CPU time in float seconds
    for i in range(reps):           # call function reps times
        func(*args)                 # discard any return value
    return time.clock() - start     # stop time - start time
