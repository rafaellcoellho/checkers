import sys
import time

from queue import Queue

from engine.defines import Players
from network.server import Server
from network.client import Client
from client.network_configuration import NetworkConfigurationUi
from client.dialogs import ServerWaitingDialog
from client.game import GameUi

if __name__ == "__main__":
    net_conf_ui = NetworkConfigurationUi()
    info = net_conf_ui.run()

    if not any(info):
        sys.exit()

    is_hosting_server, ip, port = info
    receive_queue = Queue()

    server = None
    client = None

    if is_hosting_server:
        player = Players.P1
        server = Server('127.0.0.1', 65432)
        server.run()

        client = Client('127.0.0.1', 65432, receive_queue)
        time.sleep(1)
        if client.connect() is not True:
            sys.exit()

        client.listen()

        wait_dialog = ServerWaitingDialog('127.0.0.1', 65432, server.get_number_of_players)
        wait_dialog.run()
    else:
        player = Players.P2
        client = Client(ip, port, receive_queue)
        if client.connect() is not True:
            sys.exit()
        client.listen()

    game = GameUi(player, client, receive_queue)
    game.run()

    if server is not None:
        server.close_server()

    client.disconnect()
