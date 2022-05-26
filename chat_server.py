from cgi import test
import socket
import threading
import time
from chat import exc, exc_traceback

def accept():
    while True:
        client, addr = server.accept()

        # Check if connection is coming from a valid client.
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
        unicast(motd, client, nickname)
        
        # Handle this client in a new thread from now on,
        # the main thread loops back to wait for new connections.
        handler_thread = threading.Thread(target=handler, args=(client, ))
        handler_thread.start()

def handler(client: socket.socket):
    index = client_list.index(client)
    nickname = nickname_list[index]

    while True:
        print(1, client) # Debug  
        try:
            print(2, client) # Debug 
            data = client.recv(1024)
            broadcast(data)
            print(3, client) # Debug 
        except:
            print(4, client) # Debug 
            exc_traceback()
            client_list.pop(index)
            nickname_list.pop(index)
            print(client) # Debug
            broadcast('client.close()!') # Debug
            client.close()
            print(client) # Debug
            broadcast(f'{nickname} has left the server.')
            print(5, client) # Debug 
            break
        print(6, client) # Debug 

def broadcast(data):
    if isinstance(data, str):
        data = data.encode()
    for client in client_list:
        client.sendall(data)
    print(f'Broadcast: {data}')

def unicast(data, client: socket.socket, nickname: str):
    if isinstance(data, str):
        data = data.encode()
    client.sendall(data)
    print(f'Unicast to {nickname}: {data}')

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
        print(f'Server - {server.getsockname()}')
        server.listen()
        print("Server started.")
        accept()
    print('Server closed.\n')