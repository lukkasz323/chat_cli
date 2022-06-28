import time
from threading import Thread
from socket import socket, create_server
from chat import exc, exc_traceback
from chat_server_cfg import HOST, PORT, motd

def cmd_slash(caller: socket, chatters, commands_descriptions):
    broadcast(chatters, commands_descriptions)

def cmd_chatters(caller: socket, chatters):
    print('XD1', type(caller), type(chatters)) #
    print('XD2', caller, chatters) #
    broadcast(chatters, get_chatters(chatters))

def cmd_kick(caller: socket, chatters, target_nick: str):
    if target_nick in chatters.values():
        target = get_k_from_v(chatters, target_nick)
        kick_client(chatters, target)
    else:
        broadcast(chatters, 'Invalid nickname.')

def kick_client(chatters, target: socket):
    target.close()
    chatters.pop(target)
    broadcast(chatters, f'{chatters[target]} has left the server.')
    print(get_chatters(chatters))

def get_chatters(the_dict: dict):
    print(the_dict) # <---------------- check this
    result = [v for v in the_dict.values()]
    return f'Chatters: {result}'

def get_k_from_v(the_dict: dict, x):
    return [k for k, v in the_dict.items() if v == x][0]

# Send a message and source info to every client.
def broadcast(chatters, msg, source='Server'):
    source = source.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    for target in chatters:
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
def handler(client: socket, chatters, commands):
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
                        is_chat_arg_req = commands[split[0]][1]
                        args = commands[split[0]][2]
                        print(func, args) #
                        print(len(split), len(args)) #
                        if is_chat_arg_req:
                            if len(split) > 1:
                                # func(client, *args)
                                func(client, chatters)
                            else:
                                broadcast(chatters, 'This command requies an argument.')
                        else:
                            func(client, *args)
                    else:
                        broadcast(chatters, 'Unknown command, type "/" for a list of commands.')
                # Broadcast client messages.
                else:
                    broadcast(chatters, data, chatters[client])
        except:
            exc_traceback()
            kick_client(chatters, client)
            break

def main():
    TOKEN = b'1168d420-6e9f-4caf-8956-baf7d8394d54' # Used for connection verification.
    
    server_data = {
        chatters: {} # Key -> client: socket, Value -> nickname: str
    }
    
    commands_descriptions = f'Available commands:\n'
    commands = {
        '/'        : (cmd_slash, False, (chatters, commands_descriptions), 'Print available commands.'),
        '/chatters': (cmd_chatters, False, (chatters), 'Print online chatters.'),
        '/kick'    : (cmd_kick, True, (chatters), 'Disconnects a specified chatter.')
        }

    # Setup
    for k in commands:
        commands_descriptions += f'{k} - {commands[k][2]}\n'
        
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
                if nickname in chatters.values():
                    nickname_repetitions += 1
                    nickname += str(nickname_repetitions)
                print(f'{addr} has connected as {nickname}.')
                chatters[client] = nickname
                broadcast(chatters, f'{nickname} has joined the server.')

                # Send client a welcome message.
                time.sleep(0.1)
                unicast(chatters, client, motd)

                get_k_from_v(chatters, 'User')# Print an updated list of clients.
                print(get_chatters(chatters))

                # Handle this client in a separate thread.
                handler_thread = Thread(target=handler, args=(client, chatters, commands))
                handler_thread.start()
    except OSError as e: # Starting server on occupied address.
        exc(e)
    print('Server closed.\n')

if __name__ == '__main__':
    main()

# TODO: Rewrite to OOP

# TODO: Add "Is now know as" and renaming.
# TODO: Add "who am I" command.
# TODO: Add "show motd" command.
# TODO: Add "change motd" command.
