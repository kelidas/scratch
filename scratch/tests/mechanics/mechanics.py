import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def rotate(coords, angle, deg=False):
    if deg:
        angle = angle / 180 * np.pi
    c = math.cos(angle)
    s = math.sin(angle)
    rot = np.array([[c, s], [-s, c]])
    return np.dot(rot, coords)


def move(coords, dx, dz):
    return coords + np.array([dx, dz])[:, None]


def kff(E, A, I, l):
    k1 = E * A / l
    EI = E * I
    k2 = 12 * EI / l**3
    k3 = 6 * EI / l**2
    k4 = 4 * EI / l
    k5 = k4 / 2
    kff = [[k1, 0, 0, -k1, 0, 0],
           [0, k2, -k3, 0, -k2, -k3],
           [0, -k3, k4, 0, k3, k5],
           [-k1, 0, 0, k1, 0, 0],
           [0, -k2, k3, 0, k2, k3],
           [0, -k3, k5, 0, k3, k4]]
    return np.array(kff)


def kfh(E, A, I, l):
    k1 = E * A / l
    EI = E * I
    k2 = 3 * EI / l**3
    k3 = 3 * EI / l**2
    k4 = 3 * EI / l
    kfh = [[k1, 0, 0, -k1, 0, 0],
           [0, k2, -k3, 0, -k2, 0],
           [0, -k3, k4, 0, k3, 0],
           [-k1, 0, 0, k1, 0, 0],
           [0, -k2, k3, 0, k2, 0],
           [0, 0, 0, 0, 0, 0]]
    return np.array(kfh)


def khf(E, A, I, l):
    k1 = E * A / l
    EI = E * I
    k2 = 3 * EI / l**3
    k3 = 3 * EI / l**2
    k4 = 3 * EI / l
    khf = [[k1, 0, 0, -k1, 0, 0],
           [0, k2, 0, 0, -k2, -k3],
           [0, 0, 0, 0, 0, 0],
           [-k1, 0, 0, k1, 0, 0],
           [0, -k2, 0, 0, k2, k3],
           [0, -k3, 0, 0, k3, k4]]
    return np.array(khf)


def khh(E, A, l):
    khh = np.zeros((6, 6), dtype=float)
    khh[0, 0] = 1
    khh[0, 3] = 1
    khh[3, 0] = 1
    khh[3, 3] = 1
    return E * A / l * khh


def fff(fx, fz, a, l, rel=False):
    if rel:
        a *= l
    b = l - a
    fff = [-b/l * fx,
           -b**2 * (3*l-2*b) / l**3 * fz,
           a*b**2/l**2 * fz,
           -a/l*fx,
           -a**2 * (3 * l - 2*a)/l**3 * fz,
           - a**2 * b / l**2 * fz]
    return np.array(fff)


def ffh(fx, fz, a, l, rel=False):
    if rel:
        a *= l
    b = l - a
    ffh = [-b/l * fx,
           -b * (3*l**2-b**2) / 2 / l**3 * fz,
           a*b * (l+b) / 2 / l**2 * fz,
           -a/l*fx,
           -a**2 * (3 * l - a)/2/l**3 * fz,
           0]
    return np.array(ffh)


def fhf(fx, fz, a, l, rel=False):
    if rel:
        a *= l
    b = l - a
    fhf = ffh(fx, fz, b, a, l)[np.arange(6)-3]
    return fhf


def fhh(fx, fz, a, l, rel=False):
    if rel:
        a *= l
    b = l - a
    fhh = [-b/l * fx,
           -b/l * fz,
           0,
           -a/l*fx,
           -a/l * fz,
           0]
    return np.array(fhh)


def mff(m, a, l, rel=False):
    if rel:
        a *= l
    b = l - a
    mff = [0,
           -6*a*b/l**3 * m,
           b * (2*l - 3*b)/l**2 * m,
           0,
           6*a*b/l**3 * m,
           a * (2*l - 3*a)/l**2 * m]
    return np.array(mff)


