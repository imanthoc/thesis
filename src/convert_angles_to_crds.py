from parse import parse
from filt import *
import sys
import numpy as np
import math
import statistics

ROOM_H = 330
ROOM_W = 660
WIN_SIZE = 10
ROOM_W_offset = ROOM_W * (2/10)
ROOM_H_offset = ROOM_H * (2/10)

a_top   = (ROOM_W/2+20, ROOM_H)
a_right = (ROOM_W, ROOM_H/2)
a_bot   = (ROOM_W/2+20, 0)
a_left  = (0, ROOM_H/2)

anchors = [a_bot, a_top, a_left, a_right]

moving_avg_active = False
mode = 0
stats = False
S_active = False

B_filt = Filter(statistics.mean, WIN_SIZE)
T_filt = Filter(statistics.mean, WIN_SIZE)
L_filt = Filter(statistics.mean, WIN_SIZE)
R_filt = Filter(statistics.mean, WIN_SIZE)

def reject_off(p):
    return p[0] < -ROOM_W_offset or p[1] < -ROOM_H_offset or p[0] > ROOM_W + ROOM_W_offset or p[1] > ROOM_H + ROOM_H_offset

def print_help():
    print("Usage:")
    print("python3 convert_angles_to_crds.py <file  > [method] [filtering] [options]")
    print("method: --legacy, --lqs (least squares), --all")
    print("filtering: -A, Moving AVG filter on angle values")
    print("-O, Output statistics instead of points")
    print("-S, Output points in a format compatible with visualize_path.py")

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

def convert_angles_to_crds_legacy(B, T, L, R):
    (m_bot, b_bot)      = convert_mb(a_bot, B, lambda th: 90 - th)
    (m_top, b_top)      = convert_mb(a_top, T, lambda th: 90 - th)
    (m_left, b_left)    = convert_mb(a_left, L, lambda th: -th)
    (m_right, b_right)  = convert_mb(a_right, R, lambda th: -th)

    p_bl = find_common_point(m_bot,   b_bot,   m_left,  b_left)
    p_lt = find_common_point(m_left,  b_left,  m_top,   b_top)
    p_tr = find_common_point(m_top,   b_top,   m_right, b_right)
    p_rb = find_common_point(m_right, b_right, m_bot,   b_bot)

    p_list = [p_bl, p_lt, p_tr, p_rb]

    # some times a common point is none if the two lines are parallel
    center_point = find_average_point([p for p in p_list if p is not None])

    return center_point

def convert_angles_to_crds_lsq(B, T, L, R):
    global anchors

    conv_B = 90-B
    conv_T = 90-T
    conv_L = -L
    conv_R = -R

    angles = [conv_B*(math.pi/180), conv_T*(math.pi/180), conv_L*(math.pi/180), conv_R*(math.pi/180)]

    anchors = np.array(anchors)
    angles = np.array(angles)

    a = np.sin(angles)
    b = -np.cos(angles)
    c = -a * anchors[:, 0] - b * anchors[:, 1]

    A = np.column_stack((a, b))

    pos, *_ = np.linalg.lstsq(A, -c, rcond=None)
    return pos[0], pos[1]

def convert(angles_f_name):
    global moving_avg_active
    global mode
    global stats
    global S_active

    angles_file = open(angles_f_name)

    point_list = []

    total = 0
    rejected = 0

    for line in angles_file:
        line = line.strip()
        (B, T, L, R) = parse("BOT: {:d} TOP: {:d} LEFT: {:d} RIGHT: {:d}", line)

        if moving_avg_active:
            B = B_filt.filt(B)
            T = T_filt.filt(T)
            L = L_filt.filt(L)
            R = R_filt.filt(R)

        p = (0, 0)
        p_extra = (0, 0)

        if reject_off((p[0], p[1])): rejected += 1
        else:
            if mode == 0:
                p = convert_angles_to_crds_legacy(B, T, L, R)
            elif mode == 1:
                p = convert_angles_to_crds_lsq(B, T, L, R)
            else:
                p = convert_angles_to_crds_legacy(B, T, L, R)
                p_extra = convert_angles_to_crds_lsq(B, T, L, R)

            if not stats:
                if not S_active:
                    if mode == 0 or mode  == 1:
                        print("{:5.2f} , {:5.2f}".format(p[0], p[1]))
                    else:
                        print("{:5.2f} , {:5.2f} , {:5.2f} , {:5.2f}".format(p[0], p[1], p_extra[0], p_extra[1]))
                else:
                    print("0, 0, {:5.2f}, {:5.2f}, 0, 0".format(p[0], p[1]))


        point_list.append((p[0], p[1]))
        total += 1
    if stats:
        x_list = [p[0] for p in point_list]
        y_list = [p[1] for p in point_list]

        x_avg = statistics.mean(x_list)
        y_avg = statistics.mean(y_list)
        x_stdev = statistics.stdev(x_list)
        y_stdev = statistics.stdev(y_list)

        print("{:.2f} , {:.2f} , {:.1f} , {:.1f}".format(x_avg, y_avg, x_stdev, y_stdev))
        #print("Rejected {} out of {} points".format(rejected, total))

def parse_arguments(args):
    global moving_avg_active
    global mode
    global stats
    global S_active

    for arg in args:
        if arg == "-A": moving_avg_active = True
        if arg == "--legacy": mode = 0
        elif arg == "--lsq": mode = 1
        elif arg == "--all": mode = 2
        if arg == "-O": stats = True
        if arg == "-S": S_active = True

def main():
    if len(sys.argv) < 2:
        print_help()
        quit()

    parse_arguments(sys.argv)

    f_name = sys.argv[1]
    convert(f_name)

if __name__ == "__main__": main()
