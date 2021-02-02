'''
1. 可进一步实现 qq 或 163 等邮件服务器的登录认证流程
2. 支持 TLS/SSL
3. 参考：
    python关于SSL/TLS认证的实现 https://blog.csdn.net/vip97yigang/article/details/84721027
    https://docs.python.org/3/library/ssl.html#ssl.SSLContext.wrap_socket
'''

from socket import *
import base64
import ssl

# 邮件报文可以按格式补充的更丰富一些，就像HTTP的一些首部行一样
# From: alice@crepes\r\n
# To bob@hamburger.edu\r\n
# Subject: Searching for the meaning of life.\r\n
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.qq.com'
# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
sock = socket(AF_INET, SOCK_STREAM)

# 可选，为 tcp socket 添加 TLS/SSL 支持
context = ssl.create_default_context()
clientSocket = context.wrap_socket(sock, server_side=False):

clientSocket.connect(mailserver, 25)
#Fill in end
recv = clientSocket.recv(1024)
print recv
if recv[:3] != '220':
    print '220 reply not received from server.'

# Send HELO command and print server response.
heloCommand = 'HELO QQ mail\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '250':
    print '250 reply not received from server.'


'''
实际中，如 qq、163等邮箱是需要先到账户设置里开启stmp服务，并在HELO之后进行登录
loginCommand = 'auth login\r\n'
userCommand = base64.b64encode(mailUser.encode()) + b'\r\n' # 947034046
passCommand = base64.b64encode(mailPassWord.encode()) + b'\r\n' # 授权码
'''

# Send MAIL FROM command and print server response.
# Fill in start
clientSocket.send('MAIL FROM: <947034046@qq.com>\r\n')
recv2 = clientSocket.recv(1024)
print recv2
if recv2[:3] != '250':
    print '250 reply not received from server.'
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
clientSocket.send('RCPT TO: <390369782@qq.com>\r\n')
recv3 = clientSocket.recv(1024)
print recv3
if recv3[:3] != '250':
    print '250 reply not received from server.'
# Fill in end

# Send DATA command and print server response.
# Fill in start
clientSocket.send('DATA\r\n')
recv4 = clientSocket.recv(1024)
print recv4
if recv4[:3] != '354':
    print '354 reply not received from server.'
# Fill in end

# 应用层握手之后，开始发送邮件报文
# Send message data.
# Fill in start
clientSocket.send(msg)
# Fill in end

# Message ends with a single period.
# Fill in start
clientSocket.send(endmsg)
# Fill in end

# Send QUIT command and get server response.
# Fill in start
clientSocket.send('QUIT\r\n')
recv4 = clientSocket.recv(1024)
print recv4
if recv4[:3] != '221':
    print '221 reply not received from server.'
# Fill in end
