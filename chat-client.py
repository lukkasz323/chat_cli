import socket

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 50001
    attempt = 1

    while True:
        print(f'Connecting to ({HOST}, {PORT}) [{attempt}]')
        try:
            with socket.create_connection((HOST, PORT)) as client:
                print('Connected to', client.getpeername())
                client.send(f'xd1')
        except:
            if attempt < 10:
                attempt += 1
                continue
            else:
                print("Failed to connect to the server.")
        break