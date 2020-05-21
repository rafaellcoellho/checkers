import tkinter as tk


class NetworkConfigurationUi:
    def __init__(self):
        self.is_hosting_server = None
        self.ip = None
        self.port = None

        self.root = tk.Tk()
        self.root.title("Network Configuration")
        self.root.geometry("225x130")
        self.root.resizable(0, 0)
        self.root.columnconfigure([0, 1], minsize=10)
        self.root.rowconfigure([0, 1, 2, 3], minsize=30)

        self.connect_to_server_label = tk.Label(self.root, text="Configure client connection:")
        self.connect_to_server_label.grid(row=0, column=0, columnspan=2)

        self.ip_label = tk.Label(self.root, text="IP")
        self.ip_label.grid(row=1, column=0)

        self.ip_entry = tk.Entry(self.root, width="15")
        self.ip_entry.insert(0, '127.0.0.1')
        self.ip_entry.grid(row=1, column=1)

        self.port_label = tk.Label(self.root, text="Port")
        self.port_label.grid(row=2, column=0)

        self.port_entry = tk.Entry(self.root, width="15")
        self.port_entry.insert(0, '65432')
        self.port_entry.grid(row=2, column=1)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(row=3, column=0, columnspan=2, sticky="e", padx=5, pady=5)
        self.buttons_frame.columnconfigure([0, 1], minsize=35)
        self.buttons_frame.rowconfigure(0, minsize=10)

        self.host_local_button = tk.Button(
            self.buttons_frame, text="Host server locally", command=self.set_host_server_local
        )
        self.host_local_button.grid(row=0, column=0)

        self.confirm_button = tk.Button(self.buttons_frame, text="Connect", command=self.get_client_config)
        self.confirm_button.grid(row=0, column=1)

    def set_host_server_local(self):
        self.ip = None
        self.port = None

        self.is_hosting_server = True

        self.host_local_button.master.master.destroy()

    def get_client_config(self):
        self.ip = self.ip_entry.get()
        self.port = int(self.port_entry.get())

        self.is_hosting_server = False

        self.confirm_button.master.master.destroy()

    def run(self):
        self.root.mainloop()

        return self.is_hosting_server, self.ip, self.port
