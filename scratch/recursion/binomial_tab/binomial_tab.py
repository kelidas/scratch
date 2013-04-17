
import numpy as np
import mpmath as mp
import os

mp.mp.dps = 1000

MDIR = os.path.dirname(__file__)


def get_binom_tab(n=1000, binom_tab_name=r'binom_tab.npy'):
    '''
    Prepare table of binomial coefficients including signs (-1)**(k+1) and strore
    it in .npy file.
    '''
    def binom_tab_gen():
        binom_tab = np.zeros((n, n), dtype=object)
        print 'binom_tab preparation/recalculation'
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                binom_tab[i - 1, j - 1] = mp.binomial(i, j) * (-1) ** (j + 1)
        np.save(os.path.join(MDIR, binom_tab_name))
        return binom_tab
    if os.path.exists(os.path.join(MDIR, binom_tab_name)):
        binom_tab = np.load(os.path.join(MDIR, binom_tab_name))
        if binom_tab.shape[0] < n:
            binom_tab = binom_tab_gen()
    else:
        binom_tab = binom_tab_gen()
    return binom_tab

if __name__ == '__main__':
    binom_tab = get_binom_tab(n=1000, binom_tab_name=r'binom_tab.npy')
