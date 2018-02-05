'''
Crosssectional properties of polygon
http://www.efunda.com/math/areas/Common_Geometric_Shapes_Index.cfm
'''
from __future__ import print_function, division
import configparser
import ast
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
import shapely
from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon
params = {'text.usetex': True, 'mathtext.fontset': 'stix'}
plt.rcParams.update(params)
plt.rcParams["font.family"] = "serif"


def rot(th):
    return np.array([[np.cos(th), np.sin(th)],
                     [-np.sin(th), np.cos(th)]])


def radius_i(I, A):
    return np.sqrt(I / A)


q_sign = {1: (1, 1),
          2: (-1, 1),
          3: (-1, -1),
          4: (1, -1)}

base_props = ['A', 'xt', 'yt', 'Ixt', 'Iyt', 'Dxyt', 'It']
props = ['ixt', 'iyt', 'I1', 'I2', 'theta', 'i1', 'i2']


class Shape():
    def __init__(self):
        self._init_props()
        self._calculate()

    def _init_props(self):
        for i in base_props:
            setattr(self, i, 0)
        for i in props:
            setattr(self, i, 0)

    @property
    def C(self):
        return self.xt, self.yt

    def _calculate(self):
        self._calculate_baseprops()
        self._calculate_props()

    def _calculate_baseprops(self):
        return NotImplementedError()

    def _calculate_props(self):
        self.ixt = radius_i(self.Ixt, self.A)
        self.iyt = radius_i(self.Iyt, self.A)
        a = (self.Ixt + self.Iyt) / 2
        b = np.sqrt((self.Ixt - self.Iyt)**2 + 4 * self.Dxyt**2) / 2
        self.I1 = a+b
        self.I2 = a-b
        self.i1 = radius_i(self.I1, self.A)
        self.i2 = radius_i(self.I2, self.A)
        dif = self.Iyt - self.Ixt
        self.theta = 0.5 * np.arctan2(2 * self.Dxyt, dif)


class SingleShape(Shape):

    def __init__(self, **kwds):
        self.point = kwds.get('point', (0, 0))
        self.px, self.py = self.point
        self.angle = kwds.get('angle', 0) / 180 * np.pi
        self.hollow = -1 if kwds.get('hollow', False) else 1
        super().__init__()
        # self.ref_point = kwds.get('ref_point', self.C)
        # self.rx, self.ry = self.ref_point
        self._calculate()

    def _calculate(self):
        self._calculate_baseprops()
        self._move()
        if self.angle != 0:
            self._rotate()
        self._calculate_props()

    def _move(self):
        self.xt += self.px
        self.yt += self.py
        self.poly += np.array(self.point)

    def _rotate(self):
        I = np.array([[self.Ixt, -self.Dxyt],
                      [-self.Dxyt, self.Iyt]])
        r = rot(self.angle)
        Irot = np.dot(np.dot(r, I), r.T)
        self.Ixt = Irot[0, 0]
        self.Iyt = Irot[1, 1]
        self.Dxyt = -Irot[0, 1]
        self.xt, self.yt = np.dot(r, self.C)
        self.poly = np.dot(r, self.poly.T).T


class Rectangle(SingleShape):
    def __init__(self, width, height, **kwds):
        self.w = width
        self.h = height
        super().__init__(**kwds)

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        if value <= 0:
            raise ValueError("Width has to be positive.")
        self._w = value
        #if value: self.calculate()

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        if value <= 0:
            raise ValueError("Height has to be positive.")
        self._h = value
        #if value: self.calculate()

    def _calculate_baseprops(self):
        self.A = self.w * self.h
        self.xt = 0.5 * self.w
        self.yt = 0.5 * self.h
        self.Ixt = 1/12 * self.w * self.h**3
        self.Iyt = 1/12 * self.h * self.w**3
        self.Dxyt = 0
        self.It = self.h * self.w / 12 * (self.w**2 + self.h**2)
        self.poly = np.array([[0, 0],
                             [self.w, 0],
                             [self.w, self.h],
                             [0, self.h],
                             [0, 0]])


class Circle(SingleShape):
    def __init__(self, radius, **kwds):
        self.r = radius
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = np.pi * self.r**2
        self.xt = 0
        self.yt = 0
        self.Ixt = np.pi * self.r**4 / 4
        self.Iyt = self.Ixt
        self.Dxyt = 0
        self.It = np.pi * self.r**4 / 2
        poly = Point((0, 0)).buffer(self.r, resolution=100)
        self.poly = np.array(poly.exterior.coords)


