

from numpy import sign, linspace, pi, e, mean, ones_like, sum, max, log as ln
from scipy.stats import norm
import matplotlib.pyplot as plt

d = 0.026
A = pi * d ** 2 / 4.
E = 70.e3
theta_m = 0.01
lambda_m = 0.2
ksi_m = 0.018
n_sim = 20

def H( x ):
    return sign( sign( x ) + 1.0 )

def Weibull_pdf( x, sh, sc ):
    return sh / sc * ( x / sc ) ** ( sh - 1 ) * e ** ( -( x / sc ) ** sh )

def Weibull_ppf( x, sh, sc ):
    return - sc * ( ln( 1 - x ) ) ** ( 1. / sh )

def Pullout( w, theta, lambda_, ksi ):
    q = E * A
    f = ( w - theta * ( 1 + lambda_ ) ) / ( ( 1 + theta ) * ( 1 + lambda_ ) )
    q *= f
    return q * H( w - theta * ( 1 + lambda_ ) ) * H( ksi - f )


def Spirrid( w ):
    w = w[:, None, None, None]
    theta_max = 1.
    lambda_max = 1.
    ksi_max = 1.
    theta_x = linspace( 0, theta_max, n_sim )[None, :, None, None]
    lambda_x = linspace( 0, lambda_max, n_sim )[None, None, :, None]
    ksi_x = linspace( 0, ksi_max, n_sim )[None, None, None :]
    theta = Weibull_pdf( theta_x, sh=10., sc=theta_m )
    print theta
    lambda_ = Weibull_pdf( lambda_x, sh=10., sc=lambda_m )
    ksi = Weibull_pdf( ksi_x, sh=10., sc=ksi_m )
    # todo: evaluate PDF
    dtheta = theta_max / n_sim
    dlambda = lambda_max / n_sim
    dksi = ksi_max / n_sim
    dF = theta * dtheta * lambda_ * dlambda * ksi * dksi * ones_like( w )

    q = Pullout( w, theta, lambda_, ksi ) * dF
    m = sum( q, axis= -1 ) 
    m = sum( m, axis= -1 ) 
    m = sum( m, axis= -1 )
    #m = mean( q[:-1], q[:-2], q[:-3] )
    return m

def Spirrid_LHS( w ):
    theta = linspace( 0, theta_max, n_sim )[None, :]
    lambda_ = linspace( 0, lambda_max, n_sim )[None, :]
    ksi = linspace( 0, ksi_max, n_sim )[None, :]

    q = Pullout( w, theta, lambda_, ksi )
    
    return mean( q, axis=1 )



w = linspace( 0, 100, 1000 )

m = Spirrid( w )
plt.plot( w, m )
plt.show()

