import socket
import time

from chat import exception

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 50001
    attempt = 1
    nickname = 'Marek'
    
    print('[CLIENT]\n')
    while True:
        print(f"Connecting to ('{HOST}', {PORT})... [{attempt}]")
        try:
            # Connection
            with socket.create_connection((HOST, PORT)) as client:
                pass
            print('Connection closed.\n')
            break
        except Exception as e:
            exception(e)
            if attempt < 10:
                attempt += 1
            else:
                print("Failed to connect to the server.\n")
                break