import serial
import io
import time
import os
import sys
from parse import parse
import statistics
import math
from filt import *

moving_avg_active = False
moving_med_active = False 
q_step = -1
report_angles = False
script_format = False

moving_avg = Filter_2d(statistics.mean, 10)
moving_med = Filter_2d(statistics.median, 10)

ROOM_H = 330
ROOM_W = 660

a_top   = (ROOM_W/2+20, ROOM_H)
a_right = (ROOM_W, ROOM_H/2)
a_bot   = (ROOM_W/2+20, 0)
a_left  = (0, ROOM_H/2)

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

def calc_point(th_bot, th_top, th_left, th_right):
    (m_bot, b_bot)      = convert_mb(a_bot, th_bot, lambda th: 90 - th)
    (m_left, b_left)    = convert_mb(a_left, th_left, lambda th: -th)
    (m_top, b_top)      = convert_mb(a_top, th_top, lambda th: 90 - th)
    (m_right, b_right)  = convert_mb(a_right, th_right, lambda th: -th)

    p_bl = find_common_point(m_bot,   b_bot,   m_left,  b_left)
    p_lt = find_common_point(m_left,  b_left,  m_top,   b_top)
    p_tr = find_common_point(m_top,   b_top,   m_right, b_right)
    p_rb = find_common_point(m_right, b_right, m_bot,   b_bot)

    p_list = [p_bl, p_lt, p_tr, p_rb]

    # some times a common point is none if the two lines are parallel
    center_point = find_average_point([p for p in p_list if p is not None])

    return center_point

def quantize_value(x, step):
    p1 = x - (x % step)
    p2 = p1 + step

    error1 = abs(x - p1)
    error2 = abs(x - p2)

    if error1 < error2: return p1
    else:               return p2

def quantize_point(p, step):
    return (quantize_value(p[0], step), quantize_value(p[1], step))

def get_az(line):
    line = line.decode("ascii")

    if line[:6] != "+UUDFP":
        r = parse("+UUDF:{},{},{},{},{},{},{},{},{},{}", line)

        if not r: return None 

        tag_id  = r[0]
        rssi    = r[1]
        a1      = r[2]
        a2      = r[3]
        reserved  = r[4] 
        channel   = r[5] 
        anchor_id = r[6]
        str_nn    = r[7]
        timestamp = r[8] 
        seq_num   = r[9]

        return a1
    else:
        return None

def parse_args(arg_list):
    global moving_avg_active
    global moving_med_active
    global q_step
    global report_angles
    global script_format

    i = 0
    while i < len(arg_list):
        arg = arg_list[i]

        if arg == "-a": moving_avg_active = True 
        if arg == "-m": moving_med_active = True
        if arg == "-q": q_step = int(arg_list[i + 1])
        if arg == "-g": report_angles = True
        if arg == "-s": script_format = True

        i += 1

def print_with_options(th_bot, th_top, th_left, th_right, p):
    global moving_avg_active
    global moving_med_active
    global q_step
    global report_angles
    global script_format
    
    if report_angles:
        print("BOT: {:+03d} TOP: {:+03d} LEFT: {:+03d} RIGHT: {:+03d}".format(th_bot, th_top, th_left, th_right))
    else:
        if moving_avg_active:   p = moving_avg.filt(p)
        elif moving_med_active: p = moving_med.filt(p)

        if q_step != -1: p = quantize_point(p, q_step)

        if script_format: 
            print("0, 0, {}, {}, 0, 0".format(int(p[0]), int(p[1])))
        else:
            print("{} , {}".format(int(p[0]), int(p[1])))        

# 519
# 168
def print_help():
    print("Usage:")
    print("python3 anch_report.py [reporting options] [filter options]")
    print("[reporting options]:")
    print("-g Report Angles")
    print("-s Report in a format compatible with <visualize_path_filt.py>")

    print("[filter options]:")
    print("-a Moving Average Filter")
    print("-m Moving Median Filter")
    print("-q <step> Quantize values to multiples of <step>")

def reject(p):
    return p[0] < 0 or p[1] < 0 or p[0] > ROOM_W or p[1] > ROOM_H

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print_help()
        quit()
    
    parse_args(sys.argv)
    # usb connections are:
    # left, right, bot, top
    s_bot = serial.Serial(port='/dev/ttyUSB0', baudrate=1000000, timeout=1,
                       xonxoff=False, rtscts=False, dsrdtr=True)
    s_top = serial.Serial(port='/dev/ttyUSB3', baudrate=1000000, timeout=1,
                       xonxoff=False, rtscts=False, dsrdtr=True)
    s_left = serial.Serial(port='/dev/ttyUSB2', baudrate=1000000, timeout=1,
                       xonxoff=False, rtscts=False, dsrdtr=True)
    s_right = serial.Serial(port='/dev/ttyUSB1', baudrate=1000000, timeout=1,
                       xonxoff=False, rtscts=False, dsrdtr=True)

    rejected_points = [] 
    
    for (l_bot, l_top, l_left, l_right) in zip(s_bot, s_top, s_left, s_right):
        th_bot   = get_az(l_bot)
        th_top   = get_az(l_top)
        th_left  = get_az(l_left)
        th_right = get_az(l_right)

        if None not in (th_bot, th_top, th_left, th_right):
            th_bot = int(th_bot)
            th_top = int(th_top)
            th_left = int(th_left)
            th_right = int(th_right)

            p = calc_point(th_bot, th_top, th_left, th_right)

            print_with_options(th_bot, th_top, th_left, th_right, p)

    s_bot.close()
    s_top.close()
    s_left.close()
    s_right.close()

    

if __name__ == "__main__":
    main()