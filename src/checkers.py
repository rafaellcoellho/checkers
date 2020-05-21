import sys
import time

from engine.board import Board
from network.server import Server
from network.client import Client
from client.network_configuration import NetworkConfigurationUi
from client.dialogs import ServerWaitingDialog

if __name__ == "__main__":
    net_conf_ui = NetworkConfigurationUi()
    info = net_conf_ui.run()

    if not any(info):
        sys.exit()

    is_hosting_server, ip, port = info

    if is_hosting_server:
        server = Server('127.0.0.1', 65432)
        server.run()

        client = Client('127.0.0.1', 65432)
        time.sleep(1)
        if client.connect() is not True:
            sys.exit()

        wait_dialog = ServerWaitingDialog('127.0.0.1', 65432, server.get_number_of_players)
        wait_dialog.run()
    else:
        client = Client(ip, port)
        if client.connect() is not True:
            sys.exit()

    time.sleep(10)
    print("begin match")
