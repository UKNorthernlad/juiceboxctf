#!/usr/bin/python

import socket,re,time
HOST = '203.0.113.223'


PORT = 10001


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
data = s.recv(1024)
temp = data.split("\n")
s.send(temp[1])
data=s.recv(1024)
print data
