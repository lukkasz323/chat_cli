import socket
import time
from chat import exception

if __name__ == '__main__':
    PORT = 50001
    HOST = '127.0.0.1'
    name = 'Marek'
    name_bytes = name.encode()
    attempt = 1
    xd = 0
    
    print('[CLIENT]\n')
    while True:
        print(f"Connecting to ('{HOST}', {PORT})... [{attempt}]")
        try:
            # Connection
            with socket.create_connection((HOST, PORT)) as client:
                print('Connected to', client.getpeername())

                client.sendall(name_bytes) # 1st relay

                motd_bytes = client.recv(64) # 2nd relay
                motd = motd_bytes.decode()
                print(motd)

                msg = input(f'{name}> ')
                msg_bytes = msg.encode()
                client.sendall(msg_bytes) # 3rd relay
            print('Connection closed.\n')
            break
        except Exception as e:
            exception(e)
            if attempt < 10:
                attempt += 1
            else:
                print("Failed to connect to the server.\n")
                break