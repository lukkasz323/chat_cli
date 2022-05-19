import socket
import threading
import time
from chat import exc, exc_simple

if __name__ == '__main__':
    TOKEN = b'1168d420-6e9f-4caf-8956-baf7d8394d54'
    HOST = '127.0.0.1'
    PORT = 50001
    attempt = 1
    nickname = 'Marek'
    print('[CLIENT]\n')
    while True:
        print(f"Connecting to ('{HOST}', {PORT})... [{attempt}]")
        try:
            with socket.create_connection((HOST, PORT)) as client:
                attempt = 1
                print(f'\nConnected to {client.getpeername()} as {nickname}.')

                # Prove that connection is coming from a valid client
                client.sendall(TOKEN) # 1. relay
                client.sendall(nickname.encode()) # 2. relay
                data = client.recv(1024) # 3. relay
                msg = data.decode()
                print(msg)
            print('Connection closed.\n')
            break
        except:
            exc()
            if attempt < 10:
                attempt += 1
            else:
                print("Failed to connect to the server.\n")
                break