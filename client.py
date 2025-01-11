import threading
import socket

host = "127.0.0.1"
port = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
count = 3
while data := client.recv(1024):
    response = input(data.decode('utf-8'))
    client.send(response.encode('utf-8'))
client.close()

    


