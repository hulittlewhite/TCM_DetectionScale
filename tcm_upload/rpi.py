import socket
HOST = '192.168.43.91'        # 连接本地服务器
PORT = 8001               # 设置端口号
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # 选择IPv4地址以及TCP协议
sock.bind((HOST, PORT))          # 绑定端口
sock.listen(5)                   # 监听这个端口，可连接最多5个设备

while True:
    connection, address = sock.accept()              # 接受客户端的连接请求
    Building_connection = connection.recv(1024)                      # 接收数据实例化
    if Building_connection == b"request":
        print("connection is ok!")
        connection.send(b'welcome to server!')       # 服务器已经连接

    while Building_connection == b"request":
        a = connection.recv(1024)                               # 循环，持续通讯接收数据
        if a == b"exit":
            connection.send(b"close")
            break
        if a != b"request"and a:
            print("接收端:")
            print((a).decode())
            print("服务端：")
            # se=input()
            # connection.send((se).encode("utf-8"))
            # print("")

    break
connection.close()
print("连接关闭")
