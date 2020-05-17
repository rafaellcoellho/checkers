import socket


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self) -> bool:
        connection_info = (self.host, self.port)
        print('Try connecting to server...')
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(connection_info)
            data_received = self.socket.recv(1024)
            message = data_received.decode('utf-8')
            if message == 'Success':
                print(f'Connected to {self.socket.getpeername()}')
                return True
            else:
                print(f'Connection refused: {message}')
                self.socket.close()
                self.socket = None
                return False
        except OSError as msg:
            print(msg)
            self.socket.close()
            self.socket = None
            return False

    def send_to_server(self, data: str) -> None:
        data_in_bytes = str.encode(data)
        self.socket.send(data_in_bytes)

    def receive_from_server(self) -> str:
        data_received = self.socket.recv(1024)
        msg = data_received.decode('utf-8')
        return msg

    def disconnect(self):
        print(f'Disconnected from {self.socket.getpeername()}')
        self.socket.close()
        self.socket = None
