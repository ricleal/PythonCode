TIC = None
def tic():
    global TIC
    TIC = datetime.datetime.now()

def toc():
    now = datetime.datetime.now()
    return (now-TIC).total_seconds()
