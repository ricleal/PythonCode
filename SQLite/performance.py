from __future__ import print_function, with_statement

import sqlite3
import sys
import time
import random
import string
import logging
import tempfile
import time


logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info("Took {:.3} us".format(delta*10e3))

if __name__ == '__main__':

    with tempfile.NamedTemporaryFile(suffix=".db") as temp:

        logger.debug("Using db: %s", temp.name)

        tic()
        # DB initialisation
        conn = sqlite3.connect(temp.name)
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE pairs ( key int primary key not null, value text not null)''')
            conn.commit()
        except sqlite3.OperationalError as e:
            logger.error("Looks like the table pairs exist already...")
            logger.exception(e)
        conn.close()
        toc()

        tic()
        conn = sqlite3.connect(temp.name)
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pairs VALUES (?,?)", (1, "foo"))
        conn.close()
        toc()


        conn = sqlite3.connect(temp.name)
        tic()
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pairs VALUES (?,?)", (2, "foo2"))
        toc()
        tic()
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pairs VALUES (?,?)", (3, "foo2"))
            cursor.close()
        toc()
        tic()
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pairs VALUES (?,?)", (4, "foo2"))
        toc()



