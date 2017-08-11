# pylint: disable-msg=C0103

'''

Sqlite with multiple processes

Same as example 2 but:

1. locks the db to see if the object it's there
2. frees the db
3. if it is returns it
4. if it is not:
    long operation to get it
    locks the db
    checks again if it is there:
    if it's not, inserts it
    frees the db

'''

from __future__ import print_function, with_statement

import sqlite3
import sys
import time
import random
import string
import logging
from hashlib import sha1
from pprint import pprint
from multiprocessing import Process, Queue, Lock


# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

N = 10 # Number of parallel cycles
DB = "/tmp/test.db"

def insert_into_db(conn, key, value):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pairs VALUES (?,?)", (key,value))
            cursor.close()
    except sqlite3.OperationalError as e:
        logger.error("--------- insert_into_db")
        #logger.exception(e)


def fetch_from_db(conn, key):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT key,value FROM pairs WHERE key=?', (key,) )
            result = cursor.fetchone()
            cursor.close()
        return result
    except sqlite3.OperationalError as e:
        logger.error("--------- fetch_from_db")
        #logger.exception(e)

def fetch_or_insert(conn, key, queue, lock):
    '''
    The database remains loked if the object
    needs to be fetch from somewhere else
    Need to find a solution
    @returns: tuple key,value
    '''
    lock.acquire()
    result = fetch_from_db(conn, key)
    lock.release()
    if result is not None:
        logger.debug("Exists in the DB: %s", result)
    else:
        # Sleep simulates a slow operation to get the data from somewhere else
        time.sleep(random.random())
        value = random_str_generator()
        logger.debug("Inserting in the DB: Key = %s :: Value = %s", key, value)
        lock.acquire()
        if not fetch_from_db(conn, key):
            insert_into_db(conn, key, value)
        lock.release()
        result = (key, value)
    queue.put(result)

def show_queue_contents(queue):
    '''
    This can be seen as a consumer
    '''
    while True:
        value  = queue.get()
        if value is None:
            # Poison pill means shutdown
            queue.close()
            break
        logger.info("fetch_or_insert returned: %s", value)


def random_str_generator(size=6, chars=string.ascii_letters + string.digits):
    random.seed()
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == '__main__':
    lock = Lock()
    conn = sqlite3.connect(DB)
    # DB initialisation
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE pairs ( key int primary key not null, value text not null)''')
        conn.commit()
        cursor.close()
    except sqlite3.OperationalError as e:
        logger.error("Looks like the table pairs exist already,,,")
        #logger.exception(e)

    # Queue to put the results of every fetch_or_insert
    queue = Queue()

    jobs = []
    for _ in range(N):
        key = random.randint(1,10)
        p = Process(target=fetch_or_insert, args=(conn, key, queue, lock, ))
        jobs.append(p)
        p.start()

    # starts the thread to display of the queue
    qp = Process(target=show_queue_contents, args=(queue, ))
    qp.start()

    # Waits for all jobs to finish
    for p in jobs:
        p.join()

    # All jobs finished, puts not in the queue: Poison pill
    # and waits for it to finish
    queue.put(None)
    qp.join()

    # DB cleanup
    with conn:
        cursor = conn.cursor()
        cursor.execute("delete from pairs")
        cursor.execute("drop table pairs")
        cursor.close()
    conn.close()

    logger.info("Done!")