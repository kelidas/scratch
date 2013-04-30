from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
import os
import platform
import smtplib
import base64
import multiprocessing
import time
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
from recursion_mp import gn_mp_vect, dn_mp
from mp_settings import MPF_ONE, MPF_TWO, MPF_THREE
from fn_lib import  weib_cdf_vect, norm_cdf_vect, weibul_plot_vect, differentiate, sn_mp, weibl_cdf_vect

if platform.system() == 'Linux':
    DATABASE_DIR = r'/media/data/Documents/postdoc/2013/rekurze/recursion_database'
elif platform.system() == 'Windows':
    DATABASE_DIR = r'E:\Documents\postdoc\2013\rekurze\recursion_database'

res_lst = ['x',
           'ln_x',
           'gn_cdf',
           'norm_cdf',
           'weibr_cdf',
           'gn_wp',
           'norm_wp',
           'weibr_wp',
           'x_diff',
           'ln_x_diff',
           'gn_diff',
           'norm_diff',
           'sn',
           'dn',
           'weibl_wp',
           'weibl_cdf']

def send_email_smtp(sender, receiver, email):
    # Send the message via local SMTP server.
    s = smtplib.SMTP('ex07.fce.vutbr.cz', 587)
    # s.set_debuglevel( 1 )
    s.starttls()
    s.login('sadilek.v', base64.b64decode('NTA2ZnVIRXk='))
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

def data_preparation(n_fil, shape, scale, proc_id=0, n_sam=500, n_proc=1, send_msg=False, plot=True):
    n_fil = mp.mpf('%i' % n_fil)
    shape = mp.mpf('%i' % shape)
    scale = mp.mpf('%i' % scale)

    msg = 'number of filaments = %i,' % int(n_fil)
    msg += 'shape parameter = %.1f,' % int(shape)
    print msg

    #===========================================================================
    # Testing -- one x
    #===========================================================================
#    x1 = mp.exp(mp.mpf('-10'))
#    recursion_gn_mp = gn_mp_vect(x1, scale, shape, n_fil, True)
#    print 'Result of recursion_gn_mp for one x value =', recursion_gn_mp

    #===========================================================================
    # Calculate -- array of x
    #===========================================================================
    lnxa = mp.mpf('0.5')
    lnxb = mp.mpf('-4.0')
    if n_proc > 1:
        n_sam = n_sam / n_proc
    x = np.zeros(n_sam, dtype=object)
    ln_x = np.zeros(n_sam, dtype=object)
    dlnx = (lnxa - lnxb) / (n_sam * n_proc - MPF_ONE)
    for i in range(n_sam):
        ln_x[i] = lnxb + i * dlnx + (mp.mpf(proc_id) - MPF_ONE) * n_sam * dlnx
        x[i] = mp.exp(ln_x[i])

    start = sysclock()
    recursion_gn_mp = gn_mp_vect(x, scale, shape, n_fil, False)
    gn_arr_time = sysclock() - start
    msg += 'gn_mp running time = %f' % gn_arr_time
    print msg

    #===========================================================================
    # Calculate additional values
    #===========================================================================
    scale_r = scale / mp.power(n_fil, MPF_ONE / shape)
    weibr_cdf = weib_cdf_vect(x, shape, scale_r)

    c = mp.exp(-MPF_ONE / shape)
    std_est = (mp.power(shape, -MPF_ONE / shape) *
               scale * mp.sqrt(c * (MPF_ONE - c)) / mp.sqrt(n_fil))
    mean_est = (mp.power(shape , -MPF_ONE / shape) * scale * c +
                mp.power(n_fil, -MPF_TWO / MPF_THREE) * scale *
                mp.power(shape , -(MPF_ONE / shape + MPF_ONE / MPF_THREE)) *
                mp.exp(-MPF_ONE / (MPF_THREE * shape)) * mp.mpf('0.996'))
    norm_cdf = norm_cdf_vect(x, mean_est, std_est)

    #===========================================================================
    # Calculate values for Weibull plot
    #===========================================================================
    gn_wp = weibul_plot_vect(recursion_gn_mp)
    norm_wp = weibul_plot_vect(norm_cdf)
    weibr_wp = weibul_plot_vect(weibr_cdf)
    dn = dn_mp(scale, shape, n_fil)
    sn = sn_mp(dn, scale, shape, n_fil)
    weibl_cdf = weibl_cdf_vect(x, sn, shape, n_fil)
    weibl_cdf[weibl_cdf > 1] = MPF_ONE
    weibl_wp = weibul_plot_vect(weibl_cdf)

    #===========================================================================
    # Calculate values for differentiations (different array length)
    #===========================================================================
    x_diff = (x[:-1] + x[1:]) / MPF_TWO

    ln_x_diff = (ln_x[:-1] + ln_x[1:]) / MPF_TWO

    gn_diff = (differentiate(ln_x, gn_wp) - shape) / (shape * n_fil - shape)

    norm_diff = (differentiate(ln_x, norm_wp) - shape) / (shape * n_fil - shape)

    #===========================================================================
    # Save arrays
    #===========================================================================
    name = 'n=%04i_m=%.1f' % (n_fil, shape)
    dir_name = os.path.join('m=%05.1f' % shape, 'n=%04i_m=%.1f' % (n_fil, shape))
    if os.access(dir_name, os.F_OK) == False:
        if os.access('m=%05.1f' % shape, os.F_OK) == False:
            os.mkdir('m=%05.1f' % shape)
        os.mkdir(dir_name)
    if n_proc > 1:
        name = '%02i_n=%04i_m=%.1f' % (proc_id, n_fil, shape)
    for res in res_lst:
        np.save(os.path.join(dir_name, name + '-' + res + '.npy'), locals()[res])

    # data = np.vstack((ln_x.T, x.T, recursion_gn_mp.T, gn_wp.T)).T
    # np.save('n=%02i_m=%.3f_mod.npy' % (n_fil, shape), data)

    logfile = open('recursion.log', 'a')
    logfile.write(msg + '\n')
    logfile.close()

    #===========================================================================
    # Send mail
    #===========================================================================
    if send_msg:
        email = generate_email('sadilek.v@fce.vutbr.cz',
                               'kelidas@centrum.cz',
                               'Task n = %i finished in time = %.3f.' % (n_fil, gn_arr_time))
        try:
            send_email_smtp('sadilek.v@fce.vutbr.cz',
                            'kelidas@centrum.cz',
                            email.as_string())
        except:
            pass

    #===========================================================================
    # Plot
    #===========================================================================
    if plot:
        plt.figure()
        plt.plot(x, recursion_gn_mp, 'g-x')
        plt.plot(x, norm_cdf, 'r-x')
        plt.plot(x, weibr_cdf, 'b-x')

        plt.figure()
        plt.plot(ln_x_diff, gn_diff, 'g-x')
        plt.plot(ln_x_diff, norm_diff, 'r-x')

        plt.figure()
        plt.plot(ln_x, gn_wp, 'g-x')
        plt.plot(ln_x, norm_wp, 'r-x')
        plt.plot(ln_x, weibr_wp, 'b-x')

        plt.show()

