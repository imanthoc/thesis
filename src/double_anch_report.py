import serial
import io
import time
import os
import sys
from parse import parse
import statistics
import math

ROOM_H = 300
ROOM_W = 800

a_top = (300, ROOM_H)
a_right = (ROOM_W, 150)

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

def calc_point(az1, az2):
    th_top = az1 
    th_right = az2 

    (m_top, b_top)      = convert_mb(a_top, th_top, lambda th: 90 - th)
    (m_right, b_right)  = convert_mb(a_right, th_right, lambda th: -th)

    p_tr = find_common_point(m_top, b_top, m_right, b_right)

    return p_tr

def print_help(): pass

def print_data(line):
    line = line.decode("ascii")

    if line[:6] != "+UUDFP":
        r = parse("+UUDF:{},{},{},{},{},{},{},{},{},{}", line)

        if not r: return

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

        msg = "RSSI: {} AZ: {} timestamp: {} seq_num: {}".format(rssi, a1, timestamp, seq_num)

        print(msg)

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

def main():
    s1 = serial.Serial(port='/dev/ttyUSB0', baudrate=1000000, timeout=1,
                       xonxoff=False, rtscts=False, dsrdtr=True)
    s2 = serial.Serial(port='/dev/ttyUSB1', baudrate=1000000, timeout=1,
                       xonxoff=False, rtscts=False, dsrdtr=True)
    
    for (l1, l2) in zip(s1, s2):
        az1 = get_az(l1)
        az2 = get_az(l2)

        if az1 != None and az2 != None:
            az1 = int(az1)
            az2 = int(az2)
            p = calc_point(az1, az2)
            p = (int(p[0]), int(p[1]))
            print(p)


    
    s1.close()
    s2.close()

if __name__ == "__main__":
    main()