import traceback

def exc():
    print('-------------------- EXCEPTION:')
    traceback.print_exc()
    print('--------------------')

def exc_simple(e):
    print(f'EXCEPTION: {e}')