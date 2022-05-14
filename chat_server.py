import socket
import time

if __name__ == '__main__':
    PORT = 50001
    HOST = ''
    motd = 'Welcome to the server!'
    motd_bytes = motd.encode()

    print('[SERVER]\n')
    print('Starting server...')
    with socket.create_server((HOST, PORT)) as server:
        print('Server:', server.getsockname())
        server.listen()
        print('Server is now listening.')
        print("Awaiting connections...")
        conn, addr = server.accept()
        try:
            with conn:
                name = ''
                name_bytes = conn.recv(64)
                name = name_bytes.decode()
                print(f'{addr} has connected as {name}.')
                conn.sendall(motd_bytes)
                while True:
                    msg_bytes = conn.recv(64)
                    if not msg_bytes: break
                    msg = msg_bytes.decode()
                    print(msg)
        except Exception as e:
            print(e)
        finally:
            if name:
                print(f'{name} has disconnected.')
            else:
                print(f'{addr} has disconnected.')
    print('Server closed.\n')