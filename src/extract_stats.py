import sys
import statistics

ROOM_W = 660
ROOM_H = 350

def print_help():
    pass

def reject(p):
    return p[0] < 0 or p[1] < 0 or p[0] > ROOM_W or p[1] > ROOM_H

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

        if not reject((x, y)):
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

    print("X avg: ",   statistics.mean(x_list))
    print("Y avg: ",   statistics.mean(y_list))
    print("X stdev: ", statistics.stdev(x_list))
    print("Y stdev: ", statistics.stdev(y_list))
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