import sys
import pandas as pd
import math
from collections import defaultdict
import statistics
import matplotlib.pyplot as plt
import numpy as np

def distance(x1, y1, x2, y2):
    return math.sqrt( (x1 - x2)**2 + (y1 - y2)**2 )

def print_help():
    print("Usage:")
    print("python3 create_error_maps.py <comparison CSV>")

def create_colormap(er_map):
    matrix = []

    x_ar = [x for x in range(0, 1201, 60)]
    y_ar = [y for y in range(0, 601, 60)]

    for y in reversed(y_ar):
        row = []

        for x in x_ar:
            p = (x, y)
            if p not in er_map:
                row.append(0)
            else:
                if er_map[p] > 552: er_map[p] = 552
                row.append(er_map[p])

        matrix.append(row)

    plt.pcolormesh(x_ar, y_ar, matrix)
    plt.colorbar(label='value')
    plt.show()

def create_centermap(avg_er_map):
    zero_x = 600
    zero_y = 300

    distance_error_list = []

    for ((p_x, p_y), error) in  avg_er_map.items():
        d = distance(zero_x, zero_y, p_x, p_y)
        distance_error_list.append((d, error))

    distance_error_list.sort()

    distance_list = [d for (d, e) in distance_error_list]
    error_list = [e for (d, e) in distance_error_list]

    plt.plot(distance_list, error_list)
    plt.show()

def print_avg_error_per_point(avg_er_map, stddev_map):
    matrix = []

    x_ar = [x for x in range(0, 1201, 60)]
    y_ar = [y for y in range(0, 601, 60)]

    for x in x_ar:
        for y in y_ar:
            p = (x, y)
            if p in avg_er_map and p in stddev_map:
                error = avg_er_map[p]
                stddev = stddev_map[p]

                row = [x, y, error, stddev]
                matrix.append(row)

    df = pd.DataFrame(matrix)
    df.to_csv("error_per_point.csv", index = False, header = ["X", "Y", "AVG Error", "STDDev"])

def create_error_maps(comp):
    cm_df = pd.read_csv(comp).values

    er_map = defaultdict(list)

    for line in cm_df:
        gt_x = int(line[4])
        gt_y = int(line[5])

        gt = (gt_x, gt_y)
        cl = (line[6], line[7])

        error = distance(gt[0], gt[1], cl[0], cl[1])
        er_map[gt].append(error)

    avg_er_map = {}
    stddev_map = {}

    for point, er_list in er_map.items():
        avg_er_map[point] = statistics.mean(er_list)
        stddev_map[point] = statistics.stdev(er_list)

    for point, avg_er in avg_er_map.items():
        pass #print("[{}, {}] = {}".format(point[0], point[1], avg_er))

    create_colormap(avg_er_map)
    create_centermap(avg_er_map)

    print_avg_error_per_point(avg_er_map, stddev_map)

def main():
    if len(sys.argv) != 2:
        print_help()
        quit()

    comp = sys.argv[1]

    create_error_maps(comp)

if __name__ == "__main__":
    main()
