class Constant(object):
    UNDEF = -2
    BOMB = -1

def is_bomb(x):
    return x == -1

def is_undef(x):
    return x == 2

def is_safe(x):
    return x >= 0        
