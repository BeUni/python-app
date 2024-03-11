from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class Category(BaseModel):
    _id = ObjectId
    name: str = Field(None)
    enable: bool = Field(None)
    updatedAt: datetime = Field(None)
    createdAt: datetime = Field(None)
