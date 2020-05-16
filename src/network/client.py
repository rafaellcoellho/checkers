import socket


class Client:
    def __init__(self, host, port):
        self.connection_info = (host, port)

    def connect_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.connection_info)
            s.sendall(b'Hello, world')
            data = s.recv(1024)

        print('Received', repr(data))