class SemiCircle(SingleShape):
    def __init__(self, radius, **kwds):
        self.r = radius
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = np.pi * self.r**2 / 2
        self.xt = 0
        self.yt = 4 * self.r / 3 / np.pi
        self.Ixt = (np.pi / 8 - 8 / 9 / np.pi) * self.r**4
        self.Iyt = np.pi * self.r**4 / 8
        self.Dxyt = 0
        self.It = np.pi * self.r**4 / 4
        poly = Point((0, 0)).buffer(self.r, resolution=100)
        p = Polygon(np.array([[-self.r, -self.r],
                             [self.r, -self.r],
                             [self.r, 0],
                             [-self.r, 0]]))
        poly = poly.difference(p)
        self.poly = np.array(poly.exterior.coords)


class QuarterCircle(SingleShape):
    def __init__(self, radius, quadrant=1, **kwds):
        self.r = radius
        self.q = quadrant
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = np.pi * self.r**2 / 4
        s1, s2 = np.array(q_sign[self.q])
        self.xt = s1 * 4 * self.r / 3 / np.pi
        self.yt = s2 * 4 * self.r / 3 / np.pi
        self.Ixt = (np.pi / 16 - 4 / 9 / np.pi) * self.r**4
        self.Iyt = self.Ixt
        sign = 1 if self.q in [1, 3] else -1
        self.Dxyt = sign * (1 / 8 - 4 / 9 / np.pi) * self.r**4
        self.It = (np.pi / 8 - 8 / 9 / np.pi) * self.r**4
        poly = Point((0, 0)).buffer(self.r, resolution=100)
        p = Polygon(np.array([[-self.r, -self.r],
                             [self.r, -self.r],
                             [self.r, 0],
                             [0, 0],
                             [0, self.r],
                             [-self.r, self.r]]) * 1.1 *
                                 np.array(q_sign[self.q]))
        poly = poly.difference(p)
        self.poly = np.array(poly.exterior.coords)


class Ellipse(SingleShape):
    def __init__(self, a, b, **kwds):
        self.a = a
        self.b = b
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = np.pi * self.a * self.b
        self.xt = 0
        self.yt = 0
        self.Ixt = np.pi * self.a * self.b**3 / 4
        self.Iyt = np.pi * self.b * self.a**3 / 4
        self.Dxyt = 0
        self.It = np.pi / 4 * self.a * self.b * (self.a**2 + self.b**2)
        poly = Point((0, 0)).buffer(1, resolution=100)
        poly = shapely.affinity.scale(py, self.a, self.b)
        self.poly = np.array(poly.exterior.coords)


class SemiEllipse(SingleShape):
    def __init__(self, a, b, **kwds):
        self.a = a
        self.b = b
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = np.pi * self.a * self.b / 2
        self.xt = 0
        self.yt = 4 * self.b / 3 / np.pi
        self.Ixt = (np.pi / 8 - 8 / 9 / np.pi) * self.a * self.b**3
        self.Iyt = (np.pi / 8 - 8 / 9 / np.pi) * self.b * self.a**3
        self.Dxyt = 0
        self.It = (np.pi / 8 - 8 / 9 / np.pi) * (self.a**3 * self.b +
                                                  self.b**3 * self.a)
        poly = Point((0, 0)).buffer(1, resolution=100)
        poly = shapely.affinity.scale(py, self.a, self.b)
        p = Polygon(np.array([[-self.a, -self.b],
                             [self.a, -self.b],
                             [self.a, 0],
                             [-self.a, 0]]) * 1.1)
        poly = poly.difference(p)
        self.poly = np.array(poly.exterior.coords)


class QuarterEllipse(SingleShape):
    def __init__(self, a, b, quadrant=1, **kwds):
        self.a = a
        self.b = b
        self.q = quadrant
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = np.pi * self.a * self.b / 4
        s1, s2 = np.array(q_sign[self.q])
        self.xt = s1 * 4 * self.a / 3 / np.pi
        self.yt = s2 * 4 * self.b / 3 / np.pi
        self.Ixt = (np.pi / 16 - 4 / 9 / np.pi) * self.a * self.b**3
        self.Iyt = (np.pi / 16 - 4 / 9 / np.pi) * self.b * self.a**3
        sign = 1 if self.q in [1, 3] else -1
        self.Dxyt = - sign * (1 / 8 - 4 / 9 / np.pi) * self.a**2 * self.b**2
        self.It = (np.pi / 16 - 4 / 9 / np.pi) * (self.a**3 * self.b +
                                                  self.b**3 * self.a)
        poly = Point((0, 0)).buffer(1, resolution=100)
        poly = shapely.affinity.scale(poly, self.a, self.b)
        p = Polygon(np.array([[-self.a, -self.b],
                             [self.a, -self.b],
                             [self.a, 0],
                             [0, 0],
                             [0, self.b],
                             [-self.a, self.b]]) * 1.1 * np.array(q_sign[self.q]))
        poly = poly.difference(p)
        self.poly = np.array(poly.exterior.coords)


