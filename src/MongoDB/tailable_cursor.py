#!/usr/bin/python

'''
Created on Oct 31, 2013

@author: leal

Adapted from:
http://stackoverflow.com/questions/10321140/using-pymongo-tailable-cursors-dies-on-empty-collections

This checks for changes in a capped collection.
When it changes print the oldest element in this collection.

'''


import threading
import datetime

import sys
import time
import pymongo

maxCappedTest  = 10

MONGO_SERVER = "127.0.0.1"
MONGO_DATABASE = "mdatabase"
MONGO_COLLECTION = "mcollection"

    
mongodb = pymongo.Connection(MONGO_SERVER, 27017)
database = mongodb[MONGO_DATABASE]

# if MONGO_COLLECTION in database.collection_names():
#     database[MONGO_COLLECTION].drop()


if MONGO_COLLECTION not in database.collection_names():
    print "creating capped collection"
    database.create_collection(
      MONGO_COLLECTION,
      size=100000,
      max=maxCappedTest,
      capped=True)

collection = database[MONGO_COLLECTION]



# Get a tailable cursor for our looping fun
cursor = collection.find({},await_data=True,tailable=True)

global keepAlive
keepAlive = True

def chechForInsertions(collection,cursor):
    while keepAlive:
        if collection.count() == 0:
            time.sleep(1)
        else :
            while cursor.alive and keepAlive:
                try:
                    message = cursor.next()
                    print 'Reading ->', message
                    oldestElementCursor = collection.find().sort([("$natural", pymongo.ASCENDING)]).limit(1);
                    #print 'Oldest ->', [(i['key'],i['created']) for i in oldestElementCursor], 'of', collection.count()
                    print 'Oldest ->', oldestElementCursor[0]
                except StopIteration:
                    time.sleep(0.5)



t = threading.Thread(target=chechForInsertions, args=(collection,cursor,))
t.start()

try:    
    for i in range(maxCappedTest*2):
        time.sleep(1)
        data = {"key" : "%d"%i,  "created" : "%s"%(datetime.datetime.utcnow())}
        print '**** Inserting ->', data
        collection.insert(data)

except KeyboardInterrupt:
        print "trl-C Ya!"
        keepAlive = False
        #sys.exit(0)

keepAlive = False
t.join()

print "and we're out"

