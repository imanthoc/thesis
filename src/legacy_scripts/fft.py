import numpy as np
import matplotlib.pyplot as plt
import statistics
from filt import *

# -------------------------------
# Define the discrete signal x[n]
# -------------------------------
n = np.arange(0, 1000)                     # Sample index
noise = np.random.normal(loc=0, scale=1.5, size=1000)      # Example signal
x = np.sin(2 * np.pi * 5 * n / 1000)
#x = x + noise

# -------------------------------
# Compute the Fourier Transform
# -------------------------------
X = np.fft.fft(x)
X_mag = np.abs(X)
freq = np.fft.fftfreq(len(X), d=1)

# Shift zero frequency to center
X_mag = np.fft.fftshift(X_mag)
freq = np.fft.fftshift(freq)

# -------------------------------
# Create subplots
# -------------------------------
plt.figure(figsize=(8, 6))

# Plot x[n]
plt.subplot(2, 1, 1)
plt.plot(n, x)
plt.xlabel("n")
plt.ylabel("x[n]")
plt.title("x[n]")
plt.grid(True)

# Plot |X(f)|
plt.subplot(2, 1, 2)
plt.plot(freq, X_mag)
plt.xlabel("Normalized Frequency")
plt.ylabel("|X(f)|")
plt.title("|X(f)|")
plt.grid(True)

plt.tight_layout()
plt.show()
