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