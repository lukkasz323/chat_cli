import socket
import time

from chat import exception

if __name__ == '__main__':
    HOST = ''
    PORT = 50001
    motd = 'Welcome to the server!'

    print('[SERVER]\n')
    print('Starting server...')
    with socket.create_server((HOST, PORT)) as server:
        print('Server:', server.getsockname())
        server.listen()
        print("Server started.")
    print('Server closed.\n')