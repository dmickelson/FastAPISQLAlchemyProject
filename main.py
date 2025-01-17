
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sql_app import models
from db import get_db, engine
import sql_app.models as models
import sql_app.schemas as schemas
from sql_app.repositories import ItemRepo, StoreRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List, Optional
from fastapi.encoders import jsonable_encoder

# Create FASTAPI Instance
app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0",)

# Create the Database
models.Base.metadata.create_all(bind=engine)

"""
A global exception handler for the FastAPI application.

This exception handler is registered with the FastAPI application to handle any exceptions that are raised during the execution of the application's routes. It provides a consistent error response format, returning a JSON response with a status code of 400 and a message that includes the failed request method, URL, and the detailed exception message.

Args:
    request (Request): The HTTP request that triggered the exception.
    err (Exception): The exception that was raised.

Returns:
    JSONResponse: A JSON response with a status code of 400 and an error message.
"""


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

# Create REST API Endpoints
# For POST, PUT, DELETE, PATCH methods use ASYNC and use AWAIT keyword to support concurrency and
# to avoid blocking the main thread to improve performance.


@app.post('/items', tags=["Item"], response_model=schemas.Item, status_code=201)
async def create_item(item_request: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create an Item and store it in the database.

    Args:
        item_request (schemas.ItemCreate): The item to create.
        db (Session): The database session.

    Returns:
        schemas.Item: The created item.

    Raises:
        HTTPException: If an item with the same name already exists.
    """
    db_item = ItemRepo.fetch_by_name(db, name=item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists!")

    return await ItemRepo.create(db=db, item=item_request)


@app.get('/items', tags=["Item"], response_model=List[schemas.Item])
def get_all_items(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Items stored in database
    """
    if name:
        items = []
        db_item = ItemRepo.fetch_by_name(db, name)
        items.append(db_item)
        return items
    else:
        return ItemRepo.fetch_all(db)


@app.get('/items/{item_id}', tags=["Item"], response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(
            status_code=404, detail="Item not found with the given ID")
    return db_item


@app.delete('/items/{item_id}', tags=["Item"])
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(
            status_code=404, detail="Item not found with the given ID")
    await ItemRepo.delete(db, item_id)
    return "Item deleted successfully!"


@app.put('/items/{item_id}', tags=["Item"], response_model=schemas.Item)
async def update_item(item_id: int, item_request: schemas.Item, db: Session = Depends(get_db)):
    """
    Update an Item stored in the database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.name = update_item_encoded['name']
        db_item.price = update_item_encoded['price']
        db_item.description = update_item_encoded['description']
        db_item.store_id = update_item_encoded['store_id']
        return await ItemRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(
            status_code=400, detail="Item not found with the given ID")


@app.post('/stores', tags=["Store"], response_model=schemas.Store, status_code=201)
async def create_store(store_request: schemas.StoreCreate, db: Session = Depends(get_db)):
    """
    Create a Store and save it in the database
    """
    db_store = StoreRepo.fetch_by_name(db, name=store_request.name)
    print(db_store)
    if db_store:
        raise HTTPException(status_code=400, detail="Store already exists!")

    return await StoreRepo.create(db=db, store=store_request)


@app.get('/stores', tags=["Store"], response_model=List[schemas.Store])
def get_all_stores(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Stores stored in database
    """
    if name:
        stores = []
        db_store = StoreRepo.fetch_by_name(db, name)
        print(db_store)
        stores.append(db_store)
        return stores
    else:
        return StoreRepo.fetch_all(db)


@app.get('/stores/{store_id}', tags=["Store"], response_model=schemas.Store)
def get_store(store_id: int, db: Session = Depends(get_db)):
    """
    Get the Store with the given ID provided by User stored in database
    """
    db_store = StoreRepo.fetch_by_id(db, store_id)
    if db_store is None:
        raise HTTPException(
            status_code=404, detail="Store not found with the given ID")
    return db_store


@app.delete('/stores/{store_id}', tags=["Store"])
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_store = StoreRepo.fetch_by_id(db, store_id)
    if db_store is None:
        raise HTTPException(
            status_code=404, detail="Store not found with the given ID")
    await StoreRepo.delete(db, store_id)
    return "Store deleted successfully!"


"""
Runs the FastAPI application on port 9000 with live reloading enabled.
"""
if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
