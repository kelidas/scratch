'''
Crosssectional properties of polygon
'''
from traits.api import \
    HasTraits, Instance, Property, cached_property, List, Bool, Array, Float, Tuple, Interface, implements
import matplotlib.pyplot as plt
from numpy import insert, loadtxt, array, matrix, array_equiv, sum, cos, arctan, pi, sin, sqrt
from numpy.linalg import det, inv, solve
import pylab as p
from matplotlib.patches import Ellipse
import matplotlib.figure as fig


class ICrossProp(Interface):

    local = Bool()

    A = Property()

    S = Property()

    c = Property()

    I = Property()

    I_loc = Property()

    Dyz = Property()

    Dyz_loc = Property()

    Ip = Property()

    Ip_loc = Property()

    PrincipalValues = Property()


class Polygon(HasTraits):

    implements(ICrossProp)

    pol = Array(input = True)

    local = Bool(False, input = True)

    A = Property(Float, depends_on = 'input')
    @cached_property
    def _get_A(self):
        '''
            Computes crossectional area
        '''
        pol = self.pol
        A = sum(pol[:-1, 0] * pol[1:, 1] - pol[1:, 0] * pol[:-1, 1])
        return abs(A / 2.)

    S = Property(Tuple, depends_on = 'input')
    @cached_property
    def _get_S(self):
        '''
            Computes first moment of area, axis 'y' (hor) or 'z' (ver)
        '''
        if self.local:
            pol = self.pol.copy()
            pol[:, 0] -= self.c[0]
            pol[:, 1] -= self.c[1]
        else:
            pol = self.pol
        Sy = sum((pol[1:, 0] - pol[:-1, 0]) *
                (pol[:-1, 1] ** 2 + pol[:-1, 1] * pol[1:, 1] + pol[1:, 1] ** 2))
        Sz = sum((-1) * (pol[1:, 1 ] - pol[:-1, 1]) *
                (pol[:-1, 0] ** 2 + pol[:-1, 0] * pol[1:, 0] + pol[1:, 0] ** 2))
        return Sy / 6., Sz / 6.

    c = Property(Tuple, depends_on = 'input')
    @cached_property
    def _get_c(self):
        Sy = sum((pol[1:, 0] - pol[:-1, 0]) *
                (pol[:-1, 1] ** 2 + pol[:-1, 1] * pol[1:, 1] + pol[1:, 1] ** 2)) / 6.
        Sz = sum((-1) * (pol[1:, 1 ] - pol[:-1, 1]) *
                (pol[:-1, 0] ** 2 + pol[:-1, 0] * pol[1:, 0] + pol[1:, 0] ** 2)) / 6.
        c_y = Sz / self.A
        c_z = Sy / self.A
        return c_y, c_z

    I = Property(Tuple, depends_on = 'input')
    @cached_property
    def _get_I(self):
        '''
            Computes second moment of area, axis 'y' (hor) or 'z' (ver)
        '''
        if self.local:
            print 'dfaf'
            pol = self.pol.copy()
            pol[:, 0] -= self.c[0]
            pol[:, 1] -= self.c[1]
        else:
            pol = self.pol
        Iy = sum((pol[:-1, 0] * pol[1:, 1] - pol[1:, 0] *
                                  pol[:-1, 1]) * (pol[:-1, 1] ** 2 + pol[:-1, 1] *
                                                   pol[1:, 1] + pol[1:, 1] ** 2))
        Iz = sum((-1) * (pol[:-1, 1] * pol[1:, 0] - pol[1:, 1] *
                                  pol[:-1, 0]) * (pol[:-1, 0] ** 2 + pol[:-1, 0] *
                                                   pol[1:, 0] + pol[1:, 0] ** 2))
        return abs(Iy / 12.), abs(Iz / 12.)

    Dyz = Property(Float, depends_on = 'input')
    @cached_property
    def _get_Dyz(self):
        '''
            Computes product moment of area
        '''
        if self.local:
            pol = self.pol.copy()
            pol[:, 0] -= self.c[0]
            pol[:, 1] -= self.c[1]
        else:
            pol = self.pol
        I = sum((pol[:-1, 0] * pol[1:, 1] - pol[1:, 0] * pol[:-1, 1]) *
                (pol[:-1, 0] * pol[1:, 1] + 2 * pol[:-1, 0] * pol[:-1, 1] + 2 * pol[1:, 0] *
                  pol[1:, 1] + pol[1:, 0] * pol[:-1, 1]))
        return -I / 24.

    Ip = Property(Float, depends_on = 'input')
    @cached_property
    def _get_Ip(self):
        '''
            Computes polar moment of inertia
        '''
        if self.local:
            pol = self.pol.copy()
            pol[:, 0] -= self.c[0]
            pol[:, 1] -= self.c[1]
        else:
            pol = self.pol
        I = sum((pol[1:, 0] + pol[:-1, 0]) * (pol[1:, 0] ** 2 + pol[:-1, 0] ** 2) *
                (pol[1:, 1] - pol[:-1, 1]) - (pol[1:, 1] + pol[:-1, 1]) *
                (pol[1:, 1] ** 2 + pol[:-1, 1] ** 2) * (pol[1:, 0] - pol[:-1, 0]))
        return abs(I / 12.)

    PrincipalValues = Property(Float, depends_on = 'input')
    @cached_property
    def _get_PrincipalValues(self):
        '''
            Computes principal inertia values and angle from global axes to 
            principal inertia orientation
        '''
        Iy, Iz = self.I
        Dyz = self.Dyz
        if (Iy == Iz):
            return [Iy, Iz, 0.]
        if (Dyz == 0.):
            if (Iy > Iz):
                return [Iy, Iz, 0.]
            else:
                return [Iz, Iy, .5 * pi]
        beta = 0.5 * arctan(2 * Dyz / (Iz - Iy))
        c = cos(beta)
        s = sin(beta)
        I1 = c * c * Iy + s * s * Iz - 2 * c * s * Dyz
        I2 = s * s * Iy + c * c * Iz + 2 * c * s * Dyz
        if (I1 > I2):
            return [I1, I2, beta]
        else:
            return [I2, I1, beta + 0.5 * pi]

