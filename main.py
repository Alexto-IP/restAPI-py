from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from sqligther import SQLigther

app = FastAPI()
db = SQLigther('newdb.db')


class Item(BaseModel):
    id: int
    name: str
    type: str
    price: int
    count: int


@app.get('/items/get/{item_type}/all')
def get_items_by_type(item_type: str):
    res = []
    items_id = db.get_items_id_by_type(item_type)
    for item_id in items_id:
        item = {
            "id": item_id[0],
            "name": db.get_item_name(item_id[0]),
            "type": item_type,
            "price": db.get_item_price(item_id[0]),
            "count": db.get_item_count(item_id[0])
        }
        res.append(Item(**item))
    return res


@app.get('/items/get/{item_type}/{item_id}')
def get_item(item_type: str, item_id: int, response: Response):
    items_id = db.get_items_id_by_type(item_type)
    items_id = [item[0] for item in items_id]
    if item_id in items_id:
        item = {
            "id": item_id,
            "name": db.get_item_name(item_id),
            "type": item_type,
            "price": db.get_item_price(item_id),
            "count": db.get_item_count(item_id)
        }
        return Item(**item)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False


@app.get('/items/get/all')
def get_items():
    res = []
    items_id = db.get_all_items_id()
    for item_id in items_id:
        item = {
            "id": item_id[0],
            "name": db.get_item_name(item_id[0]),
            "type": db.get_item_type(item_id[0]),
            "price": db.get_item_price(item_id[0]),
            "count": db.get_item_count(item_id[0])
        }
        res.append(Item(**item))
    return res


@app.get('/items/get/{item_id}')
def get_item(item_id: int, response: Response):
    items_id = db.get_all_items_id()
    items_id = [item[0] for item in items_id]
    if item_id in items_id:
        item = {
            "id": item_id,
            "name": db.get_item_name(item_id),
            "type": db.get_item_type(item_id),
            "price": db.get_item_price(item_id),
            "count": db.get_item_count(item_id)
        }
        return Item(**item)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False


@app.delete('/items/delete/{item_id}')
def delete_item(item_id: int, response: Response):
    items_id = db.get_all_items_id()
    items_id = [item[0] for item in items_id]
    if item_id in items_id:
        db.delete_item(item_id)
        return True
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False


@app.post('/item/add/{item_id}')
def add_item(item_id: int, item: Item, response: Response):
    items_id = db.get_all_items_id()
    if item_id in items_id:
        response.status_code = status.HTTP_302_FOUND
        return False
    else:
        db.add_item(item_id, item.name, item.type, item.count, item.price)
        return True


@app.put('/item/update/{item_id}')
def update_item(item_id: int, item: Item, response: Response):
    items_id = db.get_all_items_id()
    items_id = [item[0] for item in items_id]
    if item_id in items_id:
        db.update_item_info(item_id, item.name, item.type, item.count, item.price)
        return True
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
