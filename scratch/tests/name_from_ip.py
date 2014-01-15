import socket


for i in range(0, 90):
	try:
		print socket.gethostbyaddr("147.229.29.%i" % (i))
	except:
		print 'neni'

