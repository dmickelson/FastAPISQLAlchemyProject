"""
This module defines the database models for the SQL application.

The `Item` model represents an item in the application, with fields for the item name, price, description, and the ID of the store the item belongs to.

The `Store` model represents a store in the application, with a field for the store name. The `items` field on the `Store` model is a relationship that allows access to all the items belonging to that store.
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base


class Item(Base):
    # Define item table in database
    __tablename__ = "items"

    # Define the columns of the table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True, index=True)
    price = Column(Float(precision=2), nullable=False)
    description = Column(String(200))
    # Define a FK relationship between Item and Store tables
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)

    # Helper print function
    def __repr__(self):
        return 'ItemModel(name=%s, price=%s,store_id=%s)' % (self.name, self.price, self.store_id)


class Store(Base):

    # Define store table in database
    __tablename__ = "stores"
    # Define the columns of the table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True)

    # Define  the 'Relationship' join between Store and Item tables
    items = relationship(
        "Item", primaryjoin="Store.id == Item.store_id", cascade="all, delete-orphan")

    def __repr__(self):
        return 'Store(name=%s)' % self.name
