from parse import parse
import statistics
import math

f = open("los.txt", 'r')

def d(a, b):
    return math.sqrt( (b[0] - a[0])**2 + (b[1] - a[1])**2 )

errors = []
for line in f:
    line = line.strip()
    (x1, y1, x2, y2) = parse("{:g} , {:g} , {:g} , {:g}", line)

    errors.append(d((x1, y1), (x2, y2)))

print("AVG", statistics.mean(errors))
