import socket
import threading
import time
from chat import exc, exc_traceback

def handler():
    while True:
        pass

def receive(data):
    if isinstance(data, bytes):
        data = data.decode()
    print(data)

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

                handler_thread = threading.Thread(target=handler)
                handler_thread.start()
            print('Connection closed.\n')
            break
        except ConnectionRefusedError as e:
            exc(e)
            if attempt < 10:
                attempt += 1
            else:
                print("Failed to connect to the server.\n")
                break