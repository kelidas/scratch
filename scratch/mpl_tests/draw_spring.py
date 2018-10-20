import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 40


def spring(x0, y0, x1, y1, r=.2, n=2, a=75):
    dx = x1 - x0
    dy = y1 - y0
    l = np.sqrt(dx ** 2 + dy ** 2)

    x = np.array([0, 0.25, 0.75, 1])

    x = (np.tile(x, n) + np.arange(n).repeat(4)) / float(n) * r * l
    h = np.tan(a * np.pi / 180.) * x[1]
    y = np.array([0, h, -h, 0])
    y = np.tile(y, n)
    x = x + l * .5 - 0.5 * x[-1]  # l * ((x - 0.5) * r + 0.5)

    rot = np.array([[dx / l, -dy / l],
                    [dy / l, dx / l]])

    x, y = np.dot(rot, np.vstack((x, y)))

    x = np.hstack((x0, x + x0, x1))
    y = np.hstack((y0, y + y0, y1))

    return x, y


plt.scatter([0.125, 0.375, 0.625, 0.875], [
            0.625, 0.125, 0.875, 0.375], c='k', s=80)

x, y = spring(0.125, 0.625, 0.375, 0.125)
plt.plot(x, y, 'k-', lw=.5)

x, y = spring(
    0.375, 0.125, 0.625, 0.875, r=.2 * np.sqrt(0.75 ** 2 + 0.25 ** 2))
plt.plot(x, y, 'k-', lw=.5)

x, y = spring(0.625, 0.875, 0.875, 0.375)
plt.plot(x, y, 'k-', lw=.5)

x, y = spring(
    0.875, 0.375, 0.125, 0.625, r=.2 * np.sqrt(0.75 ** 2 + 0.25 ** 2))
plt.plot(x, y, 'k-', lw=.5)

x, y = spring(0.125, 0.625, 0.625, 0.875)
plt.plot(x, y, 'k-', lw=.5)

x, y = spring(0.375, 0.125, 0.875, 0.375)
plt.plot(x, y, 'k-', lw=.5)


plt.xlim(0, 1)
plt.ylim(0, 1)
plt.axes().set_aspect('equal')
plt.xticks(np.arange(0, 1.1, .25), [0, '', '', '', 1])
plt.yticks(np.arange(0, 1.1, .25), ['', '', '', '', 1])
plt.grid(lw=1.5)

plt.tight_layout()
plt.savefig('AE-analogie.pdf')
plt.show()
