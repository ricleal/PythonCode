'''

Sqlite with multiple processes

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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


DB = "/tmp/test.db"
conn = sqlite3.connect(DB)


def insert_into_db(conn, key, value):
    time.sleep(random.random())
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pairs VALUES (?,?)", (key,value))
            cursor.close()
    except sqlite3.OperationalError as e:
        logger.exception(e)


def fetch_from_db(conn, key):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT key,value FROM pairs WHERE key=?', (key,) )
            result = cursor.fetchone()
            cursor.close()
        return result
    except sqlite3.OperationalError as e:
        logger.exception(e)

def fetch_or_insert(conn, key):
    value = random_str_generator()
    logger.info("Key = %s :: Value = %s", key, value)

    result = fetch_from_db(conn, key)
    if result is not None:
        logger.info("Exists in the DB = %s", result)
    else:
        insert_into_db(conn, key, value)

def random_str_generator(size=6, chars=string.ascii_letters + string.digits):
    random.seed()
    return ''.join(random.choice(chars) for _ in range(size))


# DB initialisation
try:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE pairs ( key int primary key not null, value text not null)''')
    conn.commit()
    cursor.close()
except sqlite3.OperationalError as e:
    logger.error("Looks like the table pairs exist already,,,")
    logger.exception(e)


for _ in range(10):
    key = random.randint(1,10)
    fetch_or_insert(conn, key)


with conn:
    cursor = conn.cursor()
    cursor.execute("delete from pairs")
    cursor.execute("drop table pairs")
    cursor.close()

conn.close()