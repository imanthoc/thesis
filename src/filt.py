import statistics

class Filter:
    def __init__(self, func, window_size):
        self.func = func
        self.window_size = window_size
        self.window = []

    def filt(self, x):
        if len(self.window) >= self.window_size:
            self.window.pop(0)

        self.window.append(x)

        if len(self.window) > 1:
            return self.func(self.window)
        else:
            return 0

class Filter_2d:
    x_filt = None
    y_filt = None

    def __init__(self, func, window_size):
        self.x_filt = Filter(func, window_size)
        self.y_filt = Filter(func, window_size)

    def filt(self, p):
        return (self.x_filt.filt(p[0]), self.y_filt.filt(p[1]))

class AnglePack_Filter:
    def __init__(self, window_size):
        self.window_size = window_size

        self.b_filt = Filter(statistics.stdev, window_size)
        self.t_filt = Filter(statistics.stdev, window_size)
        self.l_filt = Filter(statistics.stdev, window_size)
        self.r_filt = Filter(statistics.stdev, window_size)

    def filter_b(self, b):
        return self.b_filt.filt(b)

    def filter_t(self, t):
        return self.t_filt.filt(t)

    def filter_l(self, l):
        return self.l_filt.filt(l)

    def filter_r(self, r):
        return self.r_filt.filt(r)

    def filter_angle_pack(self, b_stdev, t_stdev, l_stdev, r_stdev):

        stdev_pack = [b_stdev, t_stdev, l_stdev, r_stdev]

        median = statistics.median(stdev_pack)
        b_d = abs(b_stdev - median)
        t_d = abs(t_stdev - median)
        l_d = abs(l_stdev - median)
        r_d = abs(r_stdev - median)

        d_pack = [b_d, t_d, l_d, r_d]

        max_d = max(d_pack)
        max_i = d_pack.index(max_d)
        second_max = sorted(d_pack)[-2]

        index_pack = [0, 1, 2, 3]

        if max_d - second_max > 0.5: #reject the angle with the biggest stdev deviation from the median
            index_pack.remove(max_i)

        return index_pack
