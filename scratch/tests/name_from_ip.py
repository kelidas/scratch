import socket


for i in range(10, 90):
	try:
		print socket.gethostbyaddr("147.229.29.%i" % (i))
	except:
		print 'neni'

