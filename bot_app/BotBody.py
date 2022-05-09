import asyncio
import os, sys
from datetime import datetime
import enum
import requests
from bot_app import Application
import base_names
from bot_app.KeyBoard import KeyBoard

STARTED_TIME = datetime.now()
OFFSET = 579187220
# PATH = "last_update.txt"
# with open(PATH, "r") as f:
#     last_updated_id = f.readline()
#     OFFSET = int(last_updated_id)


app = Application({}).create_app()

# TODO ПРИ ПОДКЛЮЧЕНИЕ К БОТУ СДЕЛАТЬ ПРОКИДЫВАНИЕ КНОПОК

@app.get('/')
async def loong_pool_request():
    while True:
        await asyncio.sleep(30)
        get_updates()


@app.get("/bot")
def get_updates():
    global OFFSET

    update_id = None
    method = '/getUpdates'
    params = {'limit': 100, 'offset': OFFSET + 1}
    resp = requests.get(base_names.URL + base_names.TOKEN + method, params)
    result_list = resp.json()['result']
    if result_list:
        for record in result_list:
            msg = record.get("message")
            text = msg.get("text")

            # time_posted = datetime.utcfromtimestamp(msg.get('date'))
            chat = msg.get("chat")
            update_id = record.get("update_id")
            client_id = chat.get("id")
            import pydevd_pycharm
            pydevd_pycharm.settrace('localhost', port=2005, stdoutToServer=True, stderrToServer=True)
            if text == "/start" or True:
                send_message(chat_id=client_id, text=text, reply_markup={'inline keyboard': KeyBoard().get_keyboard()})
                # send_message(chat_id=client_id, text="Default response")
            # send_message(client_id, "This is message for you only")
        if update_id is not None:
            # with open(PATH, 'w') as file:
            #     file.write(update_id)
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
