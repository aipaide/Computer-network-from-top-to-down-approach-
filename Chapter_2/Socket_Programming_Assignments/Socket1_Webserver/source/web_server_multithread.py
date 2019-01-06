# import socket module
from socket import *
import _thread
import time

def Main():
    port=5222
    # 生成服务端socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # 绑定 socket地址(host,port)
    serverAddress=serverSocket.bind(("",port))
    print("starting up on  port {port}".format(port=port))
    # 监听端口，一次连接仅处理一次请求，不进行排队
    serverSocket.listen(1)
    print("listening on port {port}".format(port=port))
    while True:
        # socket捕获请求。对于捕获的请求，新建connectionSocket
        connectionSocket, addr =serverSocket.accept()
        threadIdentity=_thread.start_new_thread(threaded,(connectionSocket,))
        print("thread identity {threadIdentity}".format(threadIdentity=threadIdentity))

def threaded(connectionSocket):
    time.sleep(10)
    try:
        message = connectionSocket.recv(1024)
        # print("recieving message %s" % message)
        filename = message.split(b" ")[1]
        f = open(filename[1:])
        status_line="HTTP/1.1 200 OK\r\n"
        body=f.read()
        header_line="Content-Type: text/html\r\nContent-Length: %s\r\nConnection: close\r\n" % len(body)
        first =  (status_line+header_line+"\r\n")
        second=body
        connectionSocket.sendall(first.encode()+second.encode("utf-8"))
        # print("Response Message:\r\n %s" % first+second)
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        status_line="HTTP/1.1 404 Not Found\r\n"
        header_line=""
        body=""
        outputdata=status_line+header_line+"\r\n"+body
        # print("Response Message:\r\n %s" % outputdata)
        connectionSocket.sendall(outputdata.encode("utf-8"))
        connectionSocket.close()

if __name__=="__main__":
    Main()
