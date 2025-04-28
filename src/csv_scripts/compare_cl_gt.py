import sys
import pandas as pd
import math

def calc_error(gt_x, gt_y, cl_x, cl_y):
    return math.sqrt( (gt_x - cl_x)**2 + (gt_y - cl_y)**2 )

def compare_csvs(cl_name, gt_name):
    cl_df = pd.read_csv(cl_name).values
    gt_df = pd.read_csv(gt_name).values

    gt_row = 0
    cl_row = 0

    print("GT start, GT end, CL start, CL end, GT x, GT y, CL x, CL y, CL qx, CL qy, distance")
    while gt_row < len(gt_df):
        r = gt_df[gt_row]

        gt_start = int(r[0])
        gt_end = int(r[1])

        gt_x     = float(r[2])
        gt_y     = float(r[3])

        # find START of corresponding data
        while (int(cl_df [cl_row] [0]) < gt_start) or (int(cl_df [cl_row] [1]) > gt_end):
            if cl_row + 1 < len(cl_df): cl_row += 1
            else: return # csv file end has been reached

        # find ALL corresponding data
        while (int(cl_df [cl_row] [0]) > gt_start) and (int(cl_df [cl_row] [1]) < gt_end):
            cl_start = int      (cl_df [cl_row] [0])
            cl_end   = int      (cl_df [cl_row] [1])

            cl_x     = float    (cl_df [cl_row] [2])
            cl_y     = float    (cl_df [cl_row] [3])
            
            cl_qx     = float    (cl_df [cl_row] [4])
            cl_qy     = float    (cl_df [cl_row] [5])

            msg = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
                    gt_start, gt_end, cl_start, cl_end, gt_x, gt_y, cl_x, cl_y, cl_qx, cl_qy, calc_error(gt_x, gt_y, cl_x, cl_y)
                )
            print(msg)

            if cl_row + 1 < len(cl_df): cl_row += 1
            else: return # csv file end has been reached

        gt_row += 1

def print_help():
    print("Usage:")
    print("python3 compare_cl_gt.py <calculated_path csv> <gt csv>")

def main():
    if len(sys.argv) != 3:
        print_help()
        quit()

    cl_name = sys.argv[1]
    gt_name = sys.argv[2]

    compare_csvs(cl_name, gt_name)

if __name__ == "__main__":
    main()
