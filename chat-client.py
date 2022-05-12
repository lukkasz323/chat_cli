import socket

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 50001

    with socket.create_connection((HOST, PORT)) as client:
        pass