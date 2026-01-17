import serial
import io
import time
import os
import sys
from parse import parse
import statistics
import math
from filt import *

script_format = False

def get_az(line):
    if line == None: return 500
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
    global script_format

    i = 0
    while i < len(arg_list):
        arg = arg_list[i]

        if arg == "-s": script_format = True

        i += 1

def print_with_options(th_bot, th_top, th_left, th_right):
    global script_format
    #print("BOT: {:+03d} TOP: {:+03d} LEFT: {:+03d} RIGHT: {:+03d}".format(th_bot, th_top, th_left, th_right))
    print("{:+03d} , {:+03d} , {:+03d} , {:+03d}".format(th_bot, th_top, th_left, th_right))      

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

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print_help()
        quit()
    
    parse_args(sys.argv)
    # usb connections are:
    s_bot = serial.Serial(port='/dev/ttyUSB0', baudrate=1000000, timeout=0,
                       xonxoff=False, rtscts=False, dsrdtr=True)
    s_top = serial.Serial(port='/dev/ttyUSB1', baudrate=1000000, timeout=0,
                       xonxoff=False, rtscts=False, dsrdtr=True)
    s_left = serial.Serial(port='/dev/ttyUSB2', baudrate=1000000, timeout=0,
                       xonxoff=False, rtscts=False, dsrdtr=True)
    s_right = serial.Serial(port='/dev/ttyUSB3', baudrate=1000000, timeout=0,
                       xonxoff=False, rtscts=False, dsrdtr=True)

    rejected_points = [] 
    
    while True:
        if s_bot.in_waiting:
            l_bot = s_bot.readline()
        else:
            l_bot = None

        if s_top.in_waiting:
            l_top = s_top.readline()
        else:
            l_top = None

        if s_left.in_waiting:
            l_left = s_left.readline()
        else:
            l_left = None

        if s_right.in_waiting:
            l_right = s_right.readline()
        else:
            l_right = None


        th_bot   = get_az(l_bot)
        th_top   = get_az(l_top)
        th_left  = get_az(l_left)
        th_right = get_az(l_right)

        if None not in (th_bot, th_top, th_left, th_right):
            th_bot = int(th_bot)
            th_top = int(th_top)
            th_left = int(th_left)
            th_right = int(th_right)
            th = [th_bot, th_top, th_left, th_right]
            
            if th.count(500) < 2:
                print_with_options(th_bot, th_top, th_left, th_right)

    s_bot.close()
    s_top.close()
    s_left.close()
    s_right.close()

    

if __name__ == "__main__":
    main()
