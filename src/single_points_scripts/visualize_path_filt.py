import sys
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import statistics
from filt import *

moving_avg_active = False
moving_med_active = False 
ma_active = False
q_step = -1

def discard(x, y):
    return (x < 0 or y < 0) or (x > 1200 or y > 600)

def quantize_value(x, step):
    p1 = x - (x % step)
    p2 = p1 + step

    error1 = abs(x - p1)
    error2 = abs(x - p2)

    if error1 < error2: return p1
    else:               return p2

def visualize(csv_name, undersampling_rate):
    global moving_avg_active
    global moving_med_active
    global ma_active
    global q_step

    win_size = 50

    moving_avg = Filter_2d(statistics.mean, win_size)
    moving_med = Filter_2d(statistics.median, win_size)
    ma_filter = Filter_MA_2d(win_size)

    df = pd.read_csv(csv_name).values

    cl_passed_values = defaultdict(lambda: False)

    total_points = 0
    i = 1

    total_points = len(df)
    color_step = 1 / total_points
    current_color = 0.0

    for line in df:
        if i != undersampling_rate:
            i += 1
            continue

        cl_x = float(line[2])
        cl_y = float(line[3])
            
        if moving_avg_active:   (cl_x, cl_y) = moving_avg.filt((cl_x, cl_y))
        elif moving_med_active: (cl_x, cl_y) = moving_med.filt((cl_x, cl_y))
        elif ma_active:         (cl_x, cl_y) = ma_filter.filt((cl_x, cl_y))

        if q_step != -1:
            cl_x = quantize_value(cl_x, q_step)
            cl_y = quantize_value(cl_y, q_step)

        plt.xlim(left=0, right=650)
        plt.ylim(bottom=0, top=600)
        plt.scatter(cl_x, cl_y, color=(0, 1-current_color, current_color), marker='o')

        current_color += color_step
        i = 1


    print("Plotted {} points".format(total_points))
    plt.show()

def print_help():
    print("Usage:")
    print("python3 visualize_path.py <path CSV> <undersampling rate >= 1> [filter options]")
    print("[filter options]:")
    print("-A Moving Average Filter")
    print("-M Moving Median Filter")
    print("-MA Combine -A and -M")
    print("-Q <step> Quantize values to multiples of <step>")

def parse_filtering_options(arg_list):
    global moving_avg_active
    global moving_med_active
    global ma_active
    global q_step

    i = 0
    while i < len(arg_list):
        arg = arg_list[i]

        if arg == "-A": moving_avg_active = True
        if arg == "-M": moving_med_active = True
        if arg == "-MA": ma_active = True
        if arg == "-Q": q_step = int(arg_list[i + 1])
        
        i += 1

    if moving_avg_active and moving_med_active:
        print("Can't  have both moving filters active")
        quit()

def main():
    if len(sys.argv) < 3:
        print_help()
        quit()

    csv_name            = sys.argv[1]
    undersampling_rate  = int(sys.argv[2])

    # filter options exist
    if len(sys.argv) > 3: 
        parse_filtering_options(sys.argv)

    visualize(csv_name, undersampling_rate)


if __name__ == "__main__":
    main()
