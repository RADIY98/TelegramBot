import asyncio
import json
import os

from datetime import datetime

import requests
from fastapi import APIRouter
from bot_app.KeyBoard import KeyBoard
from .validation import Response
from . import base_names

router = APIRouter()
STARTED_TIME = datetime.now()
path = os.path.realpath("bot_app")

# TODO ПРИ ПОДКЛЮЧЕНИЕ К БОТУ СДЕЛАТЬ ПРОКИДЫВАНИЕ КНОПОК

@router.get('/')
async def loong_pool_request():
    while True:
        await asyncio.sleep(3)
        get_updates()


@router.get(r"/bot")
def get_updates():

    with open(f"{path}\global_update_id.txt", "r") as f:
        global_last_update = int(f.readline().split()[0])

    method = '/getUpdates'
    params = {'limit': 100, "offset": global_last_update + 1}
    update_id = global_last_update
    resp = requests.get(base_names.URL + base_names.TOKEN + method, params)
    result_list = resp.json()['result']

    if result_list:
        for record in result_list:
            Response.parse_obj(record)
            msg = record.get("message")
            text = msg.get("text")

            chat = msg.get("chat")
            update_id = record.get("update_id")
            client_id = chat.get("id")

            if text == "/start":
                send_message(
                    chat_id=client_id,
                    text=text,
                    reply_markup=json.dumps({'keyboard': KeyBoard(base_names.START_KEYBOAD).get_keyboard()})
                )
            elif text == base_names.StartButtonsNames.start:
                send_message(
                    chat_id=client_id,
                    text=text,
                    reply_markup=json.dumps({'keyboard': KeyBoard(base_names.TRAIN).get_keyboard()})
                )
            elif text == base_names.back:
                send_message(
                    chat_id=client_id,
                    text=text,
                    reply_markup=json.dumps({'keyboard': KeyBoard(base_names.TRAIN).get_keyboard()})
                )
            elif text in base_names.TRAIN:
                send_message(
                    chat_id=client_id,
                    text=text,
                    reply_markup=json.dumps({'keyboard': KeyBoard(base_names.EXERCISE).get_keyboard()})
                )
            elif text in base_names.EXERCISE:
                send_message(
                    chat_id=client_id,
                    text=text,
                    reply_markup=json.dumps({'keyboard': KeyBoard(base_names.START_TRAIN).get_keyboard()})
                )
            elif text == base_names.StartButtonsNames.change:
                pass
            elif text == base_names.StartButtonsNames.statistic:
                pass
            elif text == base_names.ExerciseButtonsNames.counts:
                send_message(
                    chat_id=client_id,
                    text=text,
                    reply_markup=json.dumps({'keyboard': KeyBoard(base_names.START_TRAIN).get_keyboard()})
                )
                # Добавить метод на запись кол-ва подходов в бд
            elif text == base_names.ExerciseButtonsNames.set_weight:
                send_message(
                    chat_id=client_id,
                    text=text,
                    reply_markup=json.dumps({'keyboard': KeyBoard(base_names.START_TRAIN).get_keyboard()})
                )
                # Добавить метод на запись кол-ва подходов в бд
            elif text == base_names.ExerciseButtonsNames.end:
                send_message(
                    chat_id=client_id,
                    text=text,
                    reply_markup=json.dumps({'keyboard': KeyBoard(base_names.EXERCISE).get_keyboard()})
                )

            send_message(chat_id=client_id, text=f"{global_last_update}, {update_id}")

        open(f'{path}\global_update_id.txt', 'w').close()
        with open(f"{path}\global_update_id.txt", "w") as const:
            const.write(str(update_id))

    return result_list


@router.put("/bot")
def send_message(**kwargs):
    """
    Метод отправки сообщений
    :return:
    """
    method = '/sendMessage'
    response = requests.post(base_names.URL + base_names.TOKEN + method, data=kwargs)

    return response
