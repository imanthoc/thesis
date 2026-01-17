import matplotlib.pyplot as plt

# Data
categories = ['Bot', 'Top', 'Left', 'Right']

#278_262_A
#values1 = [0.70, 1.37, 2.89, 1.34]
#values2 = [0.87, 0.68, 1.91, 1.84]
#values3 = [0.82, 2.02, 1.33, 1.42]

#283_168_A
#values1 = [0.86, 1.30, 0.70, 1.75]
#alues2 = [3.15, 3.54, 2.18, 1.69]
#values3 = [1.21, 0.80, 1.41, 0.92]

#400_170_A
#values1 = [1.41, 0.76, 1.56, 2.30]
#values2 = [0.50, 0.77, 0.98, 0.50]
#values3 = [0.25, 0.40, 0.62, 0.25]

#504_162_A
values1 = [0.73, 1.16, 1.83, 0.48]
values2 = [0.42, 1.10, 3.26, 0.50]
values3 = [0.72, 1.27, 1.89, 0.57]

# Create subplots
fig, axes = plt.subplots(1, 3)

# First bar chart
axes[0].bar(categories, values1)
axes[0].set_title('xx stdev')

# Second bar chart
axes[1].bar(categories, values2)
axes[1].set_title('yy stdev')

axes[2].bar(categories, values3)
axes[2].set_title('diag stdev')

plt.tight_layout()
plt.show()
