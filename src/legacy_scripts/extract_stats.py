import sys
import statistics

ROOM_W = 660
ROOM_H = 350

ROOM_W_offset = ROOM_W * (2/10)
ROOM_H_offset = ROOM_H * (2/10)

def print_help():
    pass

def reject(p):
    return p[0] < 0 or p[1] < 0 or p[0] > ROOM_W or p[1] > ROOM_H


def reject_off(p):
    return p[0] < -ROOM_W_offset or p[1] < -ROOM_H_offset or p[0] > ROOM_W + ROOM_W_offset or p[1] > ROOM_H + ROOM_H_offset

rejected = 0
total = 0

def parse_file(point_file):
    global rejected
    global total

    file = open(point_file, "r")
    point_list = []

    for line in file:
        total += 1
        (x, y) = line.split(",")
        (x, y) = (int(x), int(y))

        if not reject_off((x, y)):
            point_list.append((x, y))
        else:
            rejected += 1

    file.close()

    return point_list

def calculate_stats(point_list):
    global rejected
    global total
    x_list = [p[0] for p in point_list]
    y_list = [p[1] for p in point_list]

    print("Avg:   {} , {}".format(statistics.mean(x_list), statistics.mean(y_list)))
    print("Stdev: {} , {}".format(statistics.stdev(x_list), statistics.stdev(y_list)))
    print("Rejected {} out of {} points".format(rejected, total))

def main():
    if len(sys.argv) != 2:
        print_help()
        quit()
    
    point_file = sys.argv[1]
    
    point_list = parse_file(point_file)
    calculate_stats(point_list)

if __name__ == "__main__":
    main()