def mfh(m, a, l, rel=False):
    if rel:
        a *= l
    b = l - a
    mfh = [0,
           -3*(l**2 - b**2)/2/l**3 * m,
           (l**2 - 3*b**2)/2/l**2 * m,
           0,
           -3*(l**2 - b**2)/2/l**3 * m,
           0]
    return np.array(mfh)


def mhf(m, a, l, rel=False):
    if rel:
        a *= l
    b = l - a
    mhf = mfh(m, b, a, l)[np.arange(6)-3]
    return mhf


def mhh(m, l, rel=False):
    mhh = [0,
           -m/l,
           0,
           0,
           m/l,
           0]
    return np.array(mhh)


def drawHingeSupport(ax, x, z, angle=0.0, w=0.5, h=0.7, sliding=False, gap=0.2):
    """draw hinge support"""
    bs = 0.4
    coords = np.array([[0, 0],
                       [-w*bs, h*bs],
                       [w*bs, h*bs],
                       [0, 0],
                       [-w*bs, (h+gap)*bs],
                       [w*bs, (h+gap)*bs]]).T
    coords = move(rotate(coords, angle), x, z)

    ax.plot(coords[0, :4], coords[1, :4], color='k')

    if sliding:
        ax.plot(coords[0, 4:], coords[1, 4:], color='k')


def drawClampedEnd(ax, x, z, angle=0.0, w=0.8, h=0.35):
    """Draw clamped end (all 3 dofs fixed)"""
    c = math.cos(angle)
    s = math.sin(angle)  # positive angle is clockwise, is it ok? TODO
    bs = 0.4
    ax.plot([x+c*(-w*bs), x+c*(w*bs)],
            [z+s*(-w*bs), z+s*(w*bs)],
            color='k')
    # hatching
    for i in range(4):
        ax.plot([x+c*((-w+i*h)*bs)-s*h*bs, x+c*((-w+(i+1)*h)*bs)],
                [z+s*((-w+i*h)*bs)+c*h*bs, z+s*((-w+(i+1)*h)*bs)],
                color='k')


def drawSlidingClampedEnd(ax, x, z, angle=0.0, w=0.8, h=0.35):
    """Draw sliding clamped end (fixed rotation and displacement in one direction)"""
    bs = 0.4
    w *= bs
    h *= bs
    coords = [[-w, 0],
              [w, 0],
              [-w, h],
              [w, h],
              [-2/3*w, h/2],
              [0, h/2],
              [2/3*w, h/2]]
    for i in range(4):
        coords.extend([[-w + i*h, 2*h],
                       [-w+(i+1)*h, h]])
    coords = np.array(coords).T
    coords = move(rotate(coords, angle), x, z)

    ax.plot(coords[0, :2], coords[1, :2], color='k')
    ax.plot(coords[0, 2:4], coords[1, 2:4], color='k')

    r = 0.45*h
    c1 = plt.Circle((coords[0, 4], coords[1, 4]), r, color='k', fill=False)
    c2 = plt.Circle((coords[0, 5], coords[1, 5]), r, color='k', fill=False)
    c3 = plt.Circle((coords[0, 6], coords[1, 6]), r, color='k', fill=False)
    ax.add_artist(c1)
    ax.add_artist(c2)
    ax.add_artist(c3)

    # hatching
    for i in range(4):
        ax.plot(coords[0, (7+i*2):(9+i*2)], coords[1, (7+i*2):(9+i*2)],
                color='k')


def drawFixedRotation(ax, x, z, w=0.35, h=0.35, angle=0):
    """Draw fixed rotation (only rotation is fixed)"""
    bs = 0.4
    coords = np.array([[-w, -h],
                       [-w, h],
                       [w, h],
                       [w, -h],
                       [-w, -h]]).T * bs
    coords = move(rotate(coords, angle), x, z)
    ax.plot(coords[0, :], coords[1, :], color='k')

