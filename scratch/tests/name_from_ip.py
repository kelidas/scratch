import socket


count = 0
for i in range(120, 125):

	try:
		print socket.gethostbyaddr("147.229.29.%i" % (i))
	except:
		print 'neni'
		count += 1

print count

