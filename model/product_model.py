from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class Product(BaseModel):
    name: str = Field(None)
    quantity: int = Field(None)
    quantity_type: str = Field(None)
    description: str = Field(None)
    mrp: float = Field(None)
    revised_mrp: float = Field(None)
    category: str = Field(None)
    image: list = Field(None)
    enable: bool = Field(None)
    updatedAt: datetime = Field(None)
    createdAt: datetime = Field(None)

