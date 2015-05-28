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

if __name__ == '__main__':
	tic();
	time.sleep(0.2)
	print "Took %.2f seconds"%toc()