from numpy import genfromtxt, zeros, savetxt, equal, all
import matplotlib.pyplot as plt


#f_stress = open('stress.txt','r')
#f_princ_stress = open('principal_stress.txt','r')
#f_ref_coord = open('reference_ip_coordinates.txt','r')

def add_header( file, header ):
    '''
        add header at beginning of the 'file'
    '''
    fin = open( file, 'r' )
    temp = fin.readlines()
    fin.close()
    fout = open( file, 'w' )
    fout.write( header )
    for lin in temp:
        fout.write( lin )
    fout.close
    
def row_num( filename ):
    finput = open( filename, 'r' )
    n_rows = len( finput.readlines() ) 
    finput.close()
    return n_rows

stress = genfromtxt( 'stress.txt', dtype='float', skip_header=13, skip_footer=3, delimiter=[5, 6, 6, 11, 11, 11] )
princ_stress = genfromtxt( 'principal_stress.txt', dtype='float', skip_header=13, skip_footer=3, delimiter=[5, 6, 6, 11, 11, 11, 11, 11, 11] )
ref_coord = genfromtxt( 'reference_ip_coordinates.txt', dtype='float', skip_header=13, skip_footer=3, delimiter=[5, 6, 6, 11, 11] )

ncol = 7
if row_num( 'stress.txt' ) == row_num( 'principal_stress.txt' ) == row_num( 'reference_ip_coordinates.txt' ):
    if all( equal( stress[:, 0], princ_stress[:, 0] ) ) and all( equal( stress[:, 0], ref_coord[:, 0] ) ) and all( equal( princ_stress[:, 0], ref_coord[:, 0] ) ) \
        and all( equal( stress[:, 1], princ_stress[:, 1] ) ) and all( equal( stress[:, 1], ref_coord[:, 1] ) ) and all( equal( princ_stress[:, 1], ref_coord[:, 1] ) )  \
        and all( equal( stress[:, 2], princ_stress[:, 2] ) ) and all( equal( stress[:, 2], ref_coord[:, 2] ) ) and all( equal( princ_stress[:, 2], ref_coord[:, 2] ) ) :
        # check if first three columns of all arrays are equal
        export = zeros( len( stress ) * ncol )
        export = export.reshape( len( stress ), ncol )
        export[:, 0] = ref_coord[:, 3] # x coord
        export[:, 1] = ref_coord[:, 4] # y coord
        export[:, 2] = stress[:, 3] # sigma xx
        export[:, 3] = stress[:, 4] # sigma yy
        export[:, 4] = stress[:, 5] # sigma xy
        export[:, 5] = princ_stress[:, 3] # max
        export[:, 6] = princ_stress[:, 4] # min
        savetxt( 'export.txt', export, fmt='%11.7f%11.7f%11.7f%11.7f%11.7f%11.7f%11.7f' )
        add_header( 'export.txt', '%11s%11s%11s%11s%11s%11s%11s\n' % ( 'x', 'y', 'sigma_xx', 'sigma_yy', 'sigma_xy', 'max', 'min' ) )
    
    else:
        print 'The first three columns are not equal -- length or order is different'
        print 'Call hot line 123 456 789 :-)'
else:
    print 'The files are not equal'
    print 'stress.txt has %i rows' % row_num( 'stress.txt' )
    print 'principal_stress.txt has %i rows' % row_num( 'principal_stress.txt' )
    print 'reference_ip_coordinates.txt has %i rows' % row_num( 'reference_ip_coordinates.txt' )

# plot data for IP between x1 and x2 coordinate
x1 = 0.001
x2 = 0.002
mat1 = export[export[:, 0] > x1]
mat2 = export[export[:, 0] < x2]

# plot stress
#           y       max
plt.plot( mat2[:, 5], mat2[:, 1], 'r+' )

#plt.plot( export[:, 5], export[:, 1], 'r+' )


plt.show()































