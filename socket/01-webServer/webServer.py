# import socket module
import time
from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
serverPort = 80
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print(addr)
    try:
        message = connectionSocket.recv(1024).decode()
        # GET /somedir/page.html HTTP/1.1
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()
        # Send one HTTP header line into socket
        outputdata = 'HTTP/1.1 200 ok\r\n' + 'Content-Type: text/html\r\n\r\n' + outputdata
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        # 认为增加5秒执行延迟，在两个页面中（几乎）同时刷新发出请求，
        # 会发现第一个页面大概需要5秒，而第二个页面大概需要10秒，
        # 这说明现在这个服务器，一次只能处理一个HTTP请求，
        # 尽管 socket.accpet() 能接受多个TCP连接，但现在被内部处理速度（需要5秒）阻塞了，
        # 因此每次处理HTTP请求时，都开辟新的线程进行处理，从而不影响 socket.accpet() 继续和别的客户端进行连接。
        time.sleep(5)
        connectionSocket.close()
        print('ok!')
    except IOError:
        # Send response message for file not found
        outputdata = 'HTTP/1.1 404 Not Found\r\n\r\n'
        connectionSocket.send(outputdata.encode())
        # Close client socket
        connectionSocket.close()

serverSocket.close()
