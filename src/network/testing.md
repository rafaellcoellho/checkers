# Testing network module

Open a terminal, cd to root of this repository, activate the virtualenv and run python interpreter:

```bash
$ workon checkers
$ python
Python 3.6.10 (default, Dec 27 2019, 13:40:13) 
[GCC 9.2.1 20190827 (Red Hat 9.2.1-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from src.network.server import Server
>>> server = Server('127.0.0.1', 65432)
>>> server.run()
>>> listening on ('127.0.0.1', 65432)
```

You can CTRL + C the thread will still be active with the server listening for connections.
Use netstat in another tab to check:

```bash
$ netstat -an | grep 65432                                 
tcp        0      0 127.0.0.1:65432         0.0.0.0:*               LISTEN 
```

Just don't kill the python interpreter.
Now it's time to use the client.
In another terminal: 

```bash
$ workon checkers
$ python
Python 3.6.10 (default, Dec 27 2019, 13:40:13) 
[GCC 9.2.1 20190827 (Red Hat 9.2.1-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from src.network.client import Client
>>> client = Client('127.0.0.1', 65432)
>>> client.connect()
>>> client.send_to_server('hello world')
```

If everything is correct, in the server terminal:

```bash
[...]
>>> listening on ('127.0.0.1', 65432)
accepted connection from ('127.0.0.1', 41482)
echoing b'hello world' to ('127.0.0.1', 41482)
```
