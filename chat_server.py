import socket
import threading
import time
from chat import exception

def broadcast(msg: str):
    msg_bytes = msg.encode()
    for client in client_list:
        client.sendall(msg_bytes)

def receive():
    msg_bytes = server.recv(1024)
    msg = msg_bytes.decode()

def accept():
    while True:
        client, addr = server.accept()
        with client:
            # Check if connection is coming from a valid client
            data = client.recv(1024) # 1. relay
            if data != TOKEN:
                print(f'{addr} has an invalid token. Connection refused.')
                continue

            # Receive and save client info
            print(f'{addr} has connected.')
            data = client.recv(1024) # 2. relay
            nickname = data.decode()
            print(f'{addr} is now known as {nickname}')
            client_list.append(client)
            nickname_list.append(nickname)
            broadcast(f'{nickname} has joined the server.') # 3. relay
            
            print(client_list)
            print(nickname_list)

if __name__ == '__main__':
    TOKEN = b'1168d420-6e9f-4caf-8956-baf7d8394d54'
    HOST = ''
    PORT = 50001
    motd = 'Welcome to the server!'
    client_list = []
    nickname_list = []

    print('[SERVER]\n')
    print('Starting server...')
    with socket.create_server((HOST, PORT)) as server:
        print(f'Server: {server.getsockname()}')
        server.listen()
        print("Server started.")
        accept()
        receive()
    print('Server closed.\n')