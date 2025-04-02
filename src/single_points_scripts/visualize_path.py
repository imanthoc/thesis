import sys
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

def visualize(csv_name, q, undersampling_rate):
    df = pd.read_csv(csv_name).values

    cl_passed_values = defaultdict(lambda: False)

    total_points = 0
    i = 1
    for line in df:
        if i != undersampling_rate:
            i += 1
            continue

        total_points += 1

        if q == "1":
            cl_x = float(line[4])
            cl_y = float(line[5])
        else:
            cl_x = float(line[2])
            cl_y = float(line[3])

        if cl_x > 1200 or cl_y > 600: continue

        if not cl_passed_values[(cl_x, cl_y)]:
            plt.scatter(cl_x, cl_y, color='red', marker='o')
            cl_passed_values[(cl_x, cl_y)] = True
            #print("Printing ({}, {})".format(cl_x, cl_y))
        i = 1

    print("Plotted {} points".format(total_points))
    plt.show()

def print_help():
    print("Usage:")
    print("python3 visualize_path.py <path CSV> <quantize = 1 or 0> <undersampling rate >= 1>")

def main():
    if len(sys.argv) != 4:
        print_help()
        quit()

    csv_name            = sys.argv[1]
    q                   = sys.argv[2]
    undersampling_rate  = int(sys.argv[3])

    visualize(csv_name, q, undersampling_rate)


if __name__ == "__main__":
    main()
