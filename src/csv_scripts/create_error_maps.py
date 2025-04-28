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
        transpose_matrix.append([v for v in col])

    row_index_array = [str(i+1) for i in range(len(matrix))]
    col_index_array = [str(i+1) for i in range(len(matrix[0]))]

    avg_error_per_row = []
    stdev_per_row = []

    for row in matrix:
        filtered_row = [v for v in row if v != -1]
        # if filtered row is not empty
        if filtered_row:
            avg_error_per_row.append(statistics.mean(filtered_row))
            stdev_per_row.append(statistics.stdev(filtered_row))
        else:
            avg_error_per_row.append(0)
            stdev_per_row.append(0)

    avg_error_per_col = []
    stdev_per_col = []

    for row in transpose_matrix:
        filtered_row = [v for v in row if v != -1]
        # if filtered row is not empty
        if filtered_row:
            avg_error_per_col.append(statistics.mean(filtered_row))
            stdev_per_col.append(statistics.stdev(filtered_row))
        else:
            avg_error_per_col.append(0)
            stdev_per_col.append(0)

    f = plt.figure()
    avg_plt     = f.add_subplot(121)
    stdev_plt   = f.add_subplot(122)

    avg_plt.bar(row_index_array, avg_error_per_row)
    avg_plt.set_xlabel("Row (1-indexed)")
    avg_plt.set_ylabel("Avg Error")
    avg_plt.set_title("Average Error per Row")

    stdev_plt.bar(row_index_array, stdev_per_row)
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

    stdev_plt.bar(col_index_array, stdev_per_col)
    stdev_plt.set_xlabel("Col (1-indexed)")
    stdev_plt.set_ylabel("STDev")
    stdev_plt.set_title("STDev per Col")

    plt.show()

    return transpose_matrix

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
                row_acc.append(-1)
                row_area.append(-1)
            else:
                if er_map[p] > 552: er_map[p] = 552

                row_acc.append(er_map[p])

                if er_map[p] <= 100:    row_area.append(1)
                elif er_map[p] <= 300:  row_area.append(2)
                else:                   row_area.append(3)

        matrix_acc.append(row_acc)
        matrix_areas.append(row_area)

    try: plt.pcolormesh(x_ar, y_ar, matrix_acc).set_mouseover(True)
    except: plt.pcolormesh(x_ar, y_ar, matrix_acc)

    plt.colorbar(label='Error')
    plt.title("Color Error Map")
    plt.show()


    try: plt.pcolormesh(x_ar, y_ar, matrix_areas).set_mouseover(True)
    except: plt.pcolormesh(x_ar, y_ar, matrix_areas)

    plt.title("Area Error Map (er <= 1m, 1 < er <= 3m, er > 3m)")
    plt.show()

    transpose_matrix = create_histograms(matrix_acc)

    return (matrix_acc, matrix_areas, transpose_matrix)

def create_centermap(avg_er_map):
    zero_x = 600
    zero_y = 300

    distance_error_list = []

    for ((p_x, p_y), error) in  avg_er_map.items():
        d = distance(zero_x, zero_y, p_x, p_y)
        distance_error_list.append((d, error))

    distance_error_list.sort()

    distance_list   = [d for (d, e) in distance_error_list]
    error_list      = [e for (d, e) in distance_error_list]

    plt.plot(distance_list, error_list)
    plt.show()


def dump_master_csv(matrix_acc, matrix_areas, transpose_matrix, avg_er_map, stddev_map):
    total_error_list = []

    print("X,Y,Avg Error per XY, STDev per XY")
    for point in avg_er_map:
        print("{},{},{},{}".format(point[0], point[1], avg_er_map[point], stddev_map[point]))
        total_error_list.append(avg_er_map[point])

    print("Row,Avg Error per Row, STDev per Row")
    i = 1
    for row in matrix_acc:
        print("{},{},{}".format(i, statistics.mean(row), statistics.stdev(row)))
        i += 1

    print("Col,Avg Error per Col, STDev per Col")
    i = 1
    for line in transpose_matrix:
        print("{},{},{}".format(i, statistics.mean(line), statistics.stdev(line)))
        i += 1

    area_a = 0
    area_b = 0
    area_c = 0
    for row in matrix_areas:
        for value in row:
            if value == 1: area_a += 1
            elif value == 2: area_b += 1
            elif value == 3: area_c += 1

    print("Area A,Area B,Area C")
    print("{},{},{}".format(area_a, area_b, area_c))

    total_avg_error = statistics.mean(total_error_list)
    total_stdev     = statistics.stdev(total_error_list)
    print("Total AVG error,Total STDev")
    print("{},{}".format(total_avg_error, total_stdev))


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

        if avg_er_map[point] > 552: avg_er_map[point] = 552
        if stddev_map[point] > 552: stddev_map[point] = 552

    (matrix_acc, matrix_areas, transpose_matrix) = create_colormap(avg_er_map)
    create_centermap(avg_er_map)

    dump_master_csv(matrix_acc, matrix_areas, transpose_matrix, avg_er_map, stddev_map)


def main():
    if len(sys.argv) != 2:
        print_help()
        quit()

    comp = sys.argv[1]

    create_error_maps(comp)

if __name__ == "__main__":
    main()
