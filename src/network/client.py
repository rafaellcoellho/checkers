import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        connection_info = (self.host, self.port)
        self.socket.connect(connection_info)

    def send_to_server(self, data: str):
        data_in_bytes = str.encode(data)
        self.socket.send(data_in_bytes)