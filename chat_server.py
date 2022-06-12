from http import client
import socket
import threading
import time
from chat import exc, exc_traceback

def cmd_slash():
    broadcast(commands_descriptions)

def cmd_chatters():
    broadcast(f'Chatters: {nickname_list}')

def cmd_kick(nickname: str):
    if nickname in nickname_list:
        index = nickname_list.index(nickname)
        client = client_list[index]

        kick_client(client)
    else:
        broadcast('Invalid nickname.')

def kick_client(client: socket.socket):
    index = client_list.index(client)
    nickname = nickname_list[index]

    client.close()
    client_list.pop(index)
    nickname_list.pop(index)
    broadcast(f'{nickname} has left the server.')
    print('Chatters:', nickname_list) # Debug

def change_nickname():
    pass

# Send a message and source info to every client.
def broadcast(msg, source='Server'):
    source = source.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    for client in client_list:
        client.sendall(source)
        time.sleep(0.1)
        client.sendall(msg)
    print(f'Broadcast: {source} / {msg}')
    
# Send a message and source info to a selected client.
def unicast(msg, client: socket.socket, source='(PM) Server'):
    index = client_list.index(client)
    nickname = nickname_list[index]

    source = source.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    client.sendall(source)
    time.sleep(0.1)
    client.sendall(msg)
    print(f'Unicast to {nickname}: {msg}')

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
                split = decoded.split()
                if split[0] in commands:
                    func = commands[split[0]][0]
                    if func.__code__.co_argcount == 1:
                        if len(split) > 1:
                            func(split[1])
                        else:
                            broadcast('This command requies an argument.')
                    else:
                        func()
                else:
                    broadcast('Unknown command, type "/" for a list of commands.')
            # Broadcast client messages.
            else:
                if data:
                    broadcast(data, nickname)
        except:
            exc_traceback()
            kick_client(client)
            break

if __name__ == '__main__':
    TOKEN = b'1168d420-6e9f-4caf-8956-baf7d8394d54'
    HOST = ''
    PORT = 50001
    motd = 'Welcome to the server!'
    nickname_repetitions = 0
    client_list = []
    nickname_list = []
    commands = {
        '/'        : (cmd_slash, 'Print available commands.'),
        '/chatters': (cmd_chatters, 'Print online chatters.'),
        '/kick'    : (cmd_kick, 'Disconnects a specified chatter.')
        }

    print('[SERVER]\n')

    # Setup
    commands_descriptions = f'Available commands:\n'
    for k in commands:
        commands_descriptions += f'{k} - {commands[k][1]}\n'

    # Server
    print('Starting server...')
    try:
        with socket.create_server((HOST, PORT)) as server:
            print(f'Server hosted on {server.getsockname()}')
            server.listen()
            print("Server started.")
            while True:
                # Wait for clients to accept.
                client, addr = server.accept()

                # Check if connection is coming from a valid client.
                data = client.recv(1024) # 1. relay
                if data != TOKEN:
                    print(f'{addr} has an invalid token. Connection refused.')
                    client.close()
                    continue

                # Receive and handle client info.
                data = client.recv(1024) # 2. relay
                nickname = data.decode()
                if nickname in nickname_list:
                    nickname_repetitions += 1
                    nickname += str(nickname_repetitions)
                print(f'{addr} has connected as {nickname}.')
                client_list.append(client)
                nickname_list.append(nickname)
                broadcast(f'{nickname} has joined the server.')

                # Send client a welcome message.
                time.sleep(0.1)
                unicast(motd, client)

                # Print an updated list of clients.
                print('Chatters:', nickname_list)

                # Handle this client in a new thread from now on while
                # the main thread loops back to wait for new connections.
                handler_thread = threading.Thread(target=handler, args=(client, ))
                handler_thread.start()
    except OSError as e: # Starting server on occupied address.
        exc(e)
    print('Server closed.\n')

# TODO: Add "who am I" command.