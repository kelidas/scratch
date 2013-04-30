from scipy.misc import comb
from numpy import linspace, exp, log, abs
import numpy as np
import platform
from scipy.stats import norm
import time
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
import matplotlib.pyplot as plt
import mpmath as mp
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.message import Message
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders
from email import Charset
import getpass, imaplib

def weibul_cdf(x, shape, scale):
    return mp.mpf('1.') - mp.exp(-(x / scale) ** shape)

def norm_cdf(x, mean, std):
    return mp.mpf('0.5') * (mp.mpf('1') + mp.erf((x - mean) / mp.sqrt(mp.mpf('2') * std ** 2)))

def gn_mp(x_val, scale, shape, n):
    global binom_tab
    gn_arr = np.zeros((n_fil, n_fil, n_fil), dtype=object)
    gn_arr.fill(None)
    cdf_arr = np.zeros(n_fil, dtype=object)
    cdf_arr.fill(None)
    x_arr = np.zeros(n_fil, dtype=object)
    x_arr.fill(None)

    def recursion_gn_mp(x_val, scale, shape, n):
        if x_arr[n - 1] != None:
            cdf = cdf_arr[n - 1]
        else:
            x_arr[n - 1] = x_val
            cdf = weibul_cdf(x_val, shape, scale)
            cdf_arr[n - 1] = cdf
        res = mp.mpf('0.')
        for k in range(1, int(n) + 1):
            if gn_arr[n - 1, k - 1, n - 1] != None:
                gn = gn_arr[n - 1, k - 1, n - 1]
            else:
                cdf_k = cdf ** k
                komb = binom_tab[n - 1, k - 1]
                if k != n:
                    gn = (-1) ** (k + 1) * komb * cdf_k * recursion_gn_mp((n / (n - k)) * x_val, scale, shape, n - k)
                else:
                    gn = (-1) ** (k + 1) * komb * cdf_k  #* 1.0
                gn_arr[n - 1, k - 1, n - 1] = gn
            res += gn
        return res
    #start = sysclock()
    gn_m = recursion_gn_mp(x_val, scale, shape, n)
    #print 'gn_mp time =', sysclock() - start
    return gn_m

gn_mp_vect = np.frompyfunc(gn_mp, 4, 1)

def differentiate(x, y):
    return np.diff(y) / np.diff(x)

def send_email_smtp(sender, receiver, email):
    # Send the message via local SMTP server.
    s = smtplib.SMTP('ex07.fce.vutbr.cz', 587)
    #s.set_debuglevel( 1 )
    s.starttls()
    s.login('sadilek.v', '506fuHEy')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, receiver, email)
    s.quit()

def generate_email(sender, receiver, subject):
    frame = MIMEMultipart(u'related')
    frame['From'] = sender
    frame['To'] = receiver
    frame['Subject'] = subject
    msg = MIMEMultipart(u'alternative')
    frame.attach(msg)

    return frame


if __name__ == '__main__':
    #===========================================================================
    # Settings
    #===========================================================================
    from settings import *

    print 'number of filaments =', n_fil
    #print gn_arr.nbytes / 1024.**2

    #===========================================================================
    # Testing -- one x
    #===========================================================================
    xx = mp.mpf('-10')
    xx = mp.exp(xx)

    #----- Modified implementation
    recursion_gn_mp = gn_mp(xx, scale, shape, n_fil)
    print 'Results', recursion_gn_mp


    #===========================================================================
    # Calculate -- array of x
    #===========================================================================
    lnxa = mp.mpf('0.5')
    lnxb = mp.mpf('-4.0')
    #ln_x = np.linspace(lnxa, lnxb, n_sam)  #np.arange(lnxb, 1., (lnxa - lnxb) / n_sam)
    #xx = linspace(-4, 1., 20)
    x = np.zeros(n_sam, dtype=object)
    ln_x = np.zeros(n_sam, dtype=object)
    dlnx = (lnxa - lnxb) / (n_sam - mp.mpf('1.0'))
    for i in range(int(n_sam)):
        ln_x[i] = lnxb + i * dlnx
        x[i] = mp.exp(ln_x[i])

    #recursion_gn_mp = np.zeros(x.shape, dtype=object)
    start = sysclock()
    recursion_gn_mp = gn_mp_vect(x, scale, shape, n_fil)
