import sys
from parse import parse
import matplotlib.pyplot as plt

f = open(sys.argv[1])

B_a = []
T_a = []
L_a = []
R_a = []

for line in f:
    line = line.strip()
    (B, T, L, R) = parse("{:d} , {:d} , {:d} , {:d}", line)

    B_a.append(B)
    T_a.append(T)
    L_a.append(L)
    R_a.append(R)

plt.plot(B_a, color='red', label="B")
plt.plot(T_a, color='green', label="T")
plt.plot(L_a, color='blue', label="L")
plt.plot(R_a, color='black', label="R")
plt.legend()

plt.show()
