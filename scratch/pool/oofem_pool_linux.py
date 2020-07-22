
import multiprocessing
import os
import subprocess
import sys
import time
import glob

def execute_pool(func, cpu_num, args_lst, kwds):
    try:
        pool = multiprocessing.Pool(processes=cpu_num)
        for arg in args_lst:
            pool.apply_async(func, args=[arg], kwds=kwds)
        print('pool apply complete')
    except (KeyboardInterrupt, SystemExit):
        print('got ^C while pool mapping, terminating the pool')
        pool.terminate()
        print('pool is terminated')
    except Exception as e:
        print('got exception: %r, terminating the pool' % (e,))
        pool.terminate()
        print('pool is terminated')
    finally:
        print('joining pool processes')
        pool.close()
        pool.join()
        print('join complete')
    print('the end' )
    
def run_oofem(cmd_lst):
    print(cmd_lst[1], 'running ...')
    sys.stdout.flush()
    t = time.time()
    outfile = os.path.join(cmd_lst[0], 'results', cmd_lst[1][:-3]+'.out')
    if os.path.exists(outfile):
        print(outfile, '-- exists')
        return
    logfile = os.path.join(cmd_lst[0], cmd_lst[1][:-3]+'.log')
    with open(logfile, "w") as fnull:
        # p = subprocess.Popen('konsole -e ls -la', stdout=fnull, shell=True)
        p = subprocess.Popen('cd %s; /home/jan/oofem/release/oofem -f %s' % (cmd_lst[0], cmd_lst[1]), shell=True, stderr=fnull, stdout=fnull)
        p.communicate()
        pass
    print(cmd_lst[1], 'finished')
    print('time %.3f min' % ((time.time() - t) / 60))
    sys.stdout.flush()

if __name__ == '__main__':
    #cdir = os.getcwd()
    pcs = [101, 102, 103, 104, 105, 106, 39,
       108, 109, 110, 111, 112, 113,
       114, 115, 116, 117, 119, 126, 121, 122, 123, 124]
    
    CPU_NUM = multiprocessing.cpu_count()-1
    
    if not os.path.exists(os.path.join('DYN_nsim=40_nrun=30', 'results')):
        os.mkdir(os.path.join('DYN_nsim=40_nrun=30', 'results'))
    
    lst = glob.glob('DYN_nsim=40_nrun=30/*.in')
    #lst = ['DYN/Bb_nsim=0002_run=01_sim=0001.in', 'DYN/Bb_nsim=0005_run=10_sim=0004.in']
    lst = [os.path.split(i) for i in lst]
    lst.sort()
    
    #for i, pc in enumerate(pcs):
    #    if os.path.exists('%d.txt' % pc):
    #        lst = lst[i*1200//len(pcs):(i+1)*1200//len(pcs)]
    #lst = lst[5*1200//len(pcs):(5+1)*1200//len(pcs)] + lst[6*1200//len(pcs):(6+1)*1200//len(pcs)][::-1]
    
    #run_oofem(lst[0])
    
    execute_pool(run_oofem, CPU_NUM, lst, {})
    
    
    
    
    