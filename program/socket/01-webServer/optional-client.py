#!/usr/bin/env python3

import sys
from socket import *

print(sys.argv)
argv = sys.argv
serverName = argv[1]
serverPort = argv[2]
filename = argv[3]

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, int(serverPort)))

reqContent = 'GET ' + filename + ' HTTP/1.1\r\n' + 'Host: ' + serverName + ':' + serverPort + '\r\n'
print(reqContent)
clientSocket.send(reqContent.encode())

data = 1
while data:
    data = clientSocket.recv(1024)
    print(data.decode(), end='')

clientSocket.close()

