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
import tempfile
from hashlib import sha1
from pprint import pprint
from multiprocessing import Pool, Lock, Manager, Process, cpu_count


logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

N = 1000 # Number of parallel cycles

def insert_into_db(db_name, key, value):
    try:
        conn = sqlite3.connect(db_name)
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pairs VALUES (?,?)", (key,value))
        conn.close()
    except sqlite3.OperationalError as e:
        logger.error("--------- insert_into_db")
        logger.exception(e)


def fetch_from_db(db_name, key):
    try:
        conn = sqlite3.connect(db_name)
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT key,value FROM pairs WHERE key=?', (key,) )
            result = cursor.fetchone()
        conn.close()
        return result
    except sqlite3.OperationalError as e:
        logger.error("--------- fetch_from_db")
        logger.exception(e)

def fetch_or_insert(db_name, key, lock):
    '''
    The database remains loked if the object
    needs to be fetch from somewhere else
    Need to find a solution
    @returns: tuple key,value
    '''
    lock.acquire()
    result = fetch_from_db(db_name, key)
    lock.release()
    if result is not None:
        logger.debug("Exists in the DB: %s", result)
    else:
        # Sleep simulates a slow operation to get the data from somewhere else
        time.sleep(random.random())
        value = random_str_generator()
        logger.debug("Inserting in the DB: Key = %s :: Value = %s", key, value)
        lock.acquire()
        if not fetch_from_db(db_name, key):
            insert_into_db(db_name, key, value)
        lock.release()
        result = (key, value)
    return result


def show_results(value):
    logger.info("fetch_or_insert returned: %s", value)


def random_str_generator(size=6, chars=string.ascii_letters + string.digits):
    random.seed()
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == '__main__':

    with tempfile.NamedTemporaryFile(suffix=".db") as temp:

        logger.debug("Using db: %s", temp.name)

        # DB initialisation
        conn = sqlite3.connect(temp.name)
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE pairs ( key int primary key not \
                null, value text not null)''')
            conn.commit()
        except sqlite3.OperationalError as e:
            logger.error("Looks like the table pairs exist already...")
            logger.exception(e)
        conn.close()

        m = Manager()
        lock = m.Lock()

        # Pool() uses all available cores
        pool = Pool(processes=cpu_count()-1)
        # pool = Pool(processes=2,)
        for _ in range(N):
            key = random.randint(1, int(N/2))
            pool.apply_async(
                fetch_or_insert,
                (temp.name, key, lock, ),
                callback=show_results
            )


        pool.close()
        # Waits for all jobs to finish
        pool.join()

        # DB cleanup
        conn = sqlite3.connect(temp.name)
        with conn:
            cursor = conn.cursor()
            cursor.execute("delete from pairs")
            cursor.execute("drop table pairs")
        conn.close()

        logger.info("Done!")