import sys
import statistics

def print_help():
    pass

def parse_file(point_file):
    file = open(point_file, "r")
    point_list = []

    for line in file:
        (x, y) = line.split(",")
        (x, y) = (int(x), int(y))
        point_list.append((x, y))

    file.close()

    return point_list

def calculate_stats(point_list):
    x_list = [p[0] for p in point_list]
    y_list = [p[1] for p in point_list]

    print("X avg: ",   statistics.mean(x_list))
    print("Y avg: ",   statistics.mean(y_list))
    print("X stdev: ", statistics.stdev(x_list))
    print("Y stdev: ", statistics.stdev(y_list))

def main():
    if len(sys.argv) != 2:
        print_help()
        quit()
    
    point_file = sys.argv[1]
    
    point_list = parse_file(point_file)
    calculate_stats(point_list)

if __name__ == "__main__":
    main()