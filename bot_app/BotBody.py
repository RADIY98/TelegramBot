import asyncio
from datetime import datetime
import enum
import requests
from bot_app import base_names, Application

STARTED_TIME = datetime.now()
with open("last_update", "r") as f:
    last_updated_id = f.readline()
    OFFSET = int(last_updated_id)

class TelegramMethods(enum.Enum):
    get_updates = '/getUpdates'
    send_message = '/sendMessage'
    setWebhook = "/setWebhook"


app = Application({}).create_app()

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
    params = {'limit': 100, 'offset': OFFSET+1}
    resp = requests.get(base_names.URL + base_names.TOKEN + method, params)
    result_list = resp.json()['result']
    if result_list:
        for record in result_list:
            msg = record.get("message")
            # time_posted = datetime.utcfromtimestamp(msg.get('date'))
            chat = msg.get("chat")
            client_id = chat.get("id")
            send_message(client_id, "This is message for you only")
            update_id = record.get("update_id")
        if update_id is not None:
            OFFSET = update_id

    return result_list


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
