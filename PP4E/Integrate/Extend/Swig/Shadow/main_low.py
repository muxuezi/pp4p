"""
run similar tests to main.cxx and main.py
but use low-level C accessor function interface
"""

from _number import *           # c++ extension module wrapper 

num = new_Number(1)
Number_add(num, 4)              # pass C++ 'this' pointer explicitly
Number_display(num)             # use accessor functions in the C module
Number_sub(num, 2)
Number_display(num)
print(Number_square(num))

Number_data_set(num, 99)
print(Number_data_get(num))
Number_display(num)
print(num)
delete_Number(num)
