import os
from fnmatch import fnmatch
import re
import numpy as np
import fn_lib
import multiprocessing
from database_prep import DATABASE_DIR

CPU_NUM = multiprocessing.cpu_count() - 1

def execute_pool(func, args_lst):
    try:
        pool = multiprocessing.Pool(processes=CPU_NUM)
        pool.map_async(func, args_lst)
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

def load_lists(dir_name, pattern):
    name_lst = []
    path_lst = []
    for path, subdirs, files in os.walk(dir_name):
        for name in files:
            if fnmatch(name, pattern):
                name_lst.append(name)
                path_lst.append(path)
    return name_lst, path_lst

def wp_calc(n_p):
    data = np.load(os.path.join(n_p[1], n_p[0]))
    weibr_wp = fn_lib.weibul_plot_vect(data)
    np.save(os.path.join(n_p[1], n_p[0][:-len('-weibr_cdf.npy')] + '-weibr_wp.npy'), weibr_wp)
    print n_p[0]


if __name__ == '__main__':
    from fn_lib import sn_mp
    from utils.database_check import load_subdir_lists
    import mpmath as mp
    import matplotlib.pyplot as plt
    from utils.database_check import Selector
    import scipy.stats as stats
    s = Selector(d=os.path.join(DATABASE_DIR, 'm=005.0'))
    dir_name = s.d
    subdir_lst, path_lst = load_subdir_lists(s.d)
    subdir_lst.sort()


    # ===========================================================================
    # Calculate dk, sk
    # ===========================================================================
    from recursion_mp import dn_mp
    from mp_settings import MPF_ONE
    from utils.database_check import load_subdir_lists
    import mpmath as mp
    from fn_lib import dk_approx


    for sub in subdir_lst:
        print sub
        m = re.findall(r'm=(\d+.\d+)_n=(\d+)', sub)
        n = mp.mpf(m[0][1])
        shape = mp.mpf(m[0][0])
        scale = MPF_ONE


        gn_wp = np.load(os.path.join(s.d, sub, sub + '-gn_wp.npy'))
        ln_x = np.load(os.path.join(s.d, sub, sub + '-ln_x.npy'))
        dk = []
        for k in range(1, int(m[0][1]) + 1):
            dk.append(dk_approx(k, scale, shape, gn_wp, ln_x))

        sk = []
        for d in dk:
            sk.append(MPF_ONE / d ** (MPF_ONE / (n * shape)))

        dk = np.array(dk, dtype=object)
        print os.path.join(s.d, sub, sub + '-dk.npy'), dk

        sk = np.array(sk, dtype=object)
        print os.path.join(s.d, sub, sub + '-sk.npy'), sk
        np.save(os.path.join(s.d, sub, sub + '-dk.npy'), dk)
        np.save(os.path.join(s.d, sub, sub + '-sk.npy'), sk)



#     # ===========================================================================
#     # Calculate dn, sn
#     # ===========================================================================
#     from recursion_mp import dn_mp
#     from mp_settings import MPF_ONE
#     from utils.database_check import load_subdir_lists
#     import mpmath as mp
#     subdir_lst, path_lst = load_subdir_lists(s.d)
#     for sub in subdir_lst:
#         print sub
#         m = re.findall(r'm=(\d+.\d+)_n=(\d+)', sub)
#         n = mp.mpf(m[0][1])
#         shape = mp.mpf(m[0][0])
#         scale = MPF_ONE
#         dn = dn_mp(scale, shape, n)
#         print os.path.join(s.d, sub, sub + '-dn.npy'), dn
#         sn_ = sn_mp(dn, scale, shape, n)
#         print os.path.join(s.d, sub, sub + '-sn.npy'), sn_
#         np.save(os.path.join(s.d, sub, sub + '-dn.npy'), dn)
#         np.save(os.path.join(s.d, sub, sub + '-sn.npy'), sn_)




