import socket

host = socket.gethostname()
port = 8081

client = socket.socket()
client.connect((host, port))


while True:
    user_input = input(">>>")
    client.send(user_input.encode())
    data = client.recv(1024).decode()

    if not data:
        break

    print(f"<<<from Tania {data}")

client.close()