#    for idx, x_v in enumerate(x):
#        recursion_gn_mp[idx] = gn_mp(x_v, scale, shape, n_fil)
    gn_arr_time = sysclock() - start
    print 'gn_mp time =', gn_arr_time



    #===========================================================================
    # Calculate additional values
    #===========================================================================
    #cdf_weib = weibul_cdf(ln_x, shape, scale)
    c = mp.exp(-1 / shape)
    std_est = mp.power(shape, -1 / shape) * scale * mp.sqrt(c * (1 - c)) / mp.sqrt(n_fil);
    mean_est = (mp.power(shape , -1 / shape) * scale * c +
                mp.power(n_fil, -2.0 / 3.0) * scale * mp.power(shape , -(1.0 / shape + 1.0 / 3.0)) * mp.exp(-1.0 / (3 * shape)) * 0.996)
    norm_cdf = np.zeros(x.shape, dtype=object)
    for idx, x_v in enumerate(x):
        norm_cdf[idx] = norm_cdf(x_v, mean_est, std_est)

    #===========================================================================
    # Calculate values for Weibull plot
    #===========================================================================
    gn_wp = np.zeros_like(recursion_gn_mp)
    for i, g in enumerate(recursion_gn_mp):
        gn_wp[i] = mp.log(-mp.log(1 - g)).real

    wp_norm = np.zeros_like(norm_cdf)
    for i, g in enumerate(norm_cdf):
        wp_norm[i] = mp.log(-mp.log(1 - g)).real

    #gn2 = log(-log(1 - gn))
    #gn3 = log(-log(1 - recursion_gn_mp))

    #===========================================================================
    # Calculate values for differentiations (different array length)
    #===========================================================================
    ln_x_diff = (ln_x[:-1] + ln_x[1:]) / mp.mpf(2.0)
    gn_diff = (differentiate(ln_x, gn_wp) - shape) / (shape * n_fil - shape)
    norm_diff = (differentiate(ln_x, wp_norm) - shape) / (shape * n_fil - shape)

    #===========================================================================
    # Save arrays
    #===========================================================================

    np.save('n=%02i_m=%.3f_mod-x.npy' % (n_fil, shape), x)
    np.save('n=%02i_m=%.3f_mod-ln_x.npy' % (n_fil, shape), ln_x)
    np.save('n=%02i_m=%.3f_mod-recursion_gn_mp.npy' % (n_fil, shape), recursion_gn_mp)
    np.save('n=%02i_m=%.3f_mod-norm_cdf.npy' % (n_fil, shape), norm_cdf)

    np.save('n=%02i_m=%.3f_mod-gn_wp.npy' % (n_fil, shape), gn_wp)
    np.save('n=%02i_m=%.3f_mod-wp_norm.npy' % (n_fil, shape), wp_norm)

    np.save('n=%02i_m=%.3f_mod-ln_x_diff.npy' % (n_fil, shape), ln_x_diff)
    np.save('n=%02i_m=%.3f_mod-gn_diff.npy' % (n_fil, shape), gn_diff)
    np.save('n=%02i_m=%.3f_mod-norm_diff.npy' % (n_fil, shape), norm_diff)

    #data = np.vstack((ln_x.T, x.T, recursion_gn_mp.T, gn_wp.T)).T
    #np.save('n=%02i_m=%.3f_mod.npy' % (n_fil, shape), data)

    #===========================================================================
    # Send mail
    #===========================================================================
#    email = generate_email('sadilek.v@fce.vutbr.cz',
#                           'kelidas@centrum.cz',
#                           'Task n = %i finished in time = %.3f.' % (n_fil, gn_arr_time))
#    try:
#        send_email_smtp('sadilek.v@fce.vutbr.cz',
#                        'kelidas@centrum.cz',
#                        email.as_string())
#    except:
#        pass

    #===========================================================================
    # Plot
    #===========================================================================

    #plt.plot(x, gn1, 'b-x')
    #plt.plot(x, gn2, 'r-x')

    plt.figure()
    plt.plot(x, recursion_gn_mp, 'g-x')
    plt.plot(x, norm_cdf, 'r-x')

    plt.figure()
    plt.plot(ln_x_diff, gn_diff, 'g-x')
    plt.plot(ln_x_diff, norm_diff, 'r-x')

    plt.figure()
    plt.plot(ln_x, gn_wp, 'g-x')
    plt.plot(ln_x, wp_norm, 'r-x')
    plt.show()