def execute_pool(func, args_lst, kwds, send_msg=False):
    '''Using all available CPUs but one for evaluation of a function
    '''
    try:
        CPU_NUM = multiprocessing.cpu_count() - 1
        pool = multiprocessing.Pool(processes=CPU_NUM)
        for arg in args_lst:
            pool.apply_async(func, args=arg, kwds=kwds)
        print 'pool map complete'
    except (KeyboardInterrupt, SystemExit):
        print 'got ^C while pool mapping, terminating the pool'
        pool.terminate()
        print 'pool is terminated'
    except Exception, e:
        print 'got exception: %r, terminating the pool' % (e,)
        pool.terminate()
        print 'pool is terminated'
    finally:
        print 'joining pool processes'
        pool.close()
        pool.join()
        print 'join complete'
    if send_msg:
        email = generate_email('sadilek.v@fce.vutbr.cz',
                               'kelidas@centrum.cz',
                               'Pool finished.')
        try:
            send_email_smtp('sadilek.v@fce.vutbr.cz',
                            'kelidas@centrum.cz',
                            email.as_string())
        except:
            pass
    print 'the end'

if __name__ == '__main__':
    #===========================================================================
    # Default run
    # data_preparation(n_fil, shape, scale=1, proc_id=0, n_sam=500, n_proc=1, send_msg=False, plot=True)
    #===========================================================================
    shape = mp.mpf('6.')
    scale = mp.mpf('1.')
    n_fil = mp.mpf('1000')
#    r = os.path.split(os.getcwd())[-1].split('=')
#    if len(r) > 1:
#        shape = mp.mpf('%i' % r[-1])

#    n_sam = 500.
#    n_proc = 1
#    data_preparation(n_fil, shape, scale=1, proc_id=0, n_sam=500, n_proc=1, send_msg=False, plot=True)

    #===========================================================================
    # Run more n (<30) and more shape
    #===========================================================================
#    shape = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 24, 40, 50, 100]
#    n_fil = np.arange(3, 51, 1)
#    shape_len = len(shape)
#    n_len = len(n_fil)
#    n_fil = n_fil.repeat(shape_len)
#    shape = shape * n_len
#    scale = np.ones_like(n_fil)
#
#
#    execute_pool(data_preparation,
#                 args_lst=zip(n_fil, shape, scale),
#                 kwds=dict(plot=False),
#                 send_msg=False)

    #===========================================================================
    # Run more n (<30) and more shape
    #===========================================================================
    n_proc = 10
    shape = np.array([3])  # np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 24, 40, 50, 100])
    n_fil = np.array([60, 70, 80, 90, 100, 150, 200, 250, 300, 400, 500])
    len_shape_orig = len(shape)
    len_n_orig = len(n_fil)

    shape = list(shape.repeat(n_proc)) * len_n_orig
    proc_id = (list(np.arange(1, n_proc + 1, 1)) * len_shape_orig) * len_n_orig

    n_fil = n_fil.repeat(n_proc * len_shape_orig)
    scale = np.ones_like(proc_id)
    print zip(n_fil, shape, scale, proc_id)
#    execute_pool(data_preparation,
#                 args_lst=zip(n_fil, shape, scale, proc_id),
#                 kwds=dict(n_sam=500, n_proc=n_proc, plot=False),
#                 send_msg=True)


