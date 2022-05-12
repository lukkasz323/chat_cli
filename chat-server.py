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
        print(addr, 'has connected.')
        with conn.recv(64) as data:
            print(data)
    print('Server closed.')