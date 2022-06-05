import socket
import threading
import time
from chat import exc, exc_traceback

def cmd():
    broadcast(commands_list)

def cmd_chatters():
    broadcast(f'Chatters: {nickname_list}')

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
        nickname = client.recv(1024) # 2. relay
        nickname = nickname.decode()
        print(f'{addr} has connected as {nickname}.')
        client_list.append(client)
        nickname_list.append(nickname)
        broadcast(f'{nickname} has joined the server.')
        time.sleep(0.01)
        unicast(motd, client, nickname)

        print('Chatters:', nickname_list) # Debug

        # Handle this client in a new thread from now on,
        # the main thread loops back to wait for new connections.
        handler_thread = threading.Thread(target=handler, args=(client, ))
        handler_thread.start()

# Handler ran in a seperate thread for each client.
def handler(client: socket.socket):
    index = client_list.index(client)
    nickname = nickname_list[index]

    while True: 
        try:
            data = client.recv(1024)
            decoded = data.decode()

            # Handle client commands.
            if decoded[0] == '/': 
                if decoded in commands:
                    commands[decoded][0]()
                else:
                    broadcast('Unknown command, type "/" for a list of commands.')
            # Broadcast client messages.
            else:
                if data:
                    broadcast(data, nickname)
        except:
            exc_traceback()
            client_list.pop(index)
            nickname_list.pop(index)
            client.close()
            broadcast(f'{nickname} has left the server.')
            print('Chatters:', nickname_list) # Debug
            break

# Send a message and source info to every client.
def broadcast(msg, source='Server'):
    source = source.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    for client in client_list:
        client.sendall(source)
        time.sleep(0.01)
        client.sendall(msg)
    print(f'Broadcast: {source} / {msg}')
    
# Send a message and source info to a selected client.
def unicast(msg, client: socket.socket, nickname: str, source='(PM) Server'):
    source = source.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    client.sendall(source)
    time.sleep(0.01)
    client.sendall(msg)
    print(f'Unicast to {nickname}: {msg}')

if __name__ == '__main__':
    TOKEN = b'1168d420-6e9f-4caf-8956-baf7d8394d54'
    HOST = ''
    PORT = 50001
    motd = 'Welcome to the server!'
    client_list = []
    nickname_list = []
    commands = {
        '/'        : (cmd, 'Print available commands.'),
        '/chatters': (cmd_chatters, 'Print online chatters.')
        }
    commands_list = f'Available commands:\n'

    print('[SERVER]\n')
    print('Starting server...')

    # Setup
    for k in commands:
        commands_list += f'{k} - {commands[k][1]}\n'

    # Server
    try:
        with socket.create_server((HOST, PORT)) as server:
            print(f'Server hosted on {server.getsockname()}')
            server.listen()
            print("Server started.")
            accept()
    except OSError as e: # Starting server on occupied address.
        exc(e)
    print('Server closed.\n')

# TODO: Expand "cmd_chatters", nicer print, descriptions.