from socket import *

serverName = '104.194.87.72'
serverPort = 8000

# 创建套接字，AF_INET 指示底层网络使用 IPv4，SOCK_DGRAM 是一种 UDP 套接字类型
clientSocket = socket(AF_INET, SOCK_DGRAM)
# 提醒用户用键盘输入一行字符并赋值给 message
message = input('Input lowercase sentence: ')
# encode() 方法将字符串类型编码为字节类型，并附上目的地址，然后向套接字发送分组（源地址由操作系统自动附加到分组上，源端口也由操作系统自动分配）
clientSocket.sendto(message.encode(), (serverName, serverPort))
# 从套接字中接收服务器返回的数据，取缓存长度 2048，顺便得到服务器地址（尽管已知）
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
# 解码并打印
print(modifiedMessage.decode())
# 关闭套接字和进程
clientSocket.close()

