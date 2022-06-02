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
            client.close()
            continue

        # Receive and save client info
        print(f'{addr} has connected.')
        data = client.recv(1024) # 2. relay
        nickname = data.decode()
        print(f'{addr} is now known as {nickname}.')
        client_list.append(client)
        nickname_list.append(nickname)
        broadcast(f'{nickname} has joined the server.') # 3. relay
        time.sleep(0.1)
        unicast(motd, client, nickname)

        # Debug
        print('Chatters:', nickname_list)

        # Handle this client in a new thread from now on,
        # the main thread loops back to wait for new connections.
        handler_thread = threading.Thread(target=handler, args=(client, ))
        handler_thread.start()

def handler(client: socket.socket):
    index = client_list.index(client)
    nickname = nickname_list[index]

    while True: 
        try:
            data = client.recv(1024)
            if data:
                broadcast(data)
        except:
            exc_traceback()
            client_list.pop(index)
            nickname_list.pop(index)
            client.close()
            broadcast(f'{nickname} has left the server.')
            break

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
    try:
        with socket.create_server((HOST, PORT)) as server:
            print(f'Server hosted on {server.getsockname()}')
            server.listen()
            print("Server started.")
            accept()
    except OSError as e:
        exc(e)
    print('Server closed.\n')