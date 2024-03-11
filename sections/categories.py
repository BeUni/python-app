from pydantic import BaseModel
from mydatabase import MyDatabase
from bson import ObjectId
from model.category import Category
from datetime import datetime


class CategoriesRequest(BaseModel):
    items: list = []


def add_categories(category_request: CategoriesRequest):
    db = MyDatabase.instance()
    category_collection = db.categoryCollection
    categories = add_all_categories(items=category_request.items)
    for cate in categories:
        item = category_collection.find_one({'name': cate['name']})
        if not item:
            category_collection.insert_one(cate)
        else:
            item['name'] = cate['name']
            category_collection.update_one({"_id": ObjectId(item['_id'])}, {"$set": item})

    return {'info': 'successfully'}


def add_all_categories(items: [str]):
    categories: list = []

    for item in items:
        category = Category()
        category._id = ObjectId
        category.name = item
        category.enable = True
        category.createdAt = datetime.utcnow()
        category.updatedAt = datetime.utcnow()
        categories.append(dict(category))

    return categories