class Parabola(SingleShape):
    def __init__(self, b, h, **kwds):
        self.b = b
        self.h = h
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = 4 / 3 * self.b * self.h
        self.xt = 0
        self.yt = 2 / 5 * self.h
        self.Ixt = 16 / 175 * self.b * self.h**3
        self.Iyt = 4 / 15 * self.h * self.b**3
        self.Dxyt = 0
        self.It = 4 * self.b * self.h * (35 * self.b**2 + 12 * self.h**2) / 525
        x = np.linspace(-self.b, self.b, 100)
        a = self.h / (self.b)**2
        y = -a * x**2 + self.h
        poly = Polygon(np.vstack((x, y)).T)
        self.poly = np.array(poly.exterior.coords)


class SemiParabola(SingleShape):
    def __init__(self, b, h, quadrant=1, **kwds):
        self.b = b
        self.h = h
        self.q = quadrant
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = 2 / 3 * self.b * self.h
        s1, s2 = np.array(q_sign[self.q])
        self.xt = s1 * 3 / 8 * self.b
        self.yt = s2 * 2 / 5 * self.h
        self.Ixt = 8 / 175 * self.b * self.h**3
        self.Iyt = 19 / 480 * self.h * self.b**3
        sign = -1 if self.q in [1, 3] else 1
        self.Dxyt = sign * self.b**2 * self.h**2 / 60
        self.It = self.b * self.h * (665 * self.b**2 + 768 * self.h**2) / 16800
        # check
        x = np.linspace(0, self.b, 100)
        a = self.h / (self.b)**2
        y = -a * x**2 + self.h
        poly = np.vstack(([0, 0], np.vstack((x, y)).T))
        poly = Polygon(py * np.array(q_sign[self.q]))
        self.poly = np.array(poly.exterior.coords)


class ParabolaSpandrel(SingleShape):
    def __init__(self, b, h, quadrant=1, **kwds):
        self.b = b
        self.h = h
        self.q = quadrant
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = self.b * self.h / 3
        s1, s2 = np.array(q_sign[self.q])
        self.xt = s1 * 3 / 4 * self.b
        self.yt = s2 * 3 / 10 * self.h
        self.Ixt = 37 / 2100 * self.b * self.h**3
        self.Iyt = 1 / 80 * self.h * self.b**3
        sign = 1 if self.q in [1, 3] else -1
        self.Dxyt = sign * self.b**2 * self.h**2 / 120
        self.It = self.b * self.h * (35 * self.b**2 + 111 * self.h**2) / 6300
        x = np.linspace(0, self.b, 100)
        y = self.h * x**2 / self.b**2
        poly = np.vstack(([self.b, 0], np.vstack((x, y)).T))
        poly = Polygon(py * np.array(q_sign[self.q]))
        self.poly = np.array(poly.exterior.coords)


class Triangle(SingleShape):
    def __init__(self, width, height, quadrant=1, **kwds):
        self.w = width
        self.h = height
        self.q = quadrant
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = self.w * self.h / 2
        s1, s2 = np.array(q_sign[self.q])
        self.xt = self.w / 3 * s1
        self.yt = self.h / 3 * s2
        self.Ixt = 1/36 * self.w * self.h**3
        self.Iyt = 1/36 * self.h * self.w**3
        sign = -1 if self.q in [1, 3] else 1
        self.Dxyt = self.h**2 * self.w**2 / 72 * sign
        self.It = self.h * self.w / 36 * (self.w**2 + self.h**2)
        poly = np.array([[0, 0],
                         [self.w, 0],
                         [0, self.h],
                         [0, 0]]) * np.array(q_sign[self.q])
        self.poly = poly


