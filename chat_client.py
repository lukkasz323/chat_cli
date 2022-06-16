import socket
import threading
import time
from chat_client_cfg import *
from chat import exc, exc_traceback

def receive(client):
    while True:
        try:
            source = client.recv(1024)
            msg = client.recv(1024)
            source = source.decode()
            msg = msg.decode()
            if source and msg:
                print(f'{source}: {msg}')
        except ConnectionError as e:
            exc(e)
            break

if __name__ == '__main__':
    TOKEN = b'1168d420-6e9f-4caf-8956-baf7d8394d54' # Used for connection verification.

    print('[CLIENT]\n')

    # Print settings. (Import)
    print(f'[Settings]\nHost: {HOST}\nPort: {PORT}\nNickname: {nickname}\n')

    # [Connection]
    attempt = 1
    while True:
        print(f'Connecting to "{HOST}:{PORT}"... [{attempt}]')
        try:
            with socket.create_connection((HOST, PORT)) as client:
                print(f'\nConnected to {client.getpeername()}.')

                # Prove that connection is coming from a valid client.
                client.sendall(TOKEN) # 1. relay
                time.sleep(0.1)
                client.sendall(nickname.encode()) # 2. relay

                # Handle server data receiving in a separate thread.
                receive_thread = threading.Thread(target=receive, args=(client, ))
                receive_thread.start()

                # Handle sending messages to the server.
                while True:
                    inp = input()
                    data = inp.encode()
                    client.sendall(data)
        except ConnectionRefusedError as e:
            exc(e)
            if attempt < 10:
                attempt += 1
            else:
                print("Failed to connect to the server.\n")
                break
        except ConnectionError:
            print('Connection closed.\n')
            break