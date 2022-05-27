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