class CompositeShape(Shape):
    def __init__(self, shapes, **kwds):
        self.shapes = shapes
        super().__init__(**kwds)
        for s in self.shapes:
            s.ref_point = self.C

    def _calculate_baseprops(self):
        for s in self.shapes:
            self.A += s.A * s.hollow
            self.xt += s.A * s.xt * s.hollow
            self.yt += s.A * s.yt * s.hollow
        self.xt /= self.A
        self.yt /= self.A
        for s in self.shapes:
            self.Ixt += (s.Ixt + s.A * (self.yt - s.yt)**2) * s.hollow
            self.Iyt += (s.Iyt + s.A * (self.xt - s.xt)**2) * s.hollow
            self.Dxyt += (s.Dxyt +
                          s.A * (self.xt - s.xt)*(self.yt - s.yt)) * s.hollow
        self.It = np.nan


    def draw_mpl(self, ax):
        for s in self.shapes:
            poly = s.poly
            # ax.plot(poly[:, 0], poly[:, 1],
            #        color='r' if s.hollow == -1 else 'b')
            if s.hollow == -1:
                p = patches.Polygon(poly, True, ec='r', fill=False,
                                    hatch='xx', zorder=100, alpha=.4)
            else:
                p = patches.Polygon(poly, True, ec='b', alpha=.4, zorder=0)
            ax.add_patch(p)

            ax.plot(s.xt, s.yt, 'kx', ms=3)

        i1 = self.i1
        i2 = self.i2
        p = patches.Ellipse(self.C, i1, i2, fill=False,
                            angle=self.theta*180/np.pi, ec='k')
        ax.add_patch(p)
        line = np.array([[-i1, i1], [0, 0]])
        l1 = np.dot(rot(self.theta).T, line).T + self.C
        ax.plot(l1[:, 0], l1[:, 1], 'k-.', lw=.8)
        l2 = np.dot(rot(self.theta+np.pi/2).T, line).T + self.C
        ax.plot(l2[:, 0], l2[:, 1], 'k-.', lw=.8)

        x, y = self.xt, self.yt
        ax.plot(x, y, 'g+')
        ax.text(x*1.02, y*1.02, 'T', color='g')
        ax.autoscale_view()

        ax.grid()
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')

    @classmethod
    def fromtxt(cls, fname):
        config = configparser.ConfigParser(strict=True)
        config.read(fname)
        sections = config.sections()
        shapes = []
        for section in sections:
            items = config[section].items()
            params = {key: ast.literal_eval(val) for key, val in items}
            shapes.append(shape_dict.get(section.split()[0])(**params))
        return cls(shapes)


class PolygonShape(SingleShape):
    def __init__(self, polygon, **kwds):
        self.poly = np.asanyarray(polygon)
        super().__init__(**kwds)

    def _calculate_baseprops(self):
        self.A = np.sum(self.poly[:-1, 0] * self.poly[1:, 1] -
                        self.poly[1:, 0] * self.poly[:-1, 1]) / 2
        if self.A < 0 and self.hollow == 1:
            self.poly = self.poly[::-1, :]
        p = self.poly.copy()
        Sx = np.sum((-1) * (p[1:, 0] - p[:-1, 0]) * (p[:-1, 1] ** 2 +
                    p[:-1, 1] * p[1:, 1] + p[1:, 1] ** 2)) / 6.
        Sy = np.sum((p[1:, 1] - p[:-1, 1]) * (p[:-1, 0] ** 2 +
                    p[:-1, 0] * p[1:, 0] + p[1:, 0] ** 2)) / 6.
        self.xt = Sy / self.A
        self.yt = Sx / self.A
        p -= self.C
        self.Ixt = np.sum((p[:-1, 0] * p[1:, 1] - p[1:, 0] * p[:-1, 1]) *
                          (p[:-1, 1] ** 2 + p[:-1, 1] * p[1:, 1] +
                          p[1:, 1] ** 2)) / 12
        self.Iyt = np.sum((-1) * (p[:-1, 1] * p[1:, 0] - p[1:, 1] * p[:-1, 0]) *
                          (p[:-1, 0] ** 2 + p[:-1, 0] * p[1:, 0] +
                          p[1:, 0] ** 2)) / 12
        self.Dxyt = np.sum((p[:-1, 0] * p[1:, 1] - p[1:, 0] * p[:-1, 1]) *
                           (p[:-1, 0] * p[1:, 1] + 2 * p[:-1, 0] * p[:-1, 1] +
                           2 * p[1:, 0] * p[1:, 1] + p[1:, 0] * p[:-1, 1])) / 24
        self.It = np.sum((p[1:, 0] + p[:-1, 0]) * (p[1:, 0] ** 2 + p[:-1, 0] ** 2) *
                         (p[1:, 1] - p[:-1, 1]) - (p[1:, 1] + p[:-1, 1]) *
                         (p[1:, 1] ** 2 + p[:-1, 1] ** 2) *
                         (p[1:, 0] - p[:-1, 0])) / 12


