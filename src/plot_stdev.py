from parse import parse
from filt import *
import sys
import numpy as np
import math
import statistics
import matplotlib.pyplot as plt

ROOM_H = 330
ROOM_W = 660
ROOM_W_offset = ROOM_W * (2/10)
ROOM_H_offset = ROOM_H * (2/10)
D = False

a_top   = (ROOM_W/2+20, ROOM_H)
a_right = (ROOM_W, ROOM_H/2)
a_bot   = (ROOM_W/2+20, 0)
a_left  = (0, ROOM_H/2)

anchors = [a_bot, a_top, a_left, a_right]

def plot(f_name, win_size):
    global D

    ap_f = AnglePack_Filter(win_size)

    median_graph = []
    b_stdev_graph = []
    t_stdev_graph = []
    l_stdev_graph = []
    r_stdev_graph = []

    angle_file = open(f_name, 'r')
    x = 0
    for line in angle_file:
        line = line.strip()
        angle_pack = (b, t, l, r) = parse("{:d} , {:d} , {:d} , {:d}", line)

        b_stdev = ap_f.filter_b(b)
        t_stdev = ap_f.filter_t(t)
        l_stdev = ap_f.filter_l(l)
        r_stdev = ap_f.filter_r(r)

        stdev_pack = (b_stdev, t_stdev, l_stdev, r_stdev)

        if not D:
            b_stdev_graph.append(b_stdev)
            t_stdev_graph.append(t_stdev)
            l_stdev_graph.append(l_stdev)
            r_stdev_graph.append(r_stdev)
        else:
            median = statistics.median(stdev_pack)
            median_graph.append(median)

            b_stdev_graph.append(abs(b_stdev - median))
            t_stdev_graph.append(abs(t_stdev - median))
            l_stdev_graph.append(abs(l_stdev - median))
            r_stdev_graph.append(abs(r_stdev - median))

            ip = ap_f.filter_angle_pack(b_stdev, t_stdev, l_stdev, r_stdev)
            if len(ip) == 3:
                plt.axvspan(x, x+1)
        x += 1


    plt.plot(b_stdev_graph, color='red',   label='B', linewidth=3)
    plt.plot(t_stdev_graph, color='green', label='T', linewidth=3)
    plt.plot(l_stdev_graph, color='blue',  label='L', linewidth=3)
    plt.plot(r_stdev_graph, color='black', label='R', linewidth=3)

    plt.legend()

    plt.show()

    angle_file.close()

def print_help():
    print("Usage:")
    print("python3 plot_stdev.py <file> <window size> [options]")
    print("-D, plot the distance from the median of the pack of stdevs")

def main():
    global D

    if len(sys.argv) < 3:
        print_help()
        quit()

    f_name = sys.argv[1]
    win_size = int(sys.argv[2])

    if len(sys.argv) == 4 and sys.argv[3] == "-D":
        D = True

    plot(f_name, win_size)

if __name__ == "__main__": main()
