import socket
import threading
import time
from chat import exception

def accept():
    while True:
        print(client_list)
        print(nickname_list)
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
            
            # Handle this client in a new thread from now on,
            # the main thread loops back to wait for new connections.
            handler_thread = threading.Thread(target=handler, args=(client,))
            handler_thread.start()

def handler(client):
    while True:
        try:
            msg_bytes = server.recv(1024)
            msg = msg_bytes.decode()
            broadcast(msg)
        except Exception as e:
            exception(e)
            client.close()
            index = client_list.index(client)
            client_list.pop(index)
            nickname_list.pop(index)

def broadcast(msg):
    msg_bytes = msg.encode()
    for client in client_list:
        client.sendall(msg_bytes)

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
    print('Server closed.\n')