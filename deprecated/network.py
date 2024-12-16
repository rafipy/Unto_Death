import socket
import pickle #used to send game objects / serialize objects!


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.16.100.80"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p


    def wait(self):

        try:
            self.client.connect(self.addr)
            waiting = self.client.recv(2048).decode()

            if waiting == "Connected!":
                return [waiting, False]
            else:
                return [waiting, True]

        except:
            pass

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048)) #loads byte data to client
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data)) #dump data as an object to send as byte data
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)