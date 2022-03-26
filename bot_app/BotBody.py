from typing import Optional
from pydantic import BaseModel
import requests
import base_names
from bot_app import Application


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


app = Application({}).create_app()


@app.get('/')
def home():
    return 'Welcome to the beginning'


@app.get("/items/{item_id}")
def read_items(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_items(item_id: int, item: Item):
    return {"item_name": item.name,
            "item_id": item_id}

@app.get("/bot")
def get_updates(timeout=None, offset=30):
    method = '/getUpdates'
    params = {'timeout': timeout, 'offset': offset}
    resp = requests.get(base_names.URL + base_names.TOKEN + method, params)
    result_json = resp.json()['result']
    for record in result_json:
        msg = record.get("message")
        chat = msg.get("chat")
        client_id = chat.get("id")
        send_message(client_id, "This is message for you only")

    return result_json


@app.put("/bot")
def send_message(chat, text):
    """
    Метод отправки сообщений
    :return:
    """
    params = {"chat_id": chat, "text": text}
    method = '/sendMessage'
    response = requests.post(base_names.URL + base_names.TOKEN + method, data=params)

    return response
