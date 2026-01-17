import sys
import math

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

def find_common_point(m1, b1, m2, b2):
    if m1 == m2: return None #should generally never happen

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

def main():
    ROOM_H = 600
    ROOM_W = 1200

    a_bot   = (ROOM_W / 2,  0)
    a_top   = (ROOM_W / 2,  ROOM_H)
    a_left  = (0,           ROOM_H / 2)
    a_right = (ROOM_W,      ROOM_H / 2)

    if len(sys.argv) != 5:
        th_bot   = float(input("th bot> "))
        th_top   = float(input("th top> "))
        th_left  = float(input("th left> "))
        th_right = float(input("th right> "))
    else:
        th_bot   = float(sys.argv[1])
        th_top   = float(sys.argv[2])
        th_left  = float(sys.argv[3])
        th_right = float(sys.argv[4])

    (m_bot, b_bot)      = convert_mb(a_bot, th_bot, lambda th: 90 - th)
    (m_left, b_left)    = convert_mb(a_left, th_left, lambda th: -th)
    (m_top, b_top)      = convert_mb(a_top, th_top, lambda th: 90 - th)
    (m_right, b_right)  = convert_mb(a_right, th_right, lambda th: -th)

    p_bl = find_common_point(m_bot, b_bot, m_left, b_left)
    p_lt = find_common_point(m_left, b_left, m_top, b_top)
    p_tr = find_common_point(m_top, b_top, m_right, b_right)
    p_rb = find_common_point(m_right, b_right, m_bot, b_bot)

    center_point = find_average_point([p_bl, p_lt, p_tr, p_rb])

    print("AVG Center point found: ", center_point)

if __name__ == "__main__":
    main()
