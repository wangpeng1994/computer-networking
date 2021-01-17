# import socket module
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
        connectionSocket.close()
        print('ok!')
    except IOError:
        # Send response message for file not found
        outputdata = 'HTTP/1.1 404 Not Found\r\n\r\n'
        connectionSocket.send(outputdata.encode())
        # Close client socket
        connectionSocket.close()

serverSocket.close()
