import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('target_LHS_32sim.txt', skiprows=1)
data = np.loadtxt('target_exp.txt', skiprows=1)

plt.plot(data.T)
plt.show()
