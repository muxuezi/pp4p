sums = {}
for line in open('table4.txt'):
    cols = [float(col) for col in line.split()]
    for pos, val in enumerate(cols):
       sums[pos] = sums.get(pos, 0.0) + val

for key in sorted(sums):
    print(key, '=', sums[key])
