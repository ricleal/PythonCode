import sqlite3
import sys
import random
import string
import logging
from hashlib import sha1
from pprint import pprint

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DB(object):
    """
    Pair Key Value in SQLite
    Table is called: pairs
    """

    def __init__(self,dbname):
        logger.info("Using db %s"%dbname)
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def create_table(self):
        try:
            self.cursor.execute('''CREATE TABLE pairs ( key text primary key not null, value text not null)''')
            self.conn.commit()
        except Exception, e:
            logger.exception(e)

    def put(self, key, value):
        key_hash = self._hash_text(key)
        self.cursor.execute("INSERT INTO pairs VALUES (?,?)", (key_hash,value))
        self.conn.commit()

    def get(self,key):
        """
        Todo: protect against multiple results which will never happen
        """
        key_hash = self._hash_text(key)
        t = (key_hash,)
        self.cursor.execute('SELECT value FROM pairs WHERE key=?', t)
        res = self.cursor.fetchone()
        return res[0] if res is not None else None

    def dump(self):
        ret = []
        for row in self.cursor.execute('SELECT key,value FROM pairs'):
            ret.append(row)
        return ret

    def clean_table(self):
        self.cursor.execute("delete from pairs")
        self.conn.commit()

    def _hash_text(self, text):
        h = sha1(text)
        digest = h.hexdigest()
        logger.debug("Hash: %s = %s"%(text,digest))
        return digest

    def __del__(self):
        logger.info("Closing connection...")
        self.conn.close()

def random_str_generator(size=6, chars=string.ascii_letters + string.digits):
    random.seed()
    return ''.join(random.choice(chars) for _ in range(size))

def test():

    db = DB('test1.db')
    db.create_table()
    db.clean_table()

    for _ in range(3):
        key = "p1=%s,p2=%s,p3=%s,p4=%s"%(random_str_generator(2),
        random_str_generator(3),random_str_generator(4),random_str_generator(5))
        value = "/tmp/tmp_%s.nxs"%random_str_generator()
        db.put(key,value)

    dump = db.dump()
    pprint(dump)

    key_hashed = dump[-1][0] # Will return none
    print "Result for key", key_hashed, "-->", db.get(key_hashed)
    key_hashed = key
    print "Result for key", key_hashed, "-->", db.get(key_hashed)


if __name__ == "__main__":
    test()
