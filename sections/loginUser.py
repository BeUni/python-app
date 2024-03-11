from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi import Depends, HTTPException

import utils
from model.user import User
from mydatabase import MyDatabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class LoginRequest(BaseModel):
    email: str
    password: str


class StoreUserRequest(BaseModel):
    email: str
    name: str
    profileImage: str


class CreatePasswordStoreUser(BaseModel):
    password: str


def create_store_user(login_request: StoreUserRequest):
    db = MyDatabase.instance()
    user_collection = db.userCollection
    user = find_user(login_request.email)

    if not user:
        new_user = create_user(login_request.email, login_request.name)
        inserted_item = user_collection.insert_one(new_user)
        item = user_collection.find_one({'_id': ObjectId(inserted_item.inserted_id)})
        token = utils.create_access_token({'id': str(item['_id']), 'email': item['email']})
        return {'access_token': token}
    else:
        return dict({"error": "User already exist"})


def find_user(email):
    db = MyDatabase.instance()
    user_collection = db.userCollection
    user = user_collection.find_one({"email": email})
    if user:
        return user


def create_user(email, name):
    user = User()
    user._id = str(ObjectId())
    user.email = email
    user.name = name
    return dict(user)


def create_password_store_user(create_password: CreatePasswordStoreUser, email: str):
    user = find_user(email=email)
    db = MyDatabase.instance()
    user_collection = db.userCollection
    hashed_password = utils.hash_pass(create_password.password)
    user['password'] = hashed_password
    if user:
        user_collection.update_one(
            {"_id": ObjectId(user['_id'])}, {"$set": user}
        )


def verify_user(login_request):
    user = find_user(login_request.email)
    if user:
        verified = utils.verify_pass(login_request.password, user['password'])
        if verified:
            token = utils.create_access_token({'id': str(user['_id']), 'email': user['email']})
            return {'access_token': token}
        else:
            raise HTTPException(
                status_code=401,
                detail="Please enter valid "
            )
    else:
        return {'info': 'user is not registered'}
