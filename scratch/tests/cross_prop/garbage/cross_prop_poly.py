'''
Crosssectional properties of polygon
'''
from __future__ import print_function, division
import numpy as np


class Rectangle():
    def __init__(self, width, height):
        self.w = width
        self.h = height

    def get_A(self):
        return self.w * self.h

    def get_xt(self):
        return 0.5 * self.w

    def get_yt(self):
        return 0.5 * self.h

    def get_C(self):
        return self.get_xt(), self.get_yt()

    def get_Ix(self):
        return 1/12 * self.w * self.h**3

    def get_Iy(self):
        return 1/12 * self.h * self.w**3

    def get_It(self):
        return self.h * self.w / 12 * (self.w**2 + self.h**2)

    def get_poly(self):
        return np.array([[],
                         [],
                         [],
                         []])


class Triangle():
    def __init__(self, width, height, quadrant):
        self.w = width
        self.h = height
        self.q = quadrant

    def get_A(self):
        return self.w * self.h / 2

    def get_xt(self):
        return self.w / 3

    def get_yt(self):
        return 0.5 * self.h

    def get_C(self):
        return self.get_xt(), self.get_yt()

    def get_Ix(self):
        return 1/12 * self.w * self.h**3

    def get_Iy(self):
        return 1/12 * self.h * self.w**3

    def get_It(self):
        return self.h * self.w / 12 * (self.w**2 + self.h**2)

    def get_poly(self):
        return np.array([[],
                         [],
                         [],
                         []])



def area(pol):
    A = sum(pol[:-1, 0] * pol[1:, 1] - pol[1:, 0] * pol[:-1, 1])
    return - A / 2.


def centroid(pol):
    A = area(pol)
    Sy = sum((-1) * (pol[1:, 0] - pol[:-1, 0]) *
             (pol[:-1, 1] ** 2 + pol[:-1, 1] * pol[1:, 1] + pol[1:, 1] ** 2)) / 6.
    Sz = sum((pol[1:, 1] - pol[:-1, 1]) *
             (pol[:-1, 0] ** 2 + pol[:-1, 0] * pol[1:, 0] + pol[1:, 0] ** 2)) / 6.
    c_y = Sz / A
    c_z = Sy / A
    return c_y, c_z


def first_moment_of_area(pol):
    '''Computes first moment of area, axis 'y' (hor) or 'z' (ver)'''
    Sy = sum((pol[1:, 0] - pol[:-1, 0]) *
             (pol[:-1, 1] ** 2 + pol[:-1, 1] * pol[1:, 1] + pol[1:, 1] ** 2))
    Sz = sum((-1) * (pol[1:, 1] - pol[:-1, 1]) *
             (pol[:-1, 0] ** 2 + pol[:-1, 0] * pol[1:, 0] + pol[1:, 0] ** 2))
    return Sy / 6., Sz / 6.


def second_moment_of_area(pol):
    Iy = sum((pol[:-1, 0] * pol[1:, 1] - pol[1:, 0] *
              pol[:-1, 1]) * (pol[:-1, 1] ** 2 + pol[:-1, 1] *
                              pol[1:, 1] + pol[1:, 1] ** 2))
    Iz = sum((-1) * (pol[:-1, 1] * pol[1:, 0] - pol[1:, 1] *
                     pol[:-1, 0]) * (pol[:-1, 0] ** 2 + pol[:-1, 0] *
                                     pol[1:, 0] + pol[1:, 0] ** 2))
    return abs(Iy / 12.), abs(Iz / 12.)


def product_moment_of_area(pol):
    I = sum((pol[:-1, 0] * pol[1:, 1] - pol[1:, 0] * pol[:-1, 1]) *
            (pol[:-1, 0] * pol[1:, 1] + 2 * pol[:-1, 0] * pol[:-1, 1] + 2 * pol[1:, 0] *
             pol[1:, 1] + pol[1:, 0] * pol[:-1, 1]))
    return I / 24.


def polar_moment_of_inertia(pol):
    I = sum((pol[1:, 0] + pol[:-1, 0]) * (pol[1:, 0] ** 2 + pol[:-1, 0] ** 2) *
            (pol[1:, 1] - pol[:-1, 1]) - (pol[1:, 1] + pol[:-1, 1]) *
            (pol[1:, 1] ** 2 + pol[:-1, 1] ** 2) * (pol[1:, 0] - pol[:-1, 0]))
    return abs(I / 12.)


def principal_values(pol):
    '''Computes principal inertia values and angle from global axes to
    principal inertia orientation
    '''
    Iy, Iz = second_moment_of_area(pol)
    Dyz = product_moment_of_area(pol)
    if (Iy == Iz):
        return [Iy, Iz, 0.]
    if (Dyz == 0.):
        if (Iy > Iz):
            return [Iy, Iz, 0.]
        else:
            return [Iz, Iy, .5 * np.pi]
    beta = 0.5 * np.arctan(2 * Dyz / (Iz - Iy))
    c = np.cos(beta)
    s = np.sin(beta)
    I1 = c ** 2 * Iy + s ** 2 * Iz - 2 * c * s * Dyz
    I2 = s ** 2 * Iy + c ** 2 * Iz + 2 * c * s * Dyz
    beta *= 180 / np.pi
    if (I1 > I2):
        return [I1, I2, beta]
    else:
        return [I2, I1, beta + 0.5 * np.pi]


def to_centroid(pol):
    p = pol.copy().astype(float)
    c_y, c_z = centroid(p)
    p[:, 0] -= c_y
    p[:, 1] -= c_z
    return p


if __name__ == '__main__':
    pol = np.array([[0, 0],
                    [4, 0],
                    [4, 5],
                    [7, 5],
                    [7, 7],
                    [2, 7],
                    [2, 1],
                    [0, 1],
                    [0, 0]])

    #print area(pol)
    #print centroid(pol)
    #pol = to_centroid(pol)
    #print second_moment_of_area(pol)
    #print product_moment_of_area(pol)
    #print principal_values(pol)

    #import matplotlib.pyplot as plt
    #plt.plot(pol[:, 0], pol[:, 1])
    #plt.show()
