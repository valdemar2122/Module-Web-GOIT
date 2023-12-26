import socket

host = socket.gethostname()
port = 8081

server = socket.socket()
server.bind((host, port))

server.listen(1)

connection, address = server.accept()
print(connection)
while True:
    data = connection.recv(1024).decode()
    print(f"<<<from vova: {data}")

    user_input = input(">>>")
    connection.send(user_input.encode())

connection.close()
