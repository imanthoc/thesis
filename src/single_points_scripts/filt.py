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

        return self.func(self.window)

class Filter_2d:
    x_filt = None
    y_filt = None

    def __init__(self, func, window_size):
        self.x_filt = Filter(func, window_size)
        self.y_filt = Filter(func, window_size)

    def filt(self, p):
        return (self.x_filt.filt(p[0]), self.y_filt.filt(p[1]))

class Filter_MA_2d:
    x_window = []
    y_window = []
    window_size = 0
    outlier_size = 0
    
    def __init__(self, window_size):
        self.window_size = window_size 
        self.outlier_size = int(self.window_size * 0.2)

    def remove_outliers(self, l):
        l.sort()
        l = l[self.outlier_size : self.window_size - self.outlier_size]

        return l

    def filt(self, p):
        if len(self.x_window) >= self.window_size:
            self.x_window.pop(0)
        if len(self.y_window) >= self.window_size:
            self.y_window.pop(0)
        
        self.x_window.append(p[0])
        self.y_window.append(p[1])

        x_list = self.x_window.copy()
        y_list = self.y_window.copy()

        if len(x_list) >= self.window_size:
            x_list = self.remove_outliers(x_list)

        if len(y_list) >= self.window_size:
            y_list = self.remove_outliers(y_list)
        
        final_x = statistics.mean(x_list)
        final_y = statistics.mean(y_list)

        return (final_x, final_y)
        