from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

inventory = {}

# making routes in fastapi
@app.get("/")
def home():
    return {"Data" : "YOOOOO"}

@app.get("/about")
def about():
    return {"Data" : "About"}

# path parameters
@app.get("/item/{item_id}")
def get_item(item_id: int): # defining the type
    return inventory[item_id]

# u can take multiple path parameters
@app.get("/item/{item_id}/{name}")
def get_item_with_name(item_id: int, name: str): # defining the type
    return inventory[item_id]

# path function from fastapi
@app.get("/item-info/{item_id}")     # ... is a placeholder for default
def get_item_details(item_id: int = Path(..., description = "The id of the item you would like to view")): # defining the type
    return inventory[item_id]

# query parameters
@app.get("/get-by-name")
def get_item_by_name(name: Optional[str] = ...): # if it is option remember to the ...
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code = 404, detail = "Item name not found") # error handling
# http://127.0.0.1:8000/get-by-name?name=milk is an example of how you would use the endpoint

# class for item
class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

# POST in FastAPI
@app.post("/create-item/{item_id}")
def create_item(item: Item, item_id: int):
    if item_id in inventory:
        raise HTTPException(status_code = 400, detail = "Item id already exists") # error handling
    inventory[item_id] = item
    return inventory[item_id]

# class for update item
class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

# PUT in FastAPI
@app.put("/update-item/{item_id}")
def update_item(item: UpdateItem, item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code = 404, detail = "Item name not found") # error handling
    if item.name != None:
        inventory[item_id].name = item.name 
    if item.price != None:
        inventory[item_id].price = item.price 
    if item.brand != None:
        inventory[item_id].brand = item.brand 

    return inventory[item_id]

# DELETE in FastAPI
@app.delete("/delete-item")
def delete_item(item_id: int = Path(..., description = "id of item to delete")):
    if item_id not in inventory:
        raise HTTPException(status_code = 404, detail = "Item name not found") # error handling
    del inventory[item_id]
    return {"Success" : "Item Deleted"}