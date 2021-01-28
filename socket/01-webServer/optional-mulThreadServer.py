#!/usr/bin/env python3

# import socket module
import threading
import time
from socket import *

# 每个连接都必须创建新线程（或进程）来处理，否则，单线程在处理连接的过程中，无法接受其他客户端的连接
def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    try:
        message = sock.recv(1024).decode()
        # GET /somedir/page.html HTTP/1.1
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()
        # Send one HTTP header line into socket
        outputdata = 'HTTP/1.1 200 ok\r\n' + 'Content-Type: text/html\r\n\r\n' + outputdata
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            sock.send(outputdata[i].encode())
        sock.close()
        print('ok!')
    except IOError:
        # Send response message for file not found
        outputdata = 'HTTP/1.1 404 Not Found\r\n\r\n'
        sock.send(outputdata.encode())
        # Close client socket
        sock.close()

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
serverPort = 80
serverSocket.bind(('', serverPort))
# 指定等待连接的最大数量
serverSocket.listen(5)

while True:
    # Establish the connection
    print('Ready to serve...')
    # 接受一个新连接
    connectionSocket, addr = serverSocket.accept()
    # 创建新线程来处理TCP连接
    t = threading.Thread(target=tcplink, args=(connectionSocket, addr))
    t.start()

serverSocket.close()
