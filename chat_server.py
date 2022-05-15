import socket
import time

from chat import exception

if __name__ == '__main__':
    PORT = 50001
    HOST = ''
    motd = 'Welcome to the server!'
    motd_bytes = motd.encode()
    name = ''

    print('[SERVER]\n')
    print('Starting server...')
    # Start server and wait for connections
    with socket.create_server((HOST, PORT)) as server:
        print('Server:', server.getsockname())
        server.listen()
        print('Server is now listening.')
        print("Awaiting connections...")
        conn, addr = server.accept()
        try:
            # Connection
            with conn:
                name_bytes = conn.recv(64) # 1st relay
                name = name_bytes.decode()
                print(f'{addr} has connected as {name}.')

                conn.sendall(motd_bytes) # 2nd relay

                while True:
                    msg_bytes = conn.recv(64) # 3rd relay
                    msg = msg_bytes.decode()
                    print(f'{name}: {msg}')
        except Exception as e:
            exception(e)
        finally:
            if name:
                print(f'{name} has disconnected.')
            else:
                print(f'{addr} has disconnected.')
    print('Server closed.\n')