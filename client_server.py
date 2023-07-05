import json
import threading
from socket import socket, AF_INET, SOCK_STREAM


class ClientServer():
    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect(('82.157.234.31', 7778))
        self.InitClient()
        self.recieve = threading.Thread(target=self.recv_)
        self.recieve.daemon = True
        self.recieve.start()
        self.is_draw = False
        self.lock = threading.Lock()

    def InitClient(self):
        self.getUserName()
        dict = {'user_name': self.user_name, 'state': 'login', 'message': '', 'time':''}
        json_dict = json.dumps(dict)
        self.client.send(json_dict.encode('utf-8'))
        print(self.client.recv(1024).decode())

    def getUserName(self):
        try:
            with open('./user_info.json', 'r') as f:
                user_name = json.load(f)
                self.user_name = user_name['user_name']
        except:
            with open('./user_info.json', 'w') as f:
                dict = {'user_name': '这是默认用户名，你一定会想改的'}
                self.user_name = dict['user_name']
                json.dump(dict, f)

        return self.user_name


    def recv_(self):
        while True:
            data = self.client.recv(1024).decode()
            self.lock.acquire()
            try:
                self.is_draw = True
                data = json.loads(data)
                #print(data, type(data))
                #存储接收到的数据存入json文件中
                self.writeToJson(data)
            finally:
                self.lock.release()

    def writeToJson(self, data):
        content = []
        try:
            with open('./messages.json', 'r') as f:
                load_dict = json.load(f)
                for i in range(len(load_dict)):
                    sender_name = load_dict[i]['sender_name']
                    message = load_dict[i]['message']
                    time = load_dict[i]['time']
                    dict = {'sender_name': sender_name, 'message': message, 'time': time}
                    content.append(dict)

        except:
            with open('./messages.json', 'w') as f:
                json.dump(content, f, indent=4)

        content.append(data)

        with open('./messages.json', 'w') as f:
            json.dump(content, f, indent=4)
