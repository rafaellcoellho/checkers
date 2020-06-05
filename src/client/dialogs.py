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


class PassTurnDialog:
    def __init__(self, client, is_my_turn):
        self.button_text = "Next Turn" if is_my_turn else " Waiting "
        self.button_state = tk.NORMAL if is_my_turn else tk.DISABLED
        self.client = client

        self.root = None
        self.confirm_button = None

    def setup(self):
        self.root = tk.Tk()
        self.root.title("")

        w = 110
        h = 50
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry(f"{w}x{h}+{int(x)}+{int(y)}")

        self.root.resizable(0, 0)
        self.root.columnconfigure([0, 1, 2], minsize=10)
        self.root.rowconfigure([0, 1, 2], minsize=10)

        self.confirm_button = tk.Button(
            self.root, text=self.button_text, command=self.next_turn, state=self.button_state
        )
        self.confirm_button.grid(row=1, column=1)

        self.root.mainloop()

    def next_turn(self):
        self.client.send_to_server("ptn:__,__")
        self.confirm_button["state"] = tk.DISABLED
        self.confirm_button["text"] = " Waiting "

    def is_my_turn(self):
        self.confirm_button["state"] = tk.NORMAL
        self.confirm_button["text"] = "Next Turn"

    def show_message(self, msg):
        self.confirm_button["state"] = tk.DISABLED
        self.confirm_button["text"] = msg

    def run(self):
        from threading import Thread

        dialog_thread = Thread(
            target=self.setup, daemon=True
        )
        dialog_thread.start()
