import socket
import threading

from db import Database

database = Database()
database.load()

def handle_conn(conn: socket.socket, addr):
    while True:
            database.create_user(conn)
            database.create_chat('tobi',conn)
            break
            


def main():
    host = "0.0.0.0"
    port = 5001
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    while True:
        try:
            conn, addr = server.accept()
            print(addr, conn)
            t1 = threading.Thread(target=handle_conn, args=(conn, addr))
            t1.start()
        except:
            print('error, rerun the program')
            server.close()
            break
        server.close()
main()
        
