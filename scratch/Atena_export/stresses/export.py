from numpy import genfromtxt, zeros, savetxt, equal, all
import matplotlib.pyplot as plt


#f_stress = open('stress.txt','r')
#f_princ_stress = open('principal_stress.txt','r')
#f_ref_coord = open('reference_ip_coordinates.txt','r')

def add_header(file, header):
    '''
        add header at beginning of the 'file'
    '''
    fin = open(file, 'r')
    temp = fin.readlines()
    fin.close()
    fout = open(file, 'w')
    fout.write(header)
    for lin in temp:
        fout.write(lin)
    fout.close

def row_num(filename):
    finput = open(filename, 'r')
    n_rows = len(finput.readlines())
    finput.close()
    return n_rows

stress = genfromtxt('stresses.txt', dtype='float', skip_header=13)
ref_coord = genfromtxt('nodal_coord.txt', dtype='float', skip_header=13)
print stress

ncol = 5

export = zeros(len(stress) * ncol)
export = export.reshape(len(stress), ncol)
export[:, 0] = ref_coord[:, 1]  # x coord
export[:, 1] = ref_coord[:, 2]  # y coord
export[:, 2] = stress[:, 1]  # sigma xx
export[:, 3] = stress[:, 2]  # sigma yy
export[:, 4] = stress[:, 3]  # sigma xy
savetxt('export.txt', export, fmt='%11.7f%11.7f%11.7f%11.7f%11.7f')
add_header('export.txt', '%11s%11s%11s%11s%11s\n' % ('x', 'y', 'sigma_xx', 'sigma_yy', 'sigma_xy'))

print export

# plot data for IP between x1 and x2 coordinate
x1 = 0
x2 = 1
mat1 = export[export[:, 0] > x1]
mat2 = export[export[:, 0] < x2]

# plot stress
#           y       max
plt.plot(mat2[:, 0], mat2[:, 1], 'r+')

#plt.plot( export[:, 5], export[:, 1], 'r+' )


plt.show()