#    w = Property(Float, depends_on = 'input')
#    @cached_property
#    def _get_w(self, pol = 'y'):
#        '''
#            Computes elastic section modulus, pol = axis 'y' (hor) or 'z' (ver)
#        '''
#        pol = self.pol
#        par = 0
#        if pol == 'y':
#            par = 1
#        w1 = pol_second_moment_of_area(pol, pol) / abs(max(pol[:, par]))
#        w2 = pol_second_moment_of_area(pol, pol) / abs(min(pol[:, par]))
#        return w1, w2

#    def cut(A, B, z = 4 / 3.):
#        C = [0., z]
#        D = [1., z]
#        uy = B[0] - A[0]
#        uz = B[1] - A[1]
#        vy = D[0] - C[0]
#        vz = D[1] - C[1]
#        if det(array([[uy, vy], [uz, vz]])) <> 0.0:
#    ##        if  (uz == 0 and vz == 0):
#    ##            intersec = array( A[0],z )
#    ##        else:
#    ##            print 'tady?'
#            intersec = solve(matrix([[-uz, uy], [-vz, vy]]), matrix([[(B[0] - A[0]) * A[1] - (B[1] - A[1]) * A[0]], [(D[0] - C[0]) * C[1] - (D[1] - C[1]) * C[0]]])).T
#        else:
#            return 'parallel'
#        return array(intersec).tolist()[0]

    def __all__(self):
        A = self.A
        print '\t A', A

        print 'K POCATKU SOURADNEHO SYSTEMU'
        self.local = False
        S_y, S_z = self.S
        c_y, c_z = self.c
        I_y, I_z = self.I
        D_yz = self.Dyz
        I_p = self.Ip

        print '\t S_y', S_y
        print '\t S_z', S_z
        print '\t cy', c_y
        print '\t cz', c_z
        print '\t Iy', I_y
        print '\t Iz', I_z
        print '\t Dyz', D_yz
        print '\t I_p', I_p

        print 'K TEZISTI'
        self.local = True
        S_y, S_z = self.S
        I_y, I_z = self.I
        D_yz = self.Dyz
        I_p = self.Ip
        PrincipalValues = self.PrincipalValues

        print '\t Iy', I_y
        print '\t Iz', I_z
        print '\t Dyz', D_yz
        print '\t I_p', I_p
        print '\t PrincipalValues', PrincipalValues
        I1, I2, alpha = PrincipalValues
        i1 = sqrt(I1 / A)
        i2 = sqrt(I2 / A)
        print i1, i2

        fig = p.figure()
        ax = fig.add_subplot(111)
        e = Ellipse((c_y, c_z), width = i1 * 2, height = i2 * 2, angle = alpha * 180 / pi + 90, fill = False)
        ax.plot(self.pol[:, 0], self.pol[:, 1])
        ax.plot(self.c[0], self.c[1], 'ro')
        ax.add_patch(e)
        p.show()


