import os
import sys
import subprocess
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import time
import platform
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock

def run_test(nsim=1000, nvar=9, nrun=4, ntrials=10000, seedType=0, plotErrors=1, plotSamples=1, plotFreqs=0, typenorm=0, typetun=2, typSample=1, maxTeplota=40, minTeplota=1e-10, initNum=1, finalNum=1, acceptLevelForPrint=0):
    '''
1/ nsim
2/ nvar
3/ nrun     -- pocet zopakovani problemu o rozmeru Nvar x Nsim
4/ ntrials
5/ seedType
6/ plotErrors
7/ plotSamples
8/ plotFreqs
9/ typenorm
10/ typetun
11/ TypSample
12/ maxTeplota
13/ minTeplota
14/ Pocateni pocet soucasnych zamen paru
15/ Koncovy pocet soucasnych zamen paru
16/ AcceptLevelForPrint -- Hodnota chyby, ktera, pokud dosazena a podkrocena, vyvola tisk navrhu (pro TotalCombin)


Ad 4/ ntrials
Pocet obratek (nahodnych zamen) na shodne teplote v priapde simulovaneho zihani (metoda 2 v bode 9)


Ad 5/ seedType
pokud je nulovy, pouzije se Mersene Twister k tomu, aby vygeneroval seed pro generator ve freetu. mela by byt zajistena "dokonala randomizizace"


Ad 6/ plotErrors
0[1] bude [nebude] se tisknout soubor chyb. 
Format: Prvni sloupec je nsim, druhy sloupec maximalni koreladce v pripade korelacniho kriteria, nebo 1/Lmin^2  - pripspevek do normy odpovidajici minimalni vzdalenosti mezi dvema body v pripade AE. Do souboru s existujucim nazvem se dopisuje.

 
Ad 7/ plotSamples
0[1] bude [nebude] se tisknout soubor s vygenerovanymi vzorky (rovnomerne rozdelenymi na intervalu (0,1). Do souboru se dopisuje, jednotlive runs jsou oddelny dvema radky.


Ad 8/ plotFreqs
0[1] bude [ne0bude] se tisknout soubor s frekvenecemi (vyuziva honza elias pro hodnoceni rovnomernosti pokryti)


Ad 9/ typenorm
Norma, ktera se pouziva k optimalizaci 
0...rms korel, 
4...AE
5...PAE
6...MaxiMin
7...pMaxiMin
8...CL2 diskrepance


Ad 10/ typetun
Metoda zamichani
0...TotalKombin, 1...randomSwitch (prijima pouze zlepseni), 2...SA klasik, 3...RandMixSwitch (jedno nahodne pretrideni)



Ad 11/ TypSample
   [0=LHSmean, 1=LHSmedian, 2=LHS-Random, 3=MC]"


Ad 12/ maxTeplota
Max teplota, ktera se pouzije v pripade metody "2" v bode 10. 
 - Pro korelaci (0 v bode 9) lze ponechat 0 (automaticky vyber), nebo nastavit na Nvar*Nvar/2, coz je velka hodnota. Pro 
 - pro AE (4 v bode 9) nastavit na 1.2e-8


Ad 13/ minTeplota
Max teplota, ktera se pouzije v pripade metody "2" v bode 10. 
 - Pro korelaci (0 v bode 9) je treba dat na hodnotu ocekavane chyby korelace. Treba: Nvar/Nsim^(5/2)
 - pro AE (4 v bode 9) nastavit na 1.0e-8 (pak se provede  pouze sady Nstrials na dvou urovnich teplot)
    '''
    start = sysclock()
    with open(os.devnull, 'w') as f:
        p = subprocess.Popen('wine SimulationTests.exe %d %d %d %d %d %d %d %d %d %d %g %g %d %d %d %d' % (nsim, nvar, nrun, ntrials, seedType, plotErrors, plotSamples, plotFreqs, typenorm, typetun, maxTeplota, minTeplota, typSample, initNum, finalNum, acceptLevelForPrint), shell=True, stdout=f)
    p.communicate()
    t = sysclock() - start
    namepart = '%04dvar_%04dsim_%04druns_00seed.txt' % (nvar, nsim, nrun)
    errors = np.loadtxt('Samples/Errors_%s' % namepart)
    col2 = errors[:, 1]
    error = errors[:, 2]
    seed = errors[:, 3]

    os.remove('Samples/Errors_%s' % namepart)
    os.remove('Samples/Samples_%04dvar_%04dsim.txt' % (nvar, nsim))
    print '#' * 50
    print 'nsim, nvar, nrun, ntrials =', nsim, nvar, nrun, ntrials
    print 'Error (mean, std, cov) =', np.mean(error), np.std(error), np.std(error) / np.mean(error)
    print 'maxTeplota =', maxTeplota
    print 'minTeplota =', minTeplota
    print 'col2 (mean, std, cov)', np.mean(col2), np.std(col2), np.std(col2) / np.mean(col2)
    print 'seed unique?', np.unique(seed).shape == seed.shape
    print 'runtime =', t

    # with open('test_results.txt', 'a') as f:
    #    f.write('%d\t%d\t%d\t%d\t%g\t%g\t%g\t%g\t%g\t%g\t%g\t%g\t%d\t%f\n' %
    return (nsim, nvar, nrun, ntrials, maxTeplota, minTeplota,
                      np.mean(error), np.std(error), np.std(error) / np.mean(error),
                      np.mean(col2), np.std(col2), np.std(col2) / np.mean(col2),
                      np.unique(seed).shape == seed.shape,
                      t)

