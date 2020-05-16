import asyncio
import threading


def game_server_loop(host: str, port: int) -> None:
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    game_server = event_loop.create_server(GameServer, host, port)
    game_server_instance = event_loop.run_until_complete(game_server)

    print(f'Serving on {game_server_instance.sockets[0].getsockname()}')
    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        print('Closing server')

    game_server_instance.close()
    event_loop.run_until_complete(game_server_instance.wait_closed())
    event_loop.close()


class GameServer(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.peername = None

    def connection_made(self, transport: asyncio.transports.BaseTransport) -> None:
        self.peername = transport.get_extra_info('peername')
        print(f'Connection from {self.peername}')
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        message = data.decode()
        print(f'Received from {self.peername}: {message}')

        # send to all other peers


class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def run(self) -> None:
        args_to_server = (self.host, self.port)
        server_daemon_thread = threading.Thread(
            target=game_server_loop, args=args_to_server, daemon=True
        )
        server_daemon_thread.start()
