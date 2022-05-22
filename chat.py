import traceback

def exc(e):
    print(f'EXCEPTION: {e}')

def exc_traceback():
    print('-------------------- EXCEPTION:')
    traceback.print_exc()
    print('--------------------')