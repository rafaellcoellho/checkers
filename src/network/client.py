import socket
from network import logger


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self) -> bool:
        connection_info = (self.host, self.port)
        logger.info(f'Try connecting to server on {connection_info}')
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(connection_info)
            data_received = self.socket.recv(1024)
            message = data_received.decode('utf-8')
            if message == 'Success':
                logger.info(f'Connected to {self.socket.getpeername()}')
                return True
            else:
                logger.info(f'Connection refused: {message}')
                self.socket.close()
                self.socket = None
                return False
        except OSError as msg:
            logger.warning(msg)
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
        logger.info(f'Disconnected from {self.socket.getpeername()}')
        self.socket.close()
        self.socket = None
