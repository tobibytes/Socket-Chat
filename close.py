import socket
addys = [('127.0.0.1', 5000), ('127.0.0.1', 5001), ('127.0.0.1', 5002)]
for host, port in addys:
    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server1.connect((host, port))
    server1.close()

# import json

# with open('user_db.json', 'r') as f:
#     data = json.loads(f.read())
#     print(data)
#     print(data['tobi'])