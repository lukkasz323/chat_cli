import socket

def exception(e):
    print(f'\nEXCEPTION: {e}\n')

def chat(prefix=''):
    inp = input(f'{prefix}> ')
    inp_bytes = inp.encode()
    client.sendall(inp_bytes)

def receive():
    msg_bytes= client.recv(64)

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
            with socket.create_connection((HOST, PORT)) as client:
                print('Connected to', client.getpeername())
                client.sendall(name_bytes)
                while True:
                    chat()
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