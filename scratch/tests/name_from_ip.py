import socket


count = 0
for i in range(1, 128):
    ip = '147.229.29.%d' % (i)
    try:
        print(socket.gethostbyaddr(ip))
    except:
        print('neni', ip)
        count += 1

print(count)