#
#w, h = fig.figaspect(2.)
#plt.figure(0, figsize = (w, h))
#plt.subplot(211)
#x = pol[:, 0]
#y = pol[:, 1]
#plt.plot(x.T, y.T)
#plt.plot(c_y, c_z, 'ro')
#plt.grid(True)
#move = (max(pol[:, 0]) - min(pol[:, 0])) / 75.
#plt.text(c_y + move, c_z, 'T[%.2f, %.2f]' % (c_y, c_z), horizontalalignment = 'left', verticalalignment = 'center')
#
#print 'K TEZISTI'
#pol[:, 0] -= c_y
#pol[:, 1] -= c_z
#
#A = pol_area(pol)
#S_y, S_z = pol_first_moment_of_area(pol)
#c_y, c_z = pol_centroid(pol)
#I_y, I_z = pol_second_moment_of_area(pol)
#D_yz = pol_product_moment_of_area(pol)
#I_p = pol_polar_moment_of_inertia(pol)
##w_ely1, w_ely2 = pol_elastic_section_modulus(pol, 'y')
##w_elz1, w_elz2 = pol_elastic_section_modulus(pol, 'z')
#
#print '\t A', A
#print '\t S_y', S_y
#print '\t S_z', S_z
#print '\t cy', c_y
#print '\t cz', c_z
#print '\t Iy', I_y
#print '\t Iz', I_z
#print '\t Dyz', D_yz
#print '\t I_p', I_p
##print '\t w_ely', w_ely1, w_ely2
##print '\t w_elz', w_elz1, w_elz2
#
#plt.subplot(212)
#x = pol[:, 0]
#y = pol[:, 1]
#plt.plot(x.T, y.T)
#plt.plot(c_y, c_z, 'ro')
#plt.grid(True)
#move = (max(pol[:, 0]) - min(pol[:, 0])) / 75.
#plt.text(c_y + move, c_z, 'T[%.2f, %.2f]' % (c_y, c_z), horizontalalignment = 'left', verticalalignment = 'center')
#
##plt.show()
#
#
#
#
#
#
#
#
#
#
#
#
#z = pol_first_moment_of_area(pol)[0] / pol_area(pol)
#P1 = []
#P2 = []
#for i in range(0, len(pol) - 1):
#    cut_P = cut(pol[i, :], pol[i + 1, :], z)
#    print 'cut %i' % (i), cut_P
#    if pol[i, 1] > z:
#        P1.append(pol[i, :])
#    if cut_P != 'parallel' and (pol[i, 1] < cut_P[1] < pol[i + 1, 1] or pol[i, 1] > cut_P[1] > pol[i + 1, 1]):
#        P1.append(cut_P)
#    if pol[i, 1] < z:
#        P2.append(pol[i, :])
#    if cut_P != 'parallel' and (pol[i, 1] < cut_P[1] < pol[i + 1, 1] or pol[i, 1] > cut_P[1] > pol[i + 1, 1]):
#        P2.append(cut_P)
#if pol[len(pol) - 1, 1] > z:
#    P1.append(pol[len(pol) - 1, :])
#if pol[len(pol) - 1, 1] < z:
#    P2.append(pol[len(pol) - 1, :])
#P1 = array(P1)
#P2 = array(P2)
#if array_equiv(P1[0, :], P1[len(P1) - 1, :]) == False:
#    P1 = insert(P1, len(P1), P1[0, :], axis = 0)
#if array_equiv(P2[0, :], P2[len(P2) - 1, :]) == False:
#    P2 = insert(P2, len(P2), P2[0, :], axis = 0)
#print 'P1', P1, 'P2', P2
#
#print 'A1', pol_area(P1), 'A2', pol_area(P2), '=', pol_area(P1) + pol_area(P2)
#plt.figure(0)
#plt.subplot(211)
#plt.plot(P1[:, 0], P1[:, 1], 'go', linewidth = 3)
#plt.plot(P2[:, 0], P2[:, 1], 'rx', linewidth = 1)
#
#
#pol.figure()
#pol.plot(pol[:, 0], pol[:, 1], 'bo-')
#pol.show()


if __name__ == '__main__':

    # polygon nodes -- clockwise
    #pol = array([[80,130],[80,-130],[-80,-130],[-80,130]], dtype='f')
    #pol = array([[130.,80.],[130.,-80.],[-130.,-80.],[-130.,80.]], dtype='f')
    #pol = array([[1,-1],[-2,-1],[-1,1],[1,1]], dtype='f')
    ##pol = array([[-50,10],[50,10],[50,0],[5,0],[5,-100],[-5,-100],[-5,0],[-50,0]],dtype='f')
    #pol = array([[-100, 0], [-100, 20], [100, 20], [100, 0], [6, 0], [6, -240], [-6, -240], [-6, 0]], dtype = 'f')
    #pol=loadtxt('char.dat', dtype='f')
    #pol=loadtxt('char_2.dat', dtype='f')

    #pol = array([[0, 0], [0, 6], [1, 6], [1, 0]], dtype = 'f')

    ##################################################
    # StatikaI - str.110
    # A = 10
    # Sy = 20.833
    # Sz = 10.833
    # yt = 1.083
    # zt = 2.083
    # Iy = 19.095
    # Iz = 4.932
    # Dyz = -3.820
    # alfa = 14s10m
    # I1 = 20.06
    # I2 = 3.968
    # i1 = 1.416
    # i2 = 0.63
    pol = array([[0, 0], [0, 5], [1, 5], [3, 0]], dtype = 'f')

    pol = insert(pol, len(pol), pol[0, :], axis = 0)

    cross = Polygon(pol = pol)
    cross.__all__()










