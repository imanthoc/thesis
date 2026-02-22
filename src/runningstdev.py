import statistics
import sys
from parse import parse
import math
import numpy as np

ROOM_H = 350
ROOM_W = 660

a_top   = (400, ROOM_H)
a_right = (ROOM_W, ROOM_H/2)
a_bot   = (400, 0)
a_left  = (0, ROOM_H/2)


anchors = [a_bot, a_top, a_left, a_right]

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


def stats(angles_f_name):
    angles_file = open(angles_f_name)

    win1 = [0]
    win2 = [0]
    ls1 = []
    ls2 = []

    for line in angles_file:
        line = line.strip()
        (b, t, l, r) = parse("{:d} , {:d} , {:d} , {:d}", line)

        angle_pack = [b, t, l, r]
        index_pack = [0, 1, 2, 3]
        total_pack = (angle_pack, index_pack)

        p = convert_angles_to_crds_lsq(total_pack)

        if len(win1) > 17:
            win1.pop(0)
            win2.pop(0)

        win1.append(p[0])
        win2.append(p[1])

        ls1.append(statistics.stdev(win1))
        ls2.append(statistics.stdev(win2))

    print("mean x stdev:", statistics.mean(ls1))
    print("mean y stdev:", statistics.mean(ls2))

stats(sys.argv[1])
