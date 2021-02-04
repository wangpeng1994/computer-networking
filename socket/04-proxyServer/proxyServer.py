from socket import *
import sys
import os

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_port"\n[server_port : It is the port Of Proxy Server]')
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerPort = int(sys.argv[1])
tcpSerSock.bind(('', tcpSerPort))
tcpSerSock.listen(10)
# Strat receiving data from the client
print('Ready to serve on port %s...' % tcpSerPort)
while 1:
    tcpCliSock, addr = tcpSerSock.accept()
    print('\nReceived a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()
    # print('message:\n', message)
    # Extract the filename from the given message
    # print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    # print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print('filetouse: ', filetouse)
    try:
        # Check weather the file exist in the cache
        f = open('web_cache/' + filetouse[1:], "rb")
        outputdata = f.read()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send('HTTP/1.1 200 OK\r\n'.encode())
        tcpCliSock.send('Content-Type:text/html\r\n\r\n'.encode())
        tcpCliSock.send(outputdata)
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            # print('hostn: ', hostn)
            try:
                # Connect to the socket to port 80. 连接到原始服务器
                serverName = hostn.partition('/')[0]
                serverPort = 80
                c.connect((serverName, serverPort))
                askFile = ''.join(filename.partition('/')[1:])
                print('askFile: ', askFile)
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                # 可进一步判断扩展出支持转发POST请求（略）
                requestLine = 'GET %s HTTP/1.1\r\nHost: %s\r\n\r\n' % (askFile, serverName)
                fileobj.write(requestLine.encode())
                print('requestLine: ', requestLine)
                # Read the response into buffer
                response = fileobj.read()
                reponseBody = response.split(b'\r\n\r\n')[1]
                print('response:\n', response)
                print('reponseBody:\n', reponseBody)
                if response.split()[1] == b'404':
                    print('404')
                    tcpCliSock.send(response)
                    # tcpCliSock.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                    tcpCliSock.close()
                    continue
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                filename = "web_cache/" + filename
                # 遍历路径创建不存在的文件夹
                filesplit = filename.split('/')
                for i in range(0, len(filesplit) - 1):
                    if not os.path.exists("/".join(filesplit[0:i + 1])):
                        os.makedirs("/".join(filesplit[0:i + 1]))
                tmpFile = open(filename, "wb")
                tmpFile.write(reponseBody)
                tmpFile.close()
                tcpCliSock.send(response)  # 直接转发原始服务器的响应
            except IOError as err:
                print("Illegal request", err)
            c.close()
        else:
            # HTTP response message for file not found
            print("NET ERROR")
    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()
