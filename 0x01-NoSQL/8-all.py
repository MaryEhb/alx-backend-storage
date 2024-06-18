#!/usr/bin/env python3
'''8. List all documents in Python'''


def list_all(mongo_collection):
    '''
    lists all documents in a collection
    Return an empty list if no document in the collection
    '''
    return mongo_collection.find()
