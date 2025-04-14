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

def create_histograms(matrix):
    transpose_matrix = []
    for col in zip(*matrix):
        row = [v for v in col]
        transpose_matrix.append(row)

    row_index_array = [str(i+1) for i in range(len(matrix))]
    col_index_array = [str(i+1) for i in range(len(matrix[0]))]

    avg_error_per_row = [statistics.mean(row) for row in matrix]
    avg_stdev_per_row = [statistics.stdev(row) for row in matrix]

    avg_error_per_col = [statistics.mean(row) for row in transpose_matrix]
    avg_stdev_per_col = [statistics.stdev(row) for row in transpose_matrix]

    f = plt.figure()
    avg_plt     = f.add_subplot(121)
    stdev_plt   = f.add_subplot(122)

    avg_plt.bar(row_index_array, avg_error_per_row)
    avg_plt.set_xlabel("Row (1-indexed)")
    avg_plt.set_ylabel("Avg Error")
    avg_plt.set_title("Average Error per Row")

    stdev_plt.bar(row_index_array, avg_stdev_per_row)
    stdev_plt.set_xlabel("Row (1-indexed)")
    stdev_plt.set_ylabel("STDev")
    stdev_plt.set_title("STDev per Row")

    plt.show()

    f = plt.figure()
    avg_plt     = f.add_subplot(121)
    stdev_plt   = f.add_subplot(122)

    avg_plt.bar(col_index_array, avg_error_per_col)
    avg_plt.set_xlabel("Col (1-indexed)")
    avg_plt.set_ylabel("Avg Error")
    avg_plt.set_title("Average Error per Col")

    stdev_plt.bar(col_index_array, avg_stdev_per_col)
    stdev_plt.set_xlabel("Col (1-indexed)")
    stdev_plt.set_ylabel("STDev")
    stdev_plt.set_title("STDev per Col")

    plt.show()

def create_colormap(er_map):
    matrix_acc = []
    matrix_areas = []

    x_ar = [x for x in range(0, 1201, 60)]
    y_ar = [y for y in range(0, 601, 60)]

    for y in reversed(y_ar):
        row_acc = []
        row_area = []

        for x in x_ar:
            p = (x, y)
            if p not in er_map:
                row_acc.append(0)
                row_area.append(1)
            else:
                if er_map[p] > 552: er_map[p] = 552

                row_acc.append(er_map[p])

                if er_map[p] <= 100:    row_area.append(1)
                elif er_map[p] <= 300:  row_area.append(2)
                else:                   row_area.append(3)

        matrix_acc.append(row_acc)
        matrix_areas.append(row_area)

    plt.pcolormesh(x_ar, y_ar, matrix_acc).set_mouseover(True)
    plt.colorbar(label='Error')
    plt.title("Color Error Map")
    plt.show()

    plt.title("Area Error Map (er <= 1m, 1 < er <= 3m, er > 3m)")
    plt.pcolormesh(x_ar, y_ar, matrix_areas).set_mouseover(True)
    plt.show()

    create_histograms(matrix_acc)

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


def main():
    if len(sys.argv) != 2:
        print_help()
        quit()

    comp = sys.argv[1]

    create_error_maps(comp)

if __name__ == "__main__":
    main()
