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

# create table:
try:
    out = r.db("test").table_create("authors").run()
    logging.debug(out)
except r.RqlRuntimeError, e:
    logging.error("Error creating authors table:\n%s"%e)

# Insert data
# out = r.table("authors").insert([
#     { "name": "William Adama", "tv_show": "Battlestar Galactica",
#       "posts": [
#         {"title": "Decommissioning speech", "content": "The Cylon War is long over..."},
#         {"title": "We are at war", "content": "Moments ago, this ship received..."},
#         {"title": "The new Earth", "content": "The discoveries of the past few days..."}
#       ]
#     },
#     { "name": "Laura Roslin", "tv_show": "Battlestar Galactica",
#       "posts": [
#         {"title": "The oath of office", "content": "I, Laura Roslin, ..."},
#         {"title": "They look like us", "content": "The Cylons have the ability..."}
#       ]
#     },
#     { "name": "Jean-Luc Picard", "tv_show": "Star Trek TNG",
#       "posts": [
#         {"title": "Civil rights", "content": "There are some words I've known since..."}
#       ]
#     }
# ]).run()
# logging.debug(pprint.pformat(out))

logging.debug("Retrieve documents")
cursor = r.table("authors").run()
for document in cursor:
    logging.debug(pprint.pformat(document))

logging.debug("Filter documents based on a condition")
cursor = r.table("authors").filter(r.row["name"] == "William Adama").run()
for document in cursor:
    logging.debug(pprint.pformat(document))

logging.debug("Let's use filter again to retrieve all authors who have more than two posts:")
cursor = r.table("authors").filter(r.row["posts"].count() > 2).run()
for document in cursor:
    logging.debug(pprint.pformat(document))
    
logging.debug("Retrieve documents by primary key")
document = r.db('test').table('authors').get('029418c4-6568-4189-9494-46220c61f69c').run()
logging.debug(pprint.pformat(document))

logging.debug("Update documents")
out = r.table("authors").update({"type": "fictional"}).run()
logging.debug(pprint.pformat(out))

logging.debug("Update documents with filter")
out = r.table("authors").filter(r.row['name'] == "William Adama").update({"rank": "Admiral"}).run()
logging.debug(pprint.pformat(out))

logging.debug("The update command allows changing existing fields in the document, as well as values inside of arrays.")
out = r.table('authors').filter(r.row["name"] == "Jean-Luc Picard").update({"posts": r.row["posts"].append({
        "title": "Shakespeare",
        "content": "What a piece of work is man..."})
    }).run()
logging.debug(pprint.pformat(out))

logging.debug("Delete documents")
out = r.table("authors").filter( r.row["posts"].count() < 3 ).delete().run()
logging.debug(pprint.pformat(out))


 
