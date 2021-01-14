from socket import *

serverName = 'localhost'
serverPort = 8000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort)) # TCP三次握手

message = input('Input lowercase sentence: ')
clientSocket.send(message.encode())

modifiedMessage = clientSocket.recv(2048)
print('From Server: ', modifiedMessage.decode())

clientSocket.close() #客户端后关闭了连接套接字

