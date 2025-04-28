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
    print("python3 create_error_maps_mob.py <comparison CSV>")

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

    """"
    try: plt.pcolormesh(x_ar, y_ar, matrix_areas).set_mouseover(True)
    except: plt.pcolormesh(x_ar, y_ar, matrix_areas)

    plt.title("Area Error Map (er <= 1m, 1 < er <= 3m, er > 3m)")
    plt.show()
    """

    return (matrix_acc, matrix_areas)

def dump_master_csv(avg_er_map):
    total_error_list = []

    print("X,Y,Avg Error per XY,")
    for point in avg_er_map:
        print("{},{},{}".format(point[0], point[1], avg_er_map[point]))
        total_error_list.append(avg_er_map[point])


    total_avg_error = statistics.mean(total_error_list)
    print("Total AVG error")
    print("{}".format(total_avg_error))

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

    for point, er_list in er_map.items():
        avg_er_map[point] = statistics.mean(er_list)

        if avg_er_map[point] > 552: avg_er_map[point] = 552

    create_colormap(avg_er_map)
    dump_master_csv(avg_er_map)

def main():
    if len(sys.argv) != 2:
        print_help()
        quit()

    comp = sys.argv[1]


    create_error_maps(comp)

if __name__ == "__main__":
    main()
