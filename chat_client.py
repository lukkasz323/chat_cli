import socket

def exception(msg):
    print(f'\nEXCEPTION: {msg}\n')

def chat(prefix=''):
    inp = input(f'{prefix}> ')
    encoded = inp.encode()
    client.sendall(encoded)

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 50001
    attempt = 1

    while True:
        print(f'Connecting to ({HOST}, {PORT})... [{attempt}]')
        try:
            with socket.create_connection((HOST, PORT)) as client:
                print('Connected to', client.getpeername())
                try:
                    print('Please input your name:')
                    chat('Name')
                    print('Connection closed.\n')
                except Exception as msg:
                    exception(msg)
                break
        except Exception as msg:
            exception(msg)
            if attempt < 10:
                attempt += 1
            else:
                print("Failed to connect to the server.\n")
                break