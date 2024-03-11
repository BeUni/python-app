from pydantic import BaseModel, Field
from bson import ObjectId


class User(BaseModel):
    _id: ObjectId
    name: str = Field(None)
    email: str = Field(None)
    password: str = Field(None)
    gender: str = Field(None)


