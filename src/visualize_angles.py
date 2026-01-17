import sys
import matplotlib.pyplot as pl
import math

fig, ax = pl.subplots()

#left:  6501
#bot:   6502
#right: 6503
#top:   6504

#convert the point & angle representation of the line
#to a y = mx + b representation
#also due to the anchors aoa reporting a conversion function is needed for theta\

def convert_mb(a_p, a_th, conversion_function):
    a_th = conversion_function(a_th)

    m = math.tan(a_th * (math.pi / 180))
    b = a_p[1] - m * a_p[0]

    return (m, b)

def evaluate_line_y(mb, x):
    return mb[0]*x + mb[1]

def evaluate_line_x(mb, y):
    if (mb[0] == 0): mb[0] = 0.000000000000000000000000000000001
    return (y - mb[1]) / mb[0]

def plot_line(p1, p2, lb):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], marker='o', label=lb)

def main():
    ROOM_H = 600
    ROOM_W = 1200

    a_bot   = (ROOM_W / 2,  0)
    a_top   = (ROOM_W / 2,  ROOM_H)
    a_left  = (0,           ROOM_H / 2)
    a_right = (ROOM_W,      ROOM_H / 2)

    if len(sys.argv) != 5:
        th_left  = float(input("th left[6501]> "))
        th_bot   = float(input("th bot[6502]> "))
        th_right = float(input("th right[6503]> "))
        th_top   = float(input("th top[6504]> "))
    else:
        th_left  = float(sys.argv[1])
        th_bot   = float(sys.argv[2])
        th_right = float(sys.argv[3])
        th_top   = float(sys.argv[4])

    mb_bot   = convert_mb(a_bot, th_bot, lambda th: 90 - th)
    mb_left  = convert_mb(a_left, th_left, lambda th: -th)
    mb_top   = convert_mb(a_top, th_top, lambda th: 90 - th)
    mb_right = convert_mb(a_right, th_right, lambda th: -th)

    plot_line(a_bot,   [evaluate_line_x         (mb_bot, ROOM_H), ROOM_H],  "bot anchor line")
    plot_line(a_left,  [ROOM_W, evaluate_line_y (mb_left, ROOM_W)],         "left anchor line")
    plot_line(a_top,   [evaluate_line_x         (mb_top, 0), 0],            "top anchor line")
    plot_line(a_right, [0, evaluate_line_y      (mb_right, 0)],             "right anchor line")

    ax.legend()

    ax.set_xlim(0, ROOM_W)
    ax.set_ylim(0, ROOM_H)

    pl.show()

if __name__ == "__main__":
    main()
