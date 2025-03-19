import sys
import math

#convert the point & angle representation of the line
#to a y = mx + b representation
#also due to the anchors aoa reporting a conversion function is needed for theta\

ROOM_H = 600
ROOM_W = 1200

a_bot   = (ROOM_W / 2,  0)
a_top   = (ROOM_W / 2,  ROOM_H)
a_left  = (0,           ROOM_H / 2)
a_right = (ROOM_W,      ROOM_H / 2)

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
    if m1 == m2: return None #may happen

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

def compute_point_from_angles(th_left, th_bot, th_right, th_top):
    (m_bot, b_bot)      = convert_mb(a_bot, th_bot, lambda th: 90 - th)
    (m_left, b_left)    = convert_mb(a_left, th_left, lambda th: -th)
    (m_top, b_top)      = convert_mb(a_top, th_top, lambda th: 90 - th)
    (m_right, b_right)  = convert_mb(a_right, th_right, lambda th: -th)

    p_bl = find_common_point(m_bot, b_bot, m_left, b_left)
    p_lt = find_common_point(m_left, b_left, m_top, b_top)
    p_tr = find_common_point(m_top, b_top, m_right, b_right)
    p_rb = find_common_point(m_right, b_right, m_bot, b_bot)

    # some times a common point is none if the two lines are parallel
    center_point = find_average_point([p for p in [p_bl, p_lt, p_tr, p_rb] if p is not None])

    return center_point

def quantize_value(x):
    p1 = x - (x % 60)
    p2 = p1 + 60

    error1 = abs(x - p1)
    error2 = abs(x - p2)

    if error1 < error2: return p1
    else:               return p2

def quantize_point(p):
    return (quantize_value(p[0]), quantize_value(p[1]))

def compute_csv(csv_name):
    csv_file = open(csv_name, "r")

    anchor_found = { "6501": False, "6502": False, "6503": False, "6504": False }
    timestamps = []
    c = 0
    for line in csv_file:
        data = line.strip().split(',')
        anchor = data[7]
        ts     = int(data[0])

        timestamps.append(ts)

        if anchor == "6501":
            th_left = float(data[3])
            anchor_found["6501"] = True
        elif anchor == "6502":
            th_bot = float(data[3])
            anchor_found["6502"] = True
        elif anchor == "6503":
            th_right = float(data[3])
            anchor_found["6503"] = True
        elif anchor == "6504":
            th_top = float(data[3])
            anchor_found["6504"] = True
        else:
            print("CSV format error")
            quit()

        if False not in anchor_found.values():
            p = compute_point_from_angles(th_left, th_bot, th_right, th_top)
            qp = quantize_point(p)

            print("{}, {}, {}, {}, {}, {}".format(
                min(timestamps), max(timestamps), p[0], p[1], qp[0], qp[1]
            ))

            timestamps = []

            anchor_found = { "6501": False, "6502": False, "6503": False, "6504": False }
            c += 1

    csv_file.close()

def print_help():
    print("Usage")
    print("python3 find_avg_points_csv.py <csv name>")

def main():
    if len(sys.argv) != 2:
        print_help()
        quit()

    csv_name = sys.argv[1]
    compute_csv(csv_name)

if __name__ == "__main__":
    main()
