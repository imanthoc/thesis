from parse import parse
from filt import *
import sys
import numpy as np
import math
import statistics

ROOM_H = 330
ROOM_W = 660
WIN_SIZE = 17
ROOM_W_offset = ROOM_W * (2/10)
ROOM_H_offset = ROOM_H * (2/10)

a_top   = (ROOM_W/2+20, ROOM_H)
a_right = (ROOM_W, ROOM_H/2)
a_bot   = (ROOM_W/2+20, 0)
a_left  = (0, ROOM_H/2)

anchors = [a_bot, a_top, a_left, a_right]
stats = False
F_anchor = False

def print_help():
    print("Usage:")
    print("python3 convert_angles_to_crds.py <file> [options]")
    print("-F, Filter noisy anchor")
    print("-O, Output statistics instead of points")

def convert_mb(a_p, a_th, conversion_function):
    a_th = conversion_function(a_th)

    m = math.tan(a_th * (math.pi / 180))
    b = a_p[1] - m * a_p[0]

    return (m, b)

def find_common_point(m1, b1, m2, b2):
    if m1 == m2: m2 += 0.01

    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1

    return (x, y)

def find_average_point(point_list):
    avg_x = 0
    avg_y = 0

    for (x, y) in point_list:
        avg_x += x
        avg_y += y

    avg_x /= len(point_list)
    avg_y /= len(point_list)

    return (avg_x, avg_y)

def convert_angles_to_crds_legacy(total_pack):
    global anchors

    angle_pack = total_pack[0].copy()
    index_pack = total_pack[1]

    transform_function_table = [
        lambda th: 90 - th, lambda th: 90 - th,
        lambda th: -th, lambda th: -th
    ]

    mb_pairs = []

    for i in index_pack:
        (m, b) = convert_mb(anchors[i], angle_pack[i], transform_function_table[i])
        mb_pairs.append((m, b))

    intersection_point_list = []
    k = 0

    while k < len(index_pack) - 1:
        (m_1, b_1) = mb_pairs[k]
        (m_2, b_2) = mb_pairs[k+1]
        intersection_point_list.append(find_common_point(m_1, b_1,   m_2, b_2))

        k += 1

    (m_n, b_n) = mb_pairs[-1]
    (m_1, b_1) = mb_pairs[0]

    intersection_point_list.append(find_common_point(m_n, b_n, m_1, b_1))

    # some times a common point is none if the two lines are parallel
    center_point = find_average_point([p for p in intersection_point_list if p is not None])

    return center_point

def convert_angles_to_crds_lsq(total_pack):
    global anchors

    angle_pack = total_pack[0].copy()
    index_pack = total_pack[1]

    angle_pack[0] = (90 - angle_pack[0]) * (math.pi/180)
    angle_pack[1] = (90 - angle_pack[1]) * (math.pi/180)
    angle_pack[2] = -angle_pack[2] * (math.pi/180)
    angle_pack[3] = -angle_pack[3] * (math.pi/180)

    angles_actual = np.array([angle_pack[i] for i in index_pack])
    anchors_actual = np.array([anchors[i] for i in index_pack])

    a = np.sin(angles_actual)
    b = -np.cos(angles_actual)
    c = -a * anchors_actual[:, 0] - b * anchors_actual[:, 1]

    A = np.column_stack((a, b))

    pos, *_ = np.linalg.lstsq(A, -c, rcond=None)
    return pos[0], pos[1]

def convert(angles_f_name):
    global mode, stats

    ap_f = AnglePack_Filter(17)
    angles_file = open(angles_f_name)

    point_list = []
    point_list_2 = []

    total = 0

    for line in angles_file:
        line = line.strip()
        (b, t, l, r) = parse("{:d} , {:d} , {:d} , {:d}", line)

        angle_pack = [b, t, l, r]

        b_stdev = ap_f.filter_b(b)
        t_stdev = ap_f.filter_t(t)
        l_stdev = ap_f.filter_l(l)
        r_stdev = ap_f.filter_r(r)

        #index pack has a list of the USEFUL indices in the angle list
        if F_anchor:
            index_pack = ap_f.filter_angle_pack(b_stdev, t_stdev, l_stdev, r_stdev)
        else:
            index_pack = [0, 1, 2, 3]

        total_pack = (angle_pack, index_pack)

        p1 = convert_angles_to_crds_legacy(total_pack)
        p2 = convert_angles_to_crds_lsq(total_pack)

        point_list.append(p1)
        point_list_2.append(p2)

        if not stats:
            print("{:5.2f} , {:5.2f} , {:5.2f} , {:5.2f}".format(p1[0], p1[1], p2[0], p2[1]))
        total += 1

    if stats:
        x_list = [p[0] for p in point_list]
        y_list = [p[1] for p in point_list]

        x_avg = statistics.mean(x_list)
        y_avg = statistics.mean(y_list)
        x_stdev = statistics.stdev(x_list)
        y_stdev = statistics.stdev(y_list)

        print("{:.2f} , {:.2f} , {:.1f} , {:.1f}".format(x_avg, y_avg, x_stdev, y_stdev))

        if len(point_list_2) > 0:
            x_list = [p[0] for p in point_list_2]
            y_list = [p[1] for p in point_list_2]

            x_avg = statistics.mean(x_list)
            y_avg = statistics.mean(y_list)
            x_stdev = statistics.stdev(x_list)
            y_stdev = statistics.stdev(y_list)

            print("{:.2f} , {:.2f} , {:.1f} , {:.1f}".format(x_avg, y_avg, x_stdev, y_stdev))

def parse_arguments(args):
    global stats, F_anchor

    for arg in args:
        if arg == "-O": stats = True
        if arg == "-F": F_anchor = True

def main():
    if len(sys.argv) < 2:
        print_help()
        quit()

    parse_arguments(sys.argv)

    f_name = sys.argv[1]
    convert(f_name)

if __name__ == "__main__": main()
