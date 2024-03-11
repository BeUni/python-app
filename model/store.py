from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class Store(BaseModel):
    _id = ObjectId
    name: str = Field(None)
    type: str = Field(None)
    gstIn: str = Field(None)
    image: str = Field(None)
    enable: bool = Field(None)
    userId: str = Field(None)
    updatedAt: datetime = Field(None)
    createdAt: datetime = Field(None)

