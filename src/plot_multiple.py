from parse import parse
from filt import *
import sys
import numpy as np
import math
import statistics
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


ROOM_H = 350
ROOM_W = 660
#WIN_SIZE = 17

#a_top   = (400, ROOM_H)
#a_right = (ROOM_W, ROOM_H/2)
#a_bot   = (400, 0)
#a_left  = (0, ROOM_H/2)

a_bot = (456, 0)
a_top = (269, 705)
a_left = (0, 476)
a_right = (650, 550)
anchors = [a_bot, a_top, a_left, a_right]
stats = False
F_anchor = False
PLT = True

def print_help():
    print("Usage:")
    print("python3 convert_angles_to_crds.py <file> [options]")
    print("-F, Filter noisy anchor")
    print("-O, Output statistics instead of points")
    print ("--np, Don't plot at the end")

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

def convert(f_name_list):
    global mode, stats, PLT

    angles_file_list = [open(f_name) for f_name in f_name_list]

    colors = ['red', 'green', 'blue', 'yellow', 'black']
    lbs = ["West", "South", "East", "North"]
    c = 0

    img = mpimg.imread("../report/pictures/room_b_on.png")
    plt.imshow(img,
               extent=[0, 650, 0, 700],
                origin="upper"  # often needed for Cartesian coords
    )

    for angles_file in angles_file_list:
        first = True
        for line in angles_file:
            line = line.strip()
            (b, t, l, r) = parse("{:d} , {:d} , {:d} , {:d}", line)

            if 500 in (b, t, l, r): continue

            angle_pack = [b, t, l, r]
            index_pack = [0, 1, 2, 3]
            total_pack = (angle_pack, index_pack)

            p = convert_angles_to_crds_lsq(total_pack)

            plt.xlim(left=0, right=650)
            plt.ylim(bottom=0, top=700)
            plt.title("LSQ")
            plt.scatter(p[0], p[1], color=colors[c], marker='o', label=lbs[c] if first else None)
            first = False
        c += 1


    plt.tight_layout()
    plt.legend()
    plt.show()


def main():
    if len(sys.argv) < 2:
        quit()

    f_name_list = sys.argv[1:]
    convert(f_name_list)

if __name__ == "__main__": main()
