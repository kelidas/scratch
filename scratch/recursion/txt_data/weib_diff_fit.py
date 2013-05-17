import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

data = np.loadtxt('weib_diff_fit.txt', delimiter=';')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X = data[:, 0].reshape(18, 59)
Y = data[:, 1].reshape(18, 59)
Z = data[:, 2].reshape(18, 59)
ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
ax.plot_wireframe(X, Y, np.zeros_like(Z), rstride=1, cstride=1, color='green')
ax.set_xlabel('shape')
ax.set_ylabel('number of filaments')
ax.set_zlabel('weibull location')

plt.figure()
plt.plot(Y.T, (Z / Y / X).T)

plt.figure()
plt.plot(X, (Z / Y / X))
plt.show()
exit()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Z = data[:, 3].reshape(18, 59)
ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2)
ax.plot_wireframe(X, Y, np.ones_like(Z), rstride=1, cstride=1, color='green')
ax.set_xlabel('shape')
ax.set_ylabel('number of filaments')
ax.set_zlabel('weibull scale')

plt.figure()
plt.plot(Y.T, (Z / Y).T)
plt.plot(Y.T[:, 0], 1.0 / Y.T[:, 0], 'k-', linewidth=2)

plt.figure()
plt.plot(X, (Z))
plt.plot(X[:, 0], np.ones_like(X[:, 0]) , 'k-', linewidth=2)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Z = data[:, 4].reshape(18, 59)
ax.plot_wireframe(X, Y, np.log(Z), rstride=2, cstride=2)
ax.plot_wireframe(X, Y, np.log(np.ones_like(Z)), rstride=1, cstride=1, color='green')
ax.set_xlabel('shape')
ax.set_ylabel('number of filaments')
ax.set_zlabel('weibull shape')

plt.figure()
plt.plot(Y.T, (Z / Y).T)
plt.plot(Y.T[:, 0], 1.0 / Y.T[:, 0], 'k-', linewidth=2)


plt.show()
