import sys
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

def visualize(csv_name):
    df = pd.read_csv(csv_name, header=None).values

    cl_passed_values = defaultdict(lambda: False)

    limit = 2000
    i = 1
    for line in df:
        cl_x = float(line[2])
        cl_y = float(line[3])

        if not cl_passed_values[(cl_x, cl_y)]:
            plt.scatter(cl_x, cl_y, color='red', marker='o')
            cl_passed_values[(cl_x, cl_y)] = True

        if i == limit: break
        else: i += 1

    plt.show()

def main():
    if len(sys.argv) != 2:
        print("Not enough arguments")
        quit()

    csv_name = sys.argv[1]
    visualize(csv_name)


if __name__ == "__main__":
    main()
