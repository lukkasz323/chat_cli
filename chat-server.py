import socket

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

    print('Server closed.')