
import os
from multiprocessing import Process
import time
import redis
from pprint import pformat

def publish(myredis, channel_name):
    '''
    Publish some random data
    '''
    for i in range(3):
        myredis.publish(channel_name,'Content number {} published for channel {}.'.format(i,channel_name))
        time.sleep(0.11)

def subscribe(myredis, channel_name):
    pubsub = myredis.pubsub()
    pubsub.subscribe([channel_name])
    for item in pubsub.listen():
        print('\nPID = {} with content:\n{}'.format(os.getpid(), pformat(item)))

if __name__ == '__main__':
    myredis = redis.Redis()
    
    channel_name = "channel-1"
    processes = []
    processes.append(
        Process(target=publish, args=(myredis,channel_name)))
    processes.append(
        Process(target=subscribe, args=(myredis,channel_name)))
    processes.append(
        Process(target=subscribe, args=(myredis,channel_name)))
    
    for p in processes:
        p.start()
    for p in processes:
        p.join()
