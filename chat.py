import traceback

# Simple output (less clutter)
def exc(e):
    print('-------------------- EXCEPTION CAUGHT:')
    print(e)
    print('--------------------')

# Traceback output (more clutter)
def exc_traceback():
    print('-------------------- EXCEPTION CAUGHT:')
    traceback.print_exc()
    print('--------------------')
    
def get_chatters(the_dict: dict):
    result = [v for v in the_dict.values()]
    return f'Chatters: {result}'

def get_k_from_v(the_dict: dict, x):
    return [k for k, v in the_dict.items() if v == x][0]