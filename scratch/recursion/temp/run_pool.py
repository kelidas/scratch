import multiprocessing
import os
import shutil
import threading
import subprocess
import numpy as np
import platform
import time
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
from recursion_mp import *
import mpmath as mp

mp.mp.dps = 1000

CPU_NUM = 2  #multiprocessing.cpu_count()

def execute_pool(func, arg_lst):
    try:
        pool = multiprocessing.Pool(processes=CPU_NUM)
        pool.map_async(func, arg_lst)
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
    print 'the end'

def gn_distributed(proc_id, n, shape, scale, x_arr):

    global param_arr
    global cdf_arr
    global x_arr
    global recursion_gn_mp
    global binom_tab
    global n_sam_1

    #===========================================================================
    # Calculate -- array of x
    #===========================================================================
    start = sysclock()
    for idx, x_v in enumerate(x):
        param_arr[proc_id] = np.zeros((n, n, n), dtype=object)
        x_arr[proc_id] = np.array([], dtype=object)
        cdf_arr[proc_id] = np.array([], dtype=object)
        recursion_gn_mp[proc_id * n_sam_1 + idx] = gn_mp(x_v, scale, shape, n)
    print 'gn_mp time =', sysclock() - start

    #===========================================================================
    # Calculate additional values
    #===========================================================================
    #cdf_weib = weibul_cdf(ln_x, shape, scale)
    c = mp.exp(-1 / shape)
    std_est = mp.power(shape, -1 / shape) * scale * mp.sqrt(c * (1 - c)) / mp.sqrt(n);
    mean_est = (mp.power(shape , -1 / shape) * scale * c +
                mp.power(n, -2.0 / 3.0) * scale * mp.power(shape , -(1.0 / shape + 1.0 / 3.0)) * mp.exp(-1.0 / (3 * shape)) * 0.996)
    cdf_norm = np.zeros(x.shape, dtype=object)
    for idx, x_v in enumerate(x):
        cdf_norm[idx] = norm_cdf(x_v, mean_est, std_est)

    #===========================================================================
    # Calculate values for Weibull plot
    #===========================================================================
    wp_gn = np.zeros_like(recursion_gn_mp)
    for i, g in enumerate(recursion_gn_mp):
        wp_gn[i] = mp.log(-mp.log(1 - g)).real

    wp_norm = np.zeros_like(cdf_norm)
    for i, g in enumerate(cdf_norm):
        wp_norm[i] = mp.log(-mp.log(1 - g)).real

    #gn2 = log(-log(1 - gn))
    #gn3 = log(-log(1 - recursion_gn_mp))

    #===========================================================================
    # Calculate values for differentiations (different array length)
    #===========================================================================
    ln_x_diff = (ln_x[:-1] + ln_x[1:]) / mp.mpf(2.0)
    gn_diff = (differentiate(ln_x, wp_gn) - shape) / (shape * n - shape)
    norm_diff = (differentiate(ln_x, wp_norm) - shape) / (shape * n - shape)

    #===========================================================================
    # Save arrays
    #===========================================================================

    np.save('n=%02i_m=%.3f_mod-x.npy' % (n, shape), x)
    np.save('n=%02i_m=%.3f_mod-ln_x.npy' % (n, shape), ln_x)
    np.save('n=%02i_m=%.3f_mod-recursion_gn_mp.npy' % (n, shape), recursion_gn_mp)
    np.save('n=%02i_m=%.3f_mod-cdf_norm.npy' % (n, shape), cdf_norm)

    np.save('n=%02i_m=%.3f_mod-wp_gn.npy' % (n, shape), wp_gn)
    np.save('n=%02i_m=%.3f_mod-wp_norm.npy' % (n, shape), wp_norm)

    np.save('n=%02i_m=%.3f_mod-ln_x_diff.npy' % (n, shape), ln_x_diff)
    np.save('n=%02i_m=%.3f_mod-gn_diff.npy' % (n, shape), gn_diff)
    np.save('n=%02i_m=%.3f_mod-norm_diff.npy' % (n, shape), norm_diff)


if __name__ == '__main__':

    #===========================================================================
    # Settings
    #===========================================================================
    shape = mp.mpf('20.')
    scale = mp.mpf('1.')
    n = mp.mpf('10')

    param_arr = [np.zeros((n, n, n), dtype=object)] * CPU_NUM
    cdf_arr = [np.array([], dtype=object)] * CPU_NUM
    x_arr = [np.array([], dtype=object)] * CPU_NUM
    binom_tab = np.load('binomial_tab/binom_tab.npy')

    n_sam = 100.
    lnxa = 0.5
    lnxb = -4.0
    ln_x = np.linspace(lnxa, lnxb, n_sam)
    x = np.exp(ln_x)
    x_lst = []
    n_sam_1 = n_sam / CPU_NUM
    for i in range(CPU_NUM):
        x_lst.append(x[i * n_sam_1:(i + 1) * n_sam_1])
    proc_id_lst = range(CPU_NUM)
    n_lst = [n] * CPU_NUM
    shape_lst = [shape] * CPU_NUM
    scale_lst = [scale] * CPU_NUM
    recursion_gn_mp = np.zeros(x.shape, dtype=object)

    cmd_lst = zip(proc_id_lst, n_lst, shape_lst, scale_lst, x_lst)
    execute_pool(gn_distributed, cmd_lst)
