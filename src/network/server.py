import selectors
import socket
import threading

from network import logger
from engine.board import Board
from engine.defines import Players
from engine.utils import cn, nc


class GameServer:
    def __init__(self, host: str, port: int) -> None:
        self.running = True
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

        self.board = Board()

        logger.info(f"Game state initiated")

    def get_number_of_players(self):
        return len(self.players)

    def accept_handler(self, file_obj_socket):
        client_socket, address = file_obj_socket.accept()
        client_socket.setblocking(False)

        peername = client_socket.getpeername()

        if len(self.players) < 2:
            client_socket.sendall(b"Success")
            self.players.append({
                "id": Players.P1 if len(self.players) == 0 else Players.P2,
                "file_obj": file_obj_socket,
                "socket": client_socket
            })

            logger.info(f"Connection from {peername}")

            self.socket_selector.register(
                client_socket, selectors.EVENT_READ, data=self.receive_handler
            )
        else:
            logger.info(f"Rejecting connection from {peername}")
            client_socket.sendall(b"Full server")
            client_socket.close()

    def receive_handler(self, file_obj_socket):
        data = file_obj_socket.recv(9)
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
        message: str = data.decode("utf-8")
        logger.info(f"Received from {file_obj_socket.getpeername()}: {message}")

        command = message[:3]

        if command == "mov":
            from_coord = message[4:6]
            to_coord = message[7:9]

            result = self.board.move(*cn(from_coord, to_coord))

            if result is False:
                # move piece to origin position in client
                reverse_message: bytes = str.encode(f"mov:{to_coord},{from_coord}")
                file_obj_socket.sendall(reverse_message)
            else:
                for player in self.players:
                    if player["socket"] is not file_obj_socket:
                        player["socket"].sendall(data)

                last_piece_removed = self.board.get_last_piece_removed()
                if last_piece_removed is not None:
                    char_coord: str = nc(last_piece_removed)
                    rm_message: bytes = str.encode(f"rmv:{char_coord},__")
                    for player in self.players:
                        player["socket"].sendall(rm_message)

                last_piece_king = self.board.get_last_piece_king()
                if last_piece_king is not None:
                    char_coord: str = nc(last_piece_king)
                    king_message: bytes = str.encode(f"kin:{char_coord},__")
                    for player in self.players:
                        player["socket"].sendall(king_message)

        elif command == "ptn":
            winner = self.board.game_winner()
            if winner is not None:
                for player in self.players:
                    if player["id"] is winner:
                        player["socket"].sendall(b"win:__,__")
                    else:
                        player["socket"].sendall(b"los:__,__")
            else:
                self.board.next_turn()
                file_obj_socket.sendall(b"ntn:__,__")
                for player in self.players:
                    if player["socket"] is not file_obj_socket:
                        player["socket"].sendall(b"ytn:__,__")
        else:
            logger.error(f"Unknown command {message}")

    def main_loop(self):
        try:
            while self.running:
                events = self.socket_selector.select()
                for key, _ in events:
                    callback = key.data
                    callback(key.fileobj)
        except KeyboardInterrupt:
            logger.info("Closing server")

        self.server_socket.close()
        self.socket_selector.close()

    def close_server(self):
        self.running = False


class Server:
    def __init__(self, host: str, port: int) -> None:
        self.game_server_instance = GameServer(host, port)

    def get_number_of_players(self):
        return self.game_server_instance.get_number_of_players()

    def run(self) -> None:
        server_daemon_thread = threading.Thread(
            target=self.game_server_instance.main_loop, daemon=True
        )
        server_daemon_thread.start()

    def close_server(self):
        self.game_server_instance.close_server()