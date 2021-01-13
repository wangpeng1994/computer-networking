from socket import *

serverPort = 8000

serverSocket = socket(AF_INET, SOCK_DGRAM)
# 显示地为该套接字分配端口号
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
while True:
    # 这里 clientAddress 中的端口号由客户端操作系统自动分配
    message, clientAddress = serverSocket.recvfrom(2048)
    print('Received message:\n', message.decode())
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
