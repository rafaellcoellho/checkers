import socket


class Server:
    def __init__(self, host, port):
        self.connection_info = (host, port)

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.connection_info)
            s.listen()
            conn, address = s.accept()
            with conn:
                print('Connected by', address)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