shape_dict = {'Rectangle': Rectangle,
              'Circle': Circle,
              'SemiCircle': SemiCircle,
              'QuarterCircle': QuarterCircle,
              'Ellipse': Ellipse,
              'SemiEllipse': SemiEllipse,
              'QuarterEllipse': QuarterEllipse,
              'Parabola': Parabola,
              'SemiParabola': SemiParabola,
              'ParabolaSpandrel': ParabolaSpandrel,
              'Triangle': Triangle,
              'PolygonShape': PolygonShape}

if __name__ == '__main__':
    r = Rectangle(5, 10)
    print(r.point)
    print(r.hollow)
    # r = CompositeShape([(Rectangle(5, 10), (1, 5), False),
    #                     (Rectangle(2, 3), (3, 6), True)])
    r = CompositeShape([Rectangle(.4, .6, point=(0, 0), hollow=False),
                        Circle(.1, point=(.2, .4), hollow=True),
                        Triangle(.2, .3, 2, point=(0, 0), hollow=False)])
    r = CompositeShape([Rectangle(.1, .6, point=(-0.05, 0), hollow=False),
                        Rectangle(.6, .1, point=(-.3, .6), hollow=False)])
    r = CompositeShape([Rectangle(.1, .5, point=(-0.05, 0), hollow=False, angle=np.pi/4),
                        Rectangle(.6, .1, point=(-.55, .5), hollow=False, angle=np.pi/4)])
    r = CompositeShape([Rectangle(.5, .5, point=(0, 0), hollow=False, angle=np.pi/4),
                        QuarterEllipse(.25, .2, quadrant=2, point=(0.5, .5), hollow=False, angle=np.pi/4)])

    r = CompositeShape([Rectangle(.4, .6, point=(0, 0), hollow=False),
                        Circle(.1, point=(.2, .4), hollow=True),
                        Triangle(.2, .3, 2, point=(0, 0), hollow=False)])

    r = CompositeShape([Rectangle(.04, .22, point=(0, 0.13), hollow=False),
                        Rectangle(.22, .08, point=(0, 0.05), hollow=False),
                        Circle(.01, point=(.19, .1), hollow=True),
                        Triangle(.05, .05, 4, point=(0, 0.05), hollow=False)])

    r = CompositeShape([Rectangle(4, 1, point=(0, 0), hollow=False),
                        Rectangle(2, 4, point=(2, 1), hollow=False),
                        Rectangle(5, 2, point=(2, 5), hollow=False)])

    r = CompositeShape([Rectangle(.12, .02, point=(0, 0), hollow=False),
                        Triangle(.06, .045, quadrant=2, point=(0.06, .02), hollow=False),
                        Rectangle(.03, .045, point=(.09, .02), hollow=False)])

    r = CompositeShape.fromtxt('docs/examples/example.ini')

    r = CompositeShape([Rectangle(.4, .6, point=(0, 0), hollow=False),
                        Circle(.1, point=(.2, .4), hollow=True),
                        Triangle(.2, .3, 2, point=(0, 0), hollow=False)])


    #r = CompositeShape([PolygonShape([[0, 0],
    #                                  [.2, 0],
    #                                  [0, .3],
    #                                  [0, 0]])])
    #r = CompositeShape([Triangle(.2, .3, 1, point=(0, 0), hollow=False)])

    r = CompositeShape([Rectangle(.4, .6, point=(0, 0), hollow=False),
                        Circle(.1, point=(.2, .4), hollow=True),
                        Triangle(.2, .3, 2, point=(0, 0), hollow=False)])
    r = CompositeShape([PolygonShape([[-.2, 0],
                                      [.4, 0],
                                      [0.4, .6],
                                      [0, .6],
                                      [0, 0.3],
                                      [-.2, 0]]),
                        Circle(.1, point=(.2, .4), hollow=True)])

    #r = CompositeShape.fromtxt('docs/examples/Rectangle.ini')
    r = CompositeShape([PolygonShape([[0, 0],
                                      [1, 0],
                                      [1, .8],
                                      [1.9, 1.7],
                                      [-.3, 1.7],
                                      [0, .8],
                                      [0, 0]]),
                        Circle(.3, point=(.5, 1.2), hollow=True)])

    r = CompositeShape.fromtxt('docs/examples/Polygon_Triangle_rot.ini')
    print(r.shapes[0].poly)
    for i in base_props:
        print(i, getattr(r, i))
    print('theta =', r.theta * 180 / np.pi)

    for i in props:
        print(i, getattr(r, i))
    #print(r.i1t)
    #print(r.i2t)

    fig, ax = plt.subplots(tight_layout=True)
    r.draw_mpl(ax)
    ax.set_aspect('equal')
    plt.show()
