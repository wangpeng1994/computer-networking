from socket import *

serverPort = 8000

serverSocket = socket(AF_INET, SOCK_STREAM) # 创建 IPv4 + TCP 欢迎套接字，面向所有客户
serverSocket.bind(('', serverPort))
serverSocket.listen(1) # 监听客户握手请求，请求连接最大数设置为了1
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept() # 接受和客户握手，创建连接套接字，仅用于当前监听到的某客户
    message = connectionSocket.recv(2048).decode()
    modifiedMessage = message.upper()
    connectionSocket.send(modifiedMessage.encode())
    connectionSocket.close() # 服务端先关闭了连接套接字
