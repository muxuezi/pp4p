# test both streams
import sys
line = input()                    # from Inputs
print(line.split())               # saved to Outputs
reply = sys.stdin.readline()      # also from Inputs
sys.stdout.write(reply * 8)       # also to Outputs

