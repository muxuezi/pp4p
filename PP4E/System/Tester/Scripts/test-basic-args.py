# test args, streams
import sys, os
print(os.getcwd())                  # to Outputs
print(sys.path[0])

print('[argv]')
for arg in sys.argv:                # from Args
    print(arg)                      # to Outputs

print('[interaction]')              # to Outputs
text = input('Enter text:')         # from Inputs
rept = sys.stdin.readline()         # from Inputs
sys.stdout.write(text * int(rept))  # to Outputs
