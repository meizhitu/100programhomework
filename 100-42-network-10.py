#coding=utf-8

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('whois.networksolutions.com', 43))
s.send('google.com \r\n')
while 1:
    v = s.recv(1024)
    if v == '' or v == None:
        break
    print v
s.close()
pass