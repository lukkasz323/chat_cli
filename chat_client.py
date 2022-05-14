import socket
import time
from chat import exception

if __name__ == '__main__':
    PORT = 50001
    HOST = 'localhost'
    name = 'Marek'
    name_bytes = name.encode()
    attempt = 1
    xd = 0
    
    print('[CLIENT]\n')
    while True:
        print(f'Connecting to ({HOST}, {PORT})... [{attempt}]')
        try:
            # Connection
            with socket.create_connection((HOST, PORT)) as client:
                print('Connected to', client.getpeername())
                client.sendall(name_bytes)
                while True:
                    inp = input('> ')
                    inp_bytes = inp.encode()
                    client.sendall(inp_bytes)
                    break
            print('Connection closed.\n')
            break
        except Exception as e:
            exception(e)
            if attempt < 10:
                attempt += 1
            else:
                print("Failed to connect to the server.\n")
                break