'''

@author: leal

Stores ipython notebooks in mongodb 

Size limit: 16 megabytes per file!

DB can be browsed with : https://robomongo.org/
'''
import os
import json
import gridfs

from pymongo import MongoClient
from glob import iglob
from pprint import pprint

def mongodb_example():
    '''
    Creates a collection: files
    '''
    client = MongoClient()
    db = client["dbtest"]

    # Not needed!
    #db.create_collection( name="files" )

    # Stores all files in a directory
    object_ids = []
    for fname in iglob(os.path.expanduser('~/git/HFIRSANSReduction/src/*.ipynb')):
        with open(fname) as fin:
            ipynb_contents = json.load(fin)
            object_id = db.files.insert(ipynb_contents)
            object_ids.append(object_id)

    # Retrieve by object ID
    for object_id in object_ids:
        pprint(db.files.find_one({"_id": object_id})["metadata"])

def gridfs_example():
    '''
    For files > 16MB
    It creates binary chunks and stores metadata
    creates a collection: fs
    fs will have: fs.files and fs.chunks
    '''
    client = MongoClient()
    db = client["dbtest"]
    fs = gridfs.GridFS(db)

    filenames = iglob(os.path.expanduser('~/git/HFIRSANSReduction/src/*.ipynb'))
    object_ids = []
    for fname in filenames:
        # The file must be open in binary
        with open(fname,"rb") as fin:
            object_id = fs.put(fin, filename=fname)
            object_ids.append(object_id)

    # Retrieve by object ID
    for object_id in object_ids:
        obj = fs.get(object_id)
        print(obj)
        print(obj.filename)
        # To read the file contents: obj.read() 

    # Retrieve by object ID (MongoDB way!)
    for object_id in object_ids:
        pprint(fs.find_one({"_id": object_id}))

    # If we run this script multiple times the same file will be inserted 
    # multiple times. this finds all the cocurences and order by upload date
    files_found_cursor = db.fs.files.find({"filename": fname}).sort("uploadDate", 1)
    for cursor in files_found_cursor:
        pprint(cursor)

    
if __name__ == '__main__':
    mongodb_example()
    gridfs_example()