def drawHinge(ax, x, z, r=0.35):
    """Draw hinge"""
    bs = 0.4
    c = plt.Circle((x, z), r*bs, color='k', fill=False)
    ax.add_patch(c)


def drawForce(ax, x, z, fx, fz, w=0.1, h=0.2, angle=0, fmt='{:.3f}'):
    """draw arrow with tip at x,y,z, length f, head width f*w
    and head height f*h, rotated with angle"""
    f = math.sqrt(fx**2 + fz**2)
    ftext = fmt.format(f)
    c = fx/f
    s = fz/f
    f /= math.fabs(f)
    coords = np.array([[0, 0],
                       [-c*f, -s*f],
                       [0, 0],
                       [-c*f*h-s*f*w, -s*f*h + c*f*w],
                       [0, 0],
                       [-c*f*h+s*f*w, -s*f*h - c*f*w]]).T
    coords = move(rotate(coords, angle), x, z)
    for i in range(3):
        ax.plot(coords[0, (2*i):(2+2*i)], coords[1, (2*i):(2+2*i)],
                color='k')
    ax.text(coords[0, 1], coords[1, 1], ftext)


def drawMoment(ax, x, z, m, w=0.1, h=0.2, r=0.1, angle=0, fmt='{:.3f}'):
    """draw moment arrow with center at x,z, radius size and clockwise if m<0,
    anticlockwise otherwise"""
    theta1 = 90
    theta2 = 360
    theta = theta1
    if m<0:
        theta1 += 90
        theta2 += 90
        theta = theta2
    mtext = fmt.format(m)
    mabs = math.fabs(m)
    m /= mabs
    arc = patches.Arc((x, z), 1, 1, theta1=theta1, theta2=theta2, fill=False)
    ax.add_patch(arc)

    m = 1/2
    deg2rad = np.pi / 180.0
    c = math.cos(theta*deg2rad)
    s = math.sin(theta*deg2rad)
    coords = np.array([[x + c*m, z + s*m],
                       [x + c*m -w*c + h*s, z + s*m + h*c + w*s],
                       [x + c*m, z + s*m],
                       [x + c*m +w*c + h*s, z + s*m - h*s + w*c]]).T

    for i in range(2):
        ax.plot(coords[0, (2*i):(2+2*i)], coords[1, (2*i):(2+2*i)],
                color='k')
    #ax.text(coords[0, 1], coords[1, 1], mtext)


    #glVertex3f(x,y,z+s)
    #glVertex3f(x+s*h*(1 if size<0 else -1),y,z+s*(+1+w-r))
    #glVertex3f(x,y,z+s)
    #glVertex3f(x+s*h*(1 if size<0 else -1),y,z+s*(+1-w-r))
    #glEnd()


def drawBar(ax, x1, z1, x2, z2, gap=.05, fiber=True):
    dx = x2 - x1
    dz = z2 - z1
    l = math.sqrt(dx**2 + dz**2)
    c = dx / l
    s = dz / l
    ax.plot([x1, x2], [z1, z2], color='k', lw=1.5)
    ax.plot(x1, z1, 'ko')
    if fiber:
        ax.plot([x1 - s*gap, x2 - s*gap], [z1 + c*gap, z2 + c*gap], lw=1, ls='--', color='k')


if __name__=='__main__':
    fig, ax = plt.subplots(tight_layout=True)
    drawHingeSupport(ax, 0, 0, sliding=True)
    drawClampedEnd(ax, 1, 0)
    drawSlidingClampedEnd(ax, 2, 0)
    drawHinge(ax, 5, 0)


    drawFixedRotation(ax, 3, 0)

    drawForce(ax, 6, 0, 3, 4)
    drawMoment(ax, 7, 0, 5)
    drawBar(ax, 12,0,8,-1)

    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.relim()
    ax.autoscale_view()

    plt.show()
