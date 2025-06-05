import matplotlib.pyplot as plt
import numpy as np

# Data for demonstration
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)
y4 = np.exp(-x)

# Create a figure with a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Plot in each subplotfig
axs[0, 0].plot(x, y1, label='sin(x)', color='blue')
axs[0, 0].set_title('Sine Function')
axs[0, 0].legend()

axs[0, 1].plot(x, y2, label='cos(x)', color='green')
axs[0, 1].set_title('Cosine Function')
axs[0, 1].legend()

axs[1, 0].plot(x, y3, label='tan(x)', color='red')
axs[1, 0].set_title('Tangent Function')
axs[1, 0].set_ylim(-10, 10)  # Limit y-axis for better visualization
axs[1, 0].legend()

axs[1, 1].plot(x, y4, label='exp(-x)', color='purple')
axs[1, 1].set_title('Exponential Decay')
axs[1, 1].legend()

# Adjust layout for better spacing
plt.tight_layout()

# Show the figure
plt.show()
