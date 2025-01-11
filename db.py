import json
class Chat:
    def __init__(self,load=False, **kwargs):
        """
        Expect user1, user2 as strings or load from an existing source
        """
        if not load:
            user1, user2 = kwargs
            self.id = hash(user1) + hash(user2)
            self.users = {
                user1: 1, user2: 2
            }
            self.messages = []
        else:
            self.id = load['id']
            self.users = load['users']
            self.messages = load.get('messages', [])

    def to_dict(self):
        return {
            'id': self.id,
            'users': self.users,
            'messages': [msg.to_dict() for msg in self.messages]

        }
        
    def send_message(self, sender, message):
        msg = Message(self.users.get(sender), message)
        self.messages.append(msg)

    def show_history(self, sender, conn):
        for msg in self.messages:
            conn.send(msg.to_dict())

class Database:
    def __init__(self):
        self.users = {}
        self.chats = {}

    def validate_user(self, username):
        return username in self.users
    
    def create_user(self, conn):
        conn.send("Enter your username: ".encode('utf-8'))
        username = conn.recv(1024).decode('utf-8')
        conn.send("Enter your name: ".encode('utf-8'))
        name = conn.recv(1024).decode('utf-8')
        if self.validate_user(username):
            conn.send("User already exists, please retry again\n".encode('utf-8'))
            conn.send("Do you want to log in?: [Y/N] ".encode('utf-8'))
            login = conn.recv(1024).decode('utf-8')
            if login == 'Y':
                return self.login(conn)
            else:
                self.create_user(conn)
        
        self.users[username] = {
            'username': username,
            'name': name
        }
        self.save()
        return User(load=self.users[username])

    def login(self, conn):
        conn.send("Enter your username".encode('utf-8'))
        username = conn.recv(1024).decode('utf-8')
        return self.find_user(username)

    def create_chat(self, sender, conn):
        conn.send('Enter the username of the person whom you want to chat with'.encode('utf-8'))
        receiver = conn.recv(1024).decode('utf-8')
        if receiver not in self.users:
            conn.send("Please enter a valid username".encode('utf-8'))
            return
        if self.find_chat(hash(sender.username) + hash(receiver)):
            conn.send("Chat already exists".encode('utf-8'))
        else:
            chat = Chat(user1 = sender, user2 = receiver)
            self.chats.append(chat.to_dict())
        
    def find_chat(self, id):
        if id not in self.chats:
            return False
        chat = self.chats.get(id)
        return Chat(load=chat)
    def find_user(self, username):
        if username not in self.users:
            return False
        return User(load=self.users[username])
    
    def save(self):
        user_path = 'user_db.json'
        chat_path = 'chat_db.json'
        with open(user_path, 'w') as f:
            f.write(json.dumps(self.users))
        with open(chat_path, 'w') as f:
            f.write(json.dumps(self.chats))

    def load(self):
        try:
            with open('user_db.json', 'r') as f:
                self.users = json.loads(f.read())
            with open('chat_db.json', 'r') as f:
                self.chats = json.loads(f.read())
        except:
            print("problem with reading file")
           

class User:
    def __init__(self,load=False, **kwargs):
        """
        takes in name and username as keyword arguments, if user exists,use load
        """
        if not load:
            name, username = kwargs
            self.name = name
            self.username = username
        else:
            self.name = load['name']
            self.username = load['username']

    def open_chat(self, username, database):
        
        pass

    def send_message(self, username, message, database: Database, conn):
        chat = database.find_chat(hash(self.username) + hash(username))
        if chat:
            chat.send_message(self.username, message)
            conn.sendd("Successfully created chat")
        else:
            database.create_chat(self.username)
            conn.sendd("Could not create chat")
            self.send_message(username, message, database)
    

        
class Message:
    def __init__(self, user_no, message):
        self.id = user_no
        self.message = message

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message
        }