def output_write(tup):
    print tup
    print type(tup)
    with open('stats.txt', 'a') as f:
        f.write('%d\t%d\t%d\t%d\t%g\t%g\t%g\t%g\t%g\t%g\t%g\t%g\t%d\t%f\n' % tup)



if __name__ == '__main__':
    nsim = [2, 4, 6, 8, 10, 12, 16, 24, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    nvar = [2, 3, 5, 9]
    nrun = 5
    ntrials = [100, 500, 1000, 3000, 5000, 10000, 15000, 20000, 25000, 30000, 40000]
    seedType = 0
    plotErrors = 1
    plotSamples = 1
    plotFreqs = 0
    typenorm = 5
    typetun = 2
    typSample=1
    initNum = 1
    finalNum = 1
    acceptLevelForPrint = 0
    # if typenorm==0:
    #    maxTeplota = nvar * nvar * 0.5
    #    minTeplota = nvar / nsim ** 2.5
    # else:
    #    maxTeplota = 1.2e-8
    #    minTeplota = 1.0e-8

    import itertools as it
    args = list(it.product(ntrials, nvar, nsim))
    # for trials,var,sim in args:
    def run(trials, var, sim):
        n = np.log10(sim)
        if typenorm in [6,7]:
            maxTeplota = 50  # var * var * 0.5
            minTeplota = 1.0e-12  # var / sim ** 2.5
        elif typenorm in [4,5]:
            maxTeplota = - 2. / 7. * (n-2) + 2
            minTeplota = - 2 - n
        else:
            raise('Not implemented typenorm')
        return run_test(nsim=sim, nvar=var, nrun=nrun, ntrials=trials, seedType=seedType, plotErrors=plotErrors, plotSamples=plotSamples, plotFreqs=plotFreqs, typenorm=typenorm, typetun=typetun, maxTeplota=maxTeplota, minTeplota=minTeplota, typSample=typSample, initNum=initNum, finalNum=finalNum, acceptLevelForPrint=acceptLevelForPrint)
    pool = mp.Pool(15)  # mp.cpu_count())
    #for arg in args:
    #    pool.apply_async(run, args=arg, callback=output_write)

    results = [pool.apply_async(run, args=arg, callback=output_write) for arg in args]
    while results:
        try:
            result = results.pop(0)
            result.get(timeout=5000)
        except mp.TimeoutError as e:
            print 'timeout'
            for i in reversed(range(len(pool._pool))):
                p = pool._pool[i]
                if p.exitcode is None:
                    p.terminate()
                del pool._pool[i]

    pool.close()
    pool.join()
    print 'Finished!'
