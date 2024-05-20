import socket

# 创建一个新的socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定到指定的IP和端口
server_socket.bind(("127.0.0.1", 23010))

# 开始监听连接
server_socket.listen()

print("Server is running on port 23010...")

while True:
    # 接受一个新的连接
    client_socket, client_address = server_socket.accept()
    print("Accepted connection from", client_address)

    while True:
        # 接收数据
        data = client_socket.recv(1024)  # 接收最多1024字节的数据
        if not data:
            break  # 如果没有接收到数据，结束内部循环
        print("Received data:", data.decode())  # 打印接收到的数据

    # 处理连接...