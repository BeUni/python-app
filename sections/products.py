from pydantic import BaseModel
from mydatabase import MyDatabase
from bson import ObjectId
from model.product_model import Product
from datetime import datetime


class ProductRequest(BaseModel):
    name: str
    quantity: int
    quantity_type: str
    description: str
    category: str
    mrp: float
    revised_mrp: float
    image: list


def get_product_category_info():
    db = MyDatabase.instance()
    category_collection = db.categoryCollection
    categories = category_collection.find({'enable': True})
    cate: list = []
    for item in categories:
        cate.append(item['name'])

    return {'categories': cate, 'quantity_type': ['kg', 'gm', 'pc', 'l', 'ml']}


def add_product(product_request: ProductRequest):
    db = MyDatabase.instance()
    product_collection = db.productsCollection
    product_item = new_product(product_request=product_request)
    item = product_collection.insert_one(product_item)
    if item is not None:
        return {'info': 'product add successfully'}
    else:
        return {'info': 'product not added'}


def new_product(product_request: ProductRequest):
    product = Product()
    product._id = ObjectId
    product.name = product_request.name
    product.quantity = product_request.quantity
    product.quantity_type = product_request.quantity_type
    product.description = product_request.description
    product.mrp = product_request.mrp
    product.revised_mrp = product_request.revised_mrp
    product.category = product_request.category
    product.image = product_request.image
    product.enable = True
    product.updatedAt = datetime.utcnow()
    product.createdAt = datetime.utcnow()

    return dict(product)
