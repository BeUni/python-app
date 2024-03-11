from pymongo import MongoClient
import settings


class MyDatabase(object):
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance

    client = MongoClient(settings.mongodb_uri)

    db = client['hattah_db']

    userCollection = db['users']
    storeCollection = db['stores']
    categoryCollection = db['category']
    productsCollection = db['products']

    def close_db(self):
        self.client.close()
