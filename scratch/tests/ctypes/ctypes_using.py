from ctypes import cdll, c_double, c_int, byref


pok = cdll.LoadLibrary( "Release/EasyDLL.dll" )

print pok.Multiply

a = c_double( 2.0 )
b = c_double( 2.0 )
#pok.Multiply.argtypes[c_double,c_double]
pok.Multiply.restype = c_double
print pok.Multiply( a, b )
#print pok.Multiply(byref(a),byref(b))

pok.Sum.restype = c_int
c = c_int( 2 )
d = c_int( 3 )
print pok.Sum( c, d )
#print pok.Sum(byref(c),byref(d))


pok.Multiply_p.restype = c_double

#pointer b
print pok.Multiply_p( a, byref( b ) )
#print pok.Multiply_p(a,b)
