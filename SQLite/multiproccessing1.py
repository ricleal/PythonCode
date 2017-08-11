# pylint: disable-msg=C0103

'''

Sqlite with multiple processes

Check if something is in the DB
if it it is, returns it
if it is not, get it from somewhere (long operation) 
   and inserts in the db and returns it
The db is locked during all that
Shows the results at the same time

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
from multiprocessing import Process, Manager, Lock


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

def fetch_or_insert(conn, key, shared_results, lock):
    '''
    The database remains loked if the object
    needs to be fetch from somewhere else
    Need to find a solution
    @returns: tuple key,value
    '''
    lock.acquire()
    result = fetch_from_db(conn, key)
    if result is not None:
        lock.release()
        logger.debug("Exists in the DB: %s", result)
    else:
        # Sleep simulates a slow operation to get the data from somewhere else
        time.sleep(random.random())
        value = random_str_generator()

        logger.debug("Inserting in the DB: Key = %s :: Value = %s", key, value)
        insert_into_db(conn, key, value)
        lock.release()
        result = (key, value)
    shared_results.append(result)

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


    with Manager() as manager:
        jobs = []
        shared_results = manager.list()
        for _ in range(N):
            key = random.randint(1,10)
            p = Process(target=fetch_or_insert, args=(conn, key, shared_results, lock, ))
            jobs.append(p)
            p.start()

        for p in jobs:
            p.join()

        logger.info("fetch_or_insert returned: %s", shared_results[:])

    # DB cleanup
    with conn:
        cursor = conn.cursor()
        cursor.execute("delete from pairs")
        cursor.execute("drop table pairs")
        cursor.close()
    conn.close()