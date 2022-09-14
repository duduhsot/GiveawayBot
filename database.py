from giveaway import Giveaway
from pymongo import MongoClient
import pymongo

CONNECTION_STRING = 'mongodb+srv://user:user@cluster0.fnguq3m.mongodb.net/?retryWrites=true&w=majority'

def get_DB():
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)
    return client['giveaways']

def get_collection():
    dbname = get_DB()
    collection_name = dbname["giveaways"]

def insert_giveaway(giveaway :Giveaway):
    dbname = get_DB()
    collection_name = dbname["giveaways"]

    item_1 = {
        "author": giveaway.author,
        "authorNick": giveaway.authorNick,
        "name": giveaway.name,
        "description": giveaway.description,
        "numberOfWinners": giveaway.numberOfWinners,
        "id": str(giveaway.id),
        "subscribers": giveaway.subscribers,
        "ended": giveaway.ended,
        "winners": giveaway.winners,
        "photoId": giveaway.photoId,
    }

    collection_name.insert_one(item_1)