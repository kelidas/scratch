import socket



for i in range(100, 126):

	try:
		print socket.gethostbyaddr("147.229.29.%i" % (i))
	except:
		print 'neni'

