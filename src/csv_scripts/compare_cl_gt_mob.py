import sys
import pandas as pd
import math

def calc_error(gt_x, gt_y, cl_x, cl_y):
    return math.sqrt( (gt_x - cl_x)**2 + (gt_y - cl_y)**2 )

def compare_csvs(path_name, gt_name):
    path_df = pd.read_csv(path_name).values
    gt_df = pd.read_csv(gt_name).values

    print("GT time, NAN, PATH start, PATH end, GT x, GT y, PATH x, PATH y, PATH qx, PATH qy, distance")

    gt_row = 0
    while gt_row < len(gt_df):
        gt_time = int(gt_df[gt_row][0])
        gt_x    = int(gt_df[gt_row][2])
        gt_y    = int(gt_df[gt_row][3])

        path_row = 0
        while path_row < len(path_df) - 1:
            path_start = int(path_df[path_row][0])
            path_end   = int(path_df[path_row][1])

            if gt_time >= path_start and gt_time <= path_end:
                break
            else:
                path_row += 1

        path_start = int(path_df[path_row][0])
        path_end   = int(path_df[path_row][1])
        path_x     = int(path_df[path_row][2])
        path_y     = int(path_df[path_row][3])
        path_qx     = int(path_df[path_row][4])
        path_qy     = int(path_df[path_row][5])

        msg = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
                    gt_time, -1, path_start, path_end, gt_x, gt_y, path_x, path_y, path_qx, path_qy, calc_error(gt_x, gt_y, path_x, path_y))
        print(msg)

        gt_row += 1

def print_help():
    print("Usage:")
    print("python3 compare_cl_gt_mob.py <calculated_path csv> <gt csv>")

def main():
    if len(sys.argv) != 3:
        print_help()
        quit()

    path_name = sys.argv[1]
    gt_name = sys.argv[2]

    compare_csvs(path_name, gt_name)

if __name__ == "__main__":
    main()
