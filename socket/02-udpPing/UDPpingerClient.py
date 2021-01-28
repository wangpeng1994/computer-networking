'''
1. 使用UDP发送ping消息（注意：不同于TCP，您不需要首先建立连接，因为UDP是无连接协议。）
2. 从服务器输出响应消息
3. 如果从服务器受到响应，则计算并输出每个数据包的往返时延（RTT）（以秒为单位），
4. 否则输出“请求超时”
'''
from socket import *
from datetime import datetime

serverName = 'localhost'
serverPort = 12000
sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(1)  # 设置超时值为1秒

for i in range(1, 10):
    startTime = datetime.now()
    pingText = 'Ping ' + str(i) + ' ' + startTime.strftime('%Y-%m-%d %H:%M:%S')
    print(pingText)
    sock.sendto(pingText.encode(), (serverName, serverPort))
    try:
        res, serverAddress = sock.recvfrom(1024)
        timedelta = datetime.now() - startTime
        print(res.decode() + ' RTT=' + str(timedelta.microseconds / 1000) + 'ms')
    except timeout as err:
        print(err)

sock.close()
