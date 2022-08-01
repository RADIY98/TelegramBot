import asyncio
import json
from datetime import datetime
import requests
import base_names
from fastapi import FastAPI
from jsonschema import validate
from .KeyBoard import KeyBoard
from .common import load_schema

app = FastAPI()
STARTED_TIME = datetime.now()
OFFSET = 579187220


# TODO ПРИ ПОДКЛЮЧЕНИЕ К БОТУ СДЕЛАТЬ ПРОКИДЫВАНИЕ КНОПОК

@app.get('/')
async def loong_pool_request():
    while True:
        await asyncio.sleep(30)
        get_updates()


@app.get(r"/bot")
def get_updates():
    global OFFSET

    update_id = None
    method = '/getUpdates'
    params = {'limit': 100, 'offset': OFFSET + 1}
    resp = requests.get(base_names.URL + base_names.TOKEN + method, params)
    result_list = resp.json()['result']
    if result_list:
        for record in result_list:
            validate(instance=record, schema=load_schema("response"))
            msg = record.get("message")
            text = msg.get("text")

            chat = msg.get("chat")
            update_id = record.get("update_id")
            client_id = chat.get("id")

            if text == "/start":
                send_message(chat_id=client_id, text=text,
                             reply_markup=json.dumps({'keyboard': KeyBoard().get_keyboard()}))

                # send_message(chat_id=client_id, text="Default response")  
            send_message(chat_id=client_id, text="This is message for you only")
        if update_id is not None:
            OFFSET = update_id

    return result_list


@app.put("/bot")
def send_message(**kwargs):
    """
    Метод отправки сообщений
    :return:
    """
    method = '/sendMessage'
    response = requests.post(base_names.URL + base_names.TOKEN + method, data=kwargs)

    return response
