import socket
import time
from threading import Thread
from chat_server_cfg import *
from chat import exc, exc_traceback

def cmd_slash(caller: socket.socket):
    broadcast(commands_descriptions)

def cmd_chatters(caller: socket.socket):
    broadcast(get_chatters())

def cmd_kick(caller: socket.socket, nickname: str):
    if nickname in chatters.values():
        kick_client(client)
    else:
        broadcast('Invalid nickname.')

def kick_client(client: socket.socket):
    client.close()
    chatters.pop(client)
    broadcast(f'{nickname} has left the server.')
    print(get_chatters())

def get_chatters():
    result = [v for v in chatters.values()]
    return f'Chatters: {result}'

# Send a message and source info to every client.
def broadcast(msg, source='Server'):
    source = source.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    for client in chatters:
        client.sendall(source)
        time.sleep(0.1)
        client.sendall(msg)
    print(f'Broadcast: {source} / {msg}')
    
# Send a message and source info to a selected client.
def unicast(msg, client: socket.socket, source='(PM) Server'):
    source = source.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    client.sendall(source)
    time.sleep(0.1)
    client.sendall(msg)
    print(f'Unicast to {nickname}: {source} / {msg}')

# Handler ran in a seperate thread for each client.
def handler(client: socket.socket):
    while True:
        try:
            data = client.recv(1024)
            if data:
                decoded = data.decode()
                # Handle client commands.
                if decoded[0] == '/':
                    split = decoded.split()
                    if split[0] in commands:
                        func = commands[split[0]][0]
                        if func.__code__.co_argcount > 1:
                            if len(split) > 1:
                                func(client, split[1])
                            else:
                                broadcast('This command requies an argument.')
                        else:
                            func(client)
                    else:
                        broadcast('Unknown command, type "/" for a list of commands.')
                # Broadcast client messages.
                else:
                    broadcast(data, chatters[client])
        except:
            print('XD1')
            exc_traceback()
            kick_client(client)
            break

if __name__ == '__main__':
    TOKEN = b'1168d420-6e9f-4caf-8956-baf7d8394d54' # Used for connection verification.
    
    motd = 'Welcome to the server!'
    nickname_repetitions = 0
    chatters = {} # Key -> socket (client), Value -> str (nickname) 
    commands = {
        '/'        : (cmd_slash, 'Print available commands.'),
        '/chatters': (cmd_chatters, 'Print online chatters.'),
        '/kick'    : (cmd_kick, 'Disconnects a specified chatter.')
        }

    # Setup
    commands_descriptions = f'Available commands:\n'
    for k in commands:
        commands_descriptions += f'{k} - {commands[k][1]}\n'

    # [Server]
    print('[SERVER]\n')
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
                if nickname in chatters.values():
                    nickname_repetitions += 1
                    nickname += str(nickname_repetitions)
                print(f'{addr} has connected as {nickname}.')
                chatters[client] = nickname
                print(chatters)
                broadcast(f'{nickname} has joined the server.')

                # Send client a welcome message.
                time.sleep(0.1)
                unicast(motd, client)

                # Print an updated list of clients.
                print(get_chatters())

                # Handle this client in a separate thread.
                handler_thread = Thread(target=handler, args=(client, ))
                handler_thread.start()
    except OSError as e: # Starting server on occupied address.
        exc(e)
    print('Server closed.\n')

# TODO: MAJOR: Fix cmd_kick()
# TODO: Add "Is now know as" and renaming.
# TODO: Add "who am I" command.
