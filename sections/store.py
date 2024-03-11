from pydantic import BaseModel
from mydatabase import MyDatabase
from bson import ObjectId
from model.store import Store
from datetime import datetime


class StoreRequest(BaseModel):
    name: str
    type: str
    gstIn: str
    image: str


def add_store(store_request: StoreRequest, email: str):
    db = MyDatabase.instance()
    store_collection = db.storeCollection
    user = db.userCollection.find_one({'email': email})
    if user:
        store = new_store(name=store_request.name, store_type=store_request.type, gst_in=store_request.gstIn,
                          user_id=str(user['_id']), image_url='')
        inserted_store = store_collection.insert_one(store)
        item = store_collection.find_one({'_id': ObjectId(inserted_store.inserted_id)})
        if item is not None:
            return {'info': 'successfully store added'}
        else:
            return {'info': 'store is not added'}


def new_store(name: str, store_type: str, gst_in: str, user_id: str, image_url: str):
    store = Store()
    store._id = ObjectId
    store.name = name
    store.type = store_type
    store.gstIn = gst_in
    store.image = image_url
    store.enable = True
    store.userId = user_id
    store.createdAt = datetime.utcnow()
    store.updatedAt = datetime.utcnow()
    return dict(store)
