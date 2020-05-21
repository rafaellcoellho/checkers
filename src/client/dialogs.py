import tkinter as tk

from client import logger


class ServerWaitingDialog:
    def __init__(self, ip: str, port: int, count_players_callback):
        self.count_players_callback = count_players_callback

        self.root = tk.Tk()
        self.root.title("Network Configuration")

        w = 225
        h = 130
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry(f"{w}x{h}+{int(x)}+{int(y)}")

        self.root.resizable(0, 0)
        self.root.columnconfigure([0, 1], minsize=113)
        self.root.rowconfigure([0, 1, 2, 3], minsize=30)

        self.network_info_label = tk.Label(self.root, text="Network Info's:")
        self.network_info_label.grid(row=0, column=0, columnspan=2)

        self.server_ip_label = tk.Label(self.root, text="Server IP:")
        self.server_ip_label.grid(row=1, column=0)

        self.server_ip_value_label = tk.Label(self.root, text=ip)
        self.server_ip_value_label.grid(row=1, column=1)

        self.server_port_label = tk.Label(self.root, text="Server Port:")
        self.server_port_label.grid(row=2, column=0)

        self.server_port_value_label = tk.Label(self.root, text=str(port))
        self.server_port_value_label.grid(row=2, column=1)

        self.network_info_label = tk.Label(self.root, text="Waiting another player...")
        self.network_info_label.grid(row=3, column=0, columnspan=2)

    def check_client_connection(self):
        n_of_players = self.count_players_callback()
        logger.info(f"number of players connected: {n_of_players}")

        if n_of_players == 2:
            self.root.destroy()
        else:
            self.root.after(2000, self.check_client_connection)

    def run(self):
        self.root.after(2000, self.check_client_connection)
        self.root.mainloop()
