import socket
import time

if __name__ == '__main__':
    HOST = ''
    PORT = 50001

    print('Starting server...')

    with socket.create_server((HOST, PORT)) as server:
        print('Server:', server.getsockname())
        server.listen()
        print('Server is now listening.')

        print("Awaiting connections...")
        conn, addr = server.accept()
        with conn:
            name = conn.recv(64)
            print(addr, 'has connected as', name)
            while True:
                data = conn.recv(64)
                if not data: break
                decoded = data.decode()
                print(decoded)
    print('Server closed.\n')