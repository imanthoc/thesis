import numpy as np
import matplotlib.pyplot as plt
import statistics
from filt import *

mm = Filter(statistics.median, 30)

# -------------------------------
# Define the discrete signal x[n]
# -------------------------------
n = np.arange(0, 1000)                     # Sample index
noise = np.random.normal(loc=0, scale=1.5, size=1000)      # Example signal
x = np.sin(2 * np.pi * 5 * n / 1000)
x = x + noise
x_filt = [mm.filt(x0) for x0 in x]

# -------------------------------
# Compute the Fourier Transform
# -------------------------------
X = np.fft.fft(x)
X_mag = np.abs(X)
freq = np.fft.fftfreq(len(X), d=1)

# Shift zero frequency to center
X_mag = np.fft.fftshift(X_mag)
freq = np.fft.fftshift(freq)


plt.plot(n, x, label = "Noisy x[n]")
plt.plot(n, x_filt, color='red', linewidth=2, label="Filtered x[n]")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.title("Moving Median with window size = 30")
plt.legend()
plt.show()
