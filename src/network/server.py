import threading
import types
import selectors


def process_messages(key, mask, selector):
    server_socket = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        received_data = server_socket.recv(1024)
        if received_data:
            data.output += received_data
        else:
            print('closing connection to', data.address)
            selector.unregister(server_socket)
            server_socket.close()
    if mask & selectors.EVENT_WRITE:
        if data.output:
            print('echoing', repr(data.output), 'to', data.address)
            sent = server_socket.send(data.output)
            data.output = data.output[sent:]


def accept_new_connection(socket, selector):
    connection, address = socket.accept()
    connection.setblocking(False)
    print('accepted connection from', address)

    # TODO: create better representation for data
    data = types.SimpleNamespace(address=address, input=b'', output=b'')

    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(connection, events, data=data)


def main_loop(host, port):
    import socket

    connection_info = (host, port)
    selector = selectors.DefaultSelector()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(connection_info)
    server_socket.listen(2)

    print('listening on', connection_info)

    server_socket.setblocking(False)
    selector.register(server_socket, selectors.EVENT_READ, data=None)

    while True:
        events = selector.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_new_connection(key.fileobj, selector)
            else:
                process_messages(key, mask, selector)


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        args_to_server = (self.host, self.port)
        server_daemon_thread = threading.Thread(
            target=main_loop, args=args_to_server, daemon=True
        )
        server_daemon_thread.start()
