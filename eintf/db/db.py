from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['eintf']


def create_collection(collection_name: str):
    return db.create_collection(collection_name)


def drop_collection(collection_name: str):
    return db.drop_collection(collection_name)


def update_collection(collection_name: str, where: dict, update: dict, upsert=True):
    return db.get_collection(collection_name).update_one(where, {'$set': update}, upsert)


def get_collection(collection_name: str, where=None, key="data"):
    if where is None:
        where = {}
    if key is None:
        return db.get_collection(collection_name).find_one(where)
    return db.get_collection(collection_name).find_one(where)[key]
