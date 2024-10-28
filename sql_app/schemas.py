"""
This module defines the data models/schemas for the SQL application using Pydantic.

The `ItemBase` class defines the common attributes for an item, including the name, price, description, and the store ID.
The `ItemCreate` class inherits from `ItemBase` and is used for creating new items.
The `Item` class inherits from `ItemBase` and adds an `id` attribute. It also sets `orm_mode=True` to enable reading the data from an ORM model.

The `StoreBase` class defines the common attributes for a store, including the name.
The `StoreCreate` class inherits from `StoreBase` and is used for creating new stores.
The `Store` class inherits from `StoreBase`, adds an `id` attribute, and has a list of `Item` objects associated with the store. It also sets `orm_mode=True` to enable reading the data from an ORM model.
"""
from typing import List, Optional

from pydantic import BaseModel

# Define the data models/schema using Pydantic
# Base classes contain the common attributes of the models for creation or reading.
# Create classescontain the Base attributes and any needed attributes for creation.
# Item and Store classes contain the Base attributes and any needed attributes for reading.
# Set the orm_mode to True to enable reading the data even when it is not a dict,
# but an ORM model (or any other arbitrary object with attributes).


class ItemBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    store_id: int

#


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class StoreBase(BaseModel):
    name: str


class StoreCreate(StoreBase):
    pass


class Store(StoreBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True
