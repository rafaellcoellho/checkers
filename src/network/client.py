import selectors
import socket
import threading
from queue import Queue

from network import logger


class GameClient:
    def __init__(self, host: str, port: int, receive_queue: Queue):
        self.receive_queue = receive_queue

        self.connection_information = (host, port)
        self.socket_selector = selectors.DefaultSelector()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connected = False

    def connect(self):
        logger.info(f'Try connecting to server on {self.connection_information}')
        try:
            self.client_socket.connect(self.connection_information)
            data_received = self.client_socket.recv(1024)
            self.client_socket.setblocking(False)
            message = data_received.decode('utf-8')

            if message == 'Success':
                logger.info(f'Connected to {self.connection_information}')
                self.connected = True
            else:
                logger.info(f'Connection refused: {message}')

                self.client_socket.close()
                self.client_socket = None

                self.connected = False
        except OSError as msg:
            logger.warning(msg)

            self.client_socket.close()
            self.client_socket = None

            self.connected = False

        if self.connected:
            self.socket_selector.register(
                self.client_socket, selectors.EVENT_READ, data=self.receive_handler
            )

        return self.connected

    def receive_handler(self, file_obj_socket):
        data = file_obj_socket.recv(9)
        if data:
            self.data_received(file_obj_socket, data)
        else:
            logger.info(f"Lost connection from {file_obj_socket.getpeername()}")
            self.socket_selector.unregister(file_obj_socket)

            file_obj_socket.close()

    def data_received(self, file_obj_socket, data):
        message = data.decode("utf-8")
        logger.info(f"Received from {file_obj_socket.getpeername()}: {message}")

        # put in the queue
        self.receive_queue.put(message)

    def send_to_server(self, msg: str) -> None:
        data: bytes = str.encode(msg)
        self.client_socket.send(data)

    def main_loop(self):
        try:
            while True:
                events = self.socket_selector.select()
                for key, _ in events:
                    callback = key.data
                    callback(key.fileobj)
        except KeyboardInterrupt:
            logger.info("Closing server")

        self.client_socket.close()
        self.socket_selector.close()

    def disconnect(self):
        logger.info(f'Disconnected from {self.client_socket.getpeername()}')
        self.client_socket.close()
        self.client_socket = None


class Client:
    def __init__(self, host: str, port: int, receive_queue: Queue) -> None:
        self.game_client_instance = GameClient(host, port, receive_queue)

    def connect(self):
        return self.game_client_instance.connect()

    def listen(self) -> None:
        client_daemon_thread = threading.Thread(
            target=self.game_client_instance.main_loop, daemon=True
        )
        client_daemon_thread.start()

    def send_to_server(self, msg: str):
        self.game_client_instance.send_to_server(msg)

    def disconnect(self):
        self.game_client_instance.disconnect()
