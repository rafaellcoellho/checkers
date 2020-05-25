import selectors
import socket
import threading

from network import logger


class GameServer:
    def __init__(self, host: str, port: int) -> None:
        self.players = []

        self.connection_information = (host, port)
        self.socket_selector = selectors.DefaultSelector()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setblocking(False)
        self.server_socket.bind(self.connection_information)
        self.server_socket.listen(2)

        self.socket_selector.register(
            self.server_socket, selectors.EVENT_READ, data=self.accept_handler
        )

        logger.info(f"Serving on {self.connection_information}")

    def accept_handler(self, file_obj_socket):
        client_socket, address = file_obj_socket.accept()
        client_socket.setblocking(False)

        peername = client_socket.getpeername()

        if len(self.players) < 2:
            client_socket.sendall(b"Success")
            self.players.append({
                "file_obj": file_obj_socket,
                "socket": client_socket
            })

            logger.info(f"Connection from {peername}")

            self.socket_selector.register(
                client_socket, selectors.EVENT_READ, data=self.receive_handler
            )
        else:
            logger.info(f'Rejecting connection from {peername}')
            client_socket.sendall(b"Full server")
            client_socket.close()

    def receive_handler(self, file_obj_socket):
        data = file_obj_socket.recv(1024)
        if data:
            self.data_received(file_obj_socket, data)
        else:
            logger.info(f"Disconnect from {file_obj_socket.getpeername()}")
            self.socket_selector.unregister(file_obj_socket)
            for player in self.players:
                if player["file_obj"] is file_obj_socket:
                    del player

            file_obj_socket.close()

    def data_received(self, file_obj_socket, data):
        message = data.decode("utf-8")
        logger.info(f"Received from {file_obj_socket.getpeername()}: {message}")

        # send to all other peers
        for player in self.players:
            if player["socket"] is not file_obj_socket:
                player["socket"].sendall(data)

    def main_loop(self):
        try:
            while True:
                events = self.socket_selector.select()
                for key, _ in events:
                    callback = key.data
                    callback(key.fileobj)
        except KeyboardInterrupt:
            logger.info('Closing server')

        self.server_socket.close()
        self.socket_selector.close()


class Server:
    def __init__(self, host: str, port: int) -> None:
        self.game_server_instance = GameServer(host, port)

    def run(self) -> None:
        server_daemon_thread = threading.Thread(
            target=self.game_server_instance.main_loop, daemon=True
        )
        server_daemon_thread.start()