#     # ===========================================================================
#     # dn analysis
#     # ===========================================================================
#     sn = []
#     n = []
#     m = 0
#     def mplog(x):
#         return mp.log(x)
#     mplog_vect = np.frompyfunc(mplog, 1, 1)
#     for sub in subdir_lst:
#         # print sub
#         m = re.findall(r'm=(\d+.\d+)_n=(\d+)', sub)
#         n.append(mp.mpf(m[0][1]))
#         shape = mp.mpf(m[0][0])
#         sn_1 = mplog_vect(np.load(os.path.join(s.d, sub, sub + '-dn.npy')))
#         sn.append(sn_1)
#         # print int(m[0][1]), float(sn_1)
#     slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(n[30:], dtype=float), np.array(sn[30:], dtype=float))
#     print m[0][0], slope, intercept
#     print r_value ** 2
# #    from scipy.optimize import curve_fit
# #    def func(x, a, b):
# #        return a * x ** 2 + b * x
# #    popt, pcov = curve_fit(func, np.array(n, dtype=float), np.array(sn, dtype=float))
# #    plt.plot(n, func(np.array(n, dtype=float), *popt), 'g-')
#     plt.plot(n, sn, 'bx-')
#     plt.plot(n, float(slope) * np.array(n, dtype=float) + float(intercept), 'r-')
#
#     plt.show()
#
#     # #==========================================================================
#     # # Calculate shift
#     # #==========================================================================
#     horizontal_line = 0.2
#     cross = []
#     n = []
#     for sub in subdir_lst:
#         print sub
#         m = re.findall(r'm=(\d+.\d+)_n=(\d+)', sub)
#         n.append(mp.mpf(m[0][1]))
#         shape = mp.mpf(m[0][0])
#         gn_diff = np.load(os.path.join(s.d, sub, sub + '-gn_diff.npy'))
#         ln_x_diff = np.load(os.path.join(s.d, sub, sub + '-ln_x_diff.npy'))
#         r, l = [np.where(gn_diff <= horizontal_line)[0].min(), np.where(gn_diff > horizontal_line)[0].max()]
#         dx = np.abs(ln_x_diff[l] - ln_x_diff[r])
#         dy = np.abs(gn_diff[l] - gn_diff[r])
#         cross.append(ln_x_diff[l] + (gn_diff[l] - horizontal_line) / dy * dx)
#     cross = np.array(cross)
#     n = np.array(n)
#     plt.plot(n, np.abs(cross))
#     plt.figure()
#     plt.plot(n[1:], np.abs(np.diff(cross) / np.diff(n)))
#     plt.figure()
#     x = np.log(np.array(n[1:], dtype=float))
#     y = np.log(np.abs(np.diff(cross).astype(float) / np.diff(n).astype(float)))
#     slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
#     print slope, intercept
#     print r_value ** 2
#     plt.plot(x, y)
#     plt.plot(x, slope * x + intercept, 'r-')
#     plt.show()

    # ===========================================================================
    # Calculate weibr_wp
    # ===========================================================================
#    pattern = r'*-weibr_cdf.npy'
#    name_lst, path_lst = load_lists(dir_name, pattern)
#    execute_pool(wp_calc, zip(name_lst, path_lst))

    # ===========================================================================
    # Calculate dn, sn
    # ===========================================================================
#    from fn_lib import dn_mp, sn, MPF_ONE
#    from database_check import load_subdir_lists
#    import mpmath as mp
#    subdir_lst, path_lst = load_subdir_lists(s.d)
#    for sub in subdir_lst:
#        print sub
#        m = re.findall(r'm=(\d+.\d+)_n=(\d+)', sub)
#        n = mp.mpf(m[0][1])
#        shape = mp.mpf(m[0][0])
#        scale = MPF_ONE
#        dn = dn_mp(scale, shape, n)
#        print os.path.join(s.d, sub, sub + '-dn.npy'), dn
#        sn_ = sn(dn, scale, shape, n)
#        print os.path.join(s.d, sub, sub + '-sn.npy'), sn_
#        np.save(os.path.join(s.d, sub, sub + '-dn.npy'), dn)
#        np.save(os.path.join(s.d, sub, sub + '-sn.npy'), sn_)

    # ===========================================================================
    # Calculate weibl_wp, weibl_cdf
    # ===========================================================================
#    from fn_lib import dn_mp, sn, MPF_ONE, weibl_cdf_vect, weibul_plot_vect
#    from database_check import load_subdir_lists
#    import mpmath as mp
#    subdir_lst, path_lst = load_subdir_lists(s.d)
#    for sub in subdir_lst:
#        print sub
#        m = re.findall(r'm=(\d+.\d+)_n=(\d+)', sub)
#        n = mp.mpf(m[0][1])
#        shape = mp.mpf(m[0][0])
#        scale = MPF_ONE
#        x=np.load(os.path.join(s.d, sub, sub + '-x.npy'))
#        sn=np.load(os.path.join(s.d, sub, sub + '-sn.npy'))
#        weibl_cdf = weibl_cdf_vect(x, sn, shape, n)
#        weibl_cdf[weibl_cdf > 1] = MPF_ONE
#        weibl_wp = weibul_plot_vect(weibl_cdf)
#        np.save(os.path.join(s.d, sub, sub + '-weibl_wp.npy'), weibl_wp)
#        np.save(os.path.join(s.d, sub, sub + '-weibl_cdf.npy'), weibl_cdf)




    print 'Finished!'
