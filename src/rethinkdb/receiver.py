import sys
import rethinkdb as r
import pprint
import logging

"""
Ten-minute guide with RethinkDB and Python

http://rethinkdb.com/docs/guide/python/
"""


logging.getLogger().setLevel(logging.DEBUG)

try:
    r.connect( "localhost", 28015).repl()
except r.RqlDriverError, e:
    logging.error("Is the Server running?\n%s"%e)
    sys.exit()


logging.debug("Realtime feeds:")

cursor = r.table("authors").changes().run()
for document in cursor:
    logging.debug("Listening for changes in the authors table...")
    logging.debug(pprint.pformat(document))