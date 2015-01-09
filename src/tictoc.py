import time

TIC = None
 
def tic():
    global TIC
    TIC = time.time()

def toc():
    """
    Return time in seconds
    """
    now = time.time()
    delta = now-TIC
    return delta
