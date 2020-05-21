import sys
from engine.board import Board
from client.network_configuration import NetworkConfigurationUi

if __name__ == "__main__":
    net_conf_ui = NetworkConfigurationUi()
    info = net_conf_ui.run()

    if not any(info):
        sys.exit()

    print(info)
