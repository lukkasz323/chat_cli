import time
from threading import Thread
from socket import socket, create_server
from chat import exc, exc_traceback
from chat_server_cfg import HOST, PORT, motd

class ServerData:
    def __init__(self):
        self.chatters = {} # Key -> socket (client), Value -> str (nickname)
        self.commands_descriptions = f'Available commands:\n'
        self.commands = {
            '/'        : (cmd_slash, False, 'Print available commands.'),
            '/chatters': (cmd_chatters, False, 'Print online chatters.'),
            '/kick'    : (cmd_kick, True, 'Disconnects a specified chatter.')
            }
        
        self.setup()
        
    def setup(self):
        for k in self.commands:
            self.commands_descriptions += f'{k} - {self.commands[k][2]}\n'

def cmd_slash(caller: socket, server_data):
    broadcast(server_data, server_data.commands_descriptions)

def cmd_chatters(caller: socket, server_data):
    broadcast(server_data, get_chatters(server_data.chatters))

def cmd_kick(caller: socket, server_data, arg: str):
    if arg in server_data.chatters.values():
        target = get_k_from_v(server_data.chatters, arg)
        kick_client(server_data, target)
    else:
        broadcast(server_data, 'Invalid nickname.')

def kick_client(server_data, target: socket):
    target.close()
    server_data.chatters.pop(target)
    broadcast(server_data, f'{server_data.chatters[target]} has left the server.')
    print(get_chatters(server_data.chatters))

def get_chatters(the_dict: dict):
    result = [v for v in the_dict.values()]
    return f'Chatters: {result}'

def get_k_from_v(the_dict: dict, x):
    return [k for k, v in the_dict.items() if v == x][0]

# Send a message and source info to every client.
def broadcast(server_data, msg, source='Server'):
    source = source.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    for target in server_data.chatters:
        target.sendall(source)
        time.sleep(0.1)
        target.sendall(msg)
    print(f'Broadcast: {source} / {msg}')
    
# Send a message and source info to a selected client.
def unicast(chatters, target: socket, msg, source='(PM) Server'):
    source = source.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    target.sendall(source)
    time.sleep(0.1)
    target.sendall(msg)
    print(f'Unicast to {chatters[target]}: {source} / {msg}')

# Handler ran in a seperate thread for each client.
def handler(client: socket, server_data):
    while True:
        try:
            data = client.recv(1024)
            if data:
                decoded = data.decode()
                # Handle client commands.
                if decoded[0] == '/':
                    split = decoded.split()
                    if split[0] in server_data.commands:
                        func = server_data.commands[split[0]][0]
                        is_arg_req = server_data.commands[split[0]][1]
                        if is_arg_req:
                            if len(split) > 1:
                                func(client, server_data, split[1])
                            else:
                                broadcast(server_data, 'This command requies an argument.')
                        else:
                            func(client, server_data)
                    else:
                        broadcast(server_data, 'Unknown command, type "/" for a list of commands.')
                # Broadcast client messages.
                else:
                    broadcast(server_data, data, server_data.chatters[client])
        except:
            exc_traceback()
            kick_client(server_data, client)
            break

def main():
    TOKEN = b'1168d420-6e9f-4caf-8956-baf7d8394d54' # Used for connection verification.
    
    server_data = ServerData()
        
    # [Server]
    print('[SERVER]\n')
    print('Starting server...')
    try:
        with create_server((HOST, PORT)) as server:
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
                nickname_repetitions = 0
                
                data = client.recv(1024) # 2. relay
                nickname = data.decode()
                if nickname in server_data.chatters.values():
                    nickname_repetitions += 1
                    nickname += str(nickname_repetitions)
                print(f'{addr} has connected as {nickname}.')
                server_data.chatters[client] = nickname
                broadcast(server_data, f'{nickname} has joined the server.')

                # Send client a welcome message.
                time.sleep(0.1)
                unicast(server_data.chatters, client, motd)

                # Print an updated list of clients.
                print(get_chatters(server_data.chatters))

                # Handle this client in a separate thread.
                handler_thread = Thread(target=handler, args=(client, server_data))
                handler_thread.start()
    except OSError as e: # Starting server on occupied address.
        exc(e)
    print('Server closed.\n')

if __name__ == '__main__':
    main()

# TODO: Fix "kick" command
# TODO: Add "Is now know as" and renaming.
# TODO: Add "who am I" command.
# TODO: Add "show motd" command.
# TODO: Add "change motd" command.