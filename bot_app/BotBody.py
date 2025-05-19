import asyncio
import json
from fastapi.responses import JSONResponse
import os

from datetime import datetime

import requests
from fastapi import APIRouter

from .KeyBoard import KeyBoard
from .utils import parse_file
from .database import insert, select, delete, update
from .operation.train import TrainOperation
from .schemas.Response import Msg
from .operation.base import BaseOperation
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


@router.post(r"/bot")
def get_updates(response_list):
    """
    Метод получения обновлений
    """
    text_msg = None
    key_board = None
    # response_list = _get_http_request()
    print(response_list)
    if response_list:
        client_data = select.get_clients_update_id(
            [record.get("message").get("chat").get("id") for record in response_list]
        )

        for record in response_list:
            msg: Msg = Msg(record.get("message"))
            client_id = msg.chat.id
            update_id = record.get("update_id")
            print(update_id)

            if not client_data.get(client_id):
                insert.insert_client(msg, update_id)

            elif update_id <= client_data.get(client_id):
                continue
            client_status = select.get_client_status(client_id)

            trains = select.get_all_trains_for_keyboard(client_id)
            if client_status:
                text_msg, key_board = BaseOperation().call_method(client_id, client_status, msg)
            else:
                if msg.text == "/start":
                    text_msg = msg.text
                    key_board = base_names.StartButtons.buttons_array
                    insert.insert_client(msg, update_id)
                elif msg.text == base_names.MAIN_MENU:
                    text_msg = msg.text
                    key_board = base_names.StartButtons.buttons_array

                elif msg.text == base_names.StartButtons.set_trains:
                    text_msg = base_names.LETS_SET_TRAIN_FROM_LIST
                    key_board = base_names.TrainSettingsButton.buttons_array

                elif msg.text == base_names.TrainSettingsButton.delete:
                    text_msg = msg.text
                    key_board = trains
                    update.update_client_status(client_id, base_names.TrainStatus.DELETE)

                elif msg.text == base_names.TrainSettingsButton.change:
                    text_msg = msg.text
                    key_board = trains
                    update.update_client_status(client_id, base_names.TrainStatus.CHANGE)

                elif msg.text == base_names.TrainSettingsButton.create:
                    text_msg = base_names.ENTER_TRAIN_NAME
                    key_board = base_names.StartButtons.buttons_array
                    update.update_client_status(client_id, base_names.TrainStatus.CREATE)

                elif msg.text == base_names.StartButtons.trains:
                    if trains:
                        text_msg = base_names.CHOOSE_TRAIN_FROM_LIST
                        key_board = trains
                    else:
                        text_msg = base_names.LETS_CREATE_TRAIN
                        key_board = None

                elif msg.text in trains:
                    update.update_client_selected_entity(client_id, msg.text)
                    update.update_client_status(client_id, base_names.EXERCISE_READ_STATUS)
                    train_id = select.get_client_selected_entity(client_id)
                    key_board = select.all_exercise_for_keyboard(train_id)
                    text_msg = base_names.SELECTED_TRAIN.format(TrainOperation(client_id).read(train_id))
                elif msg.text == base_names.StartButtons.statistic:
                    pass
                elif msg.document is not None:
                    file = __download_file(msg.document)
                    train_obj = parse_file(file)
                    delete.delete_all_trains(client_id)
                    for train_name, train in train_obj.items():
                        insert.insert_train(train_name, client_id, train)
            if text_msg is not None:
                print(f"Keyboard - {key_board}")
                print(f"Text_msg - {text_msg}")

                send_message(
                    chat_id=client_id,
                    text=text_msg,
                    reply_markup=json.dumps(
                        {'keyboard': KeyBoard(key_board).get_keyboard()})
                )

            res = update.update_client_last_update(client_id, update_id)
            # print(res)
            # send_message(chat_id=client_id, text=f"{client_id}, {update_id}")

            return JSONResponse(
                content={
                    "ok": True,
                    "chat_id": client_id,
                    "text": text_msg,
                    "reply_markup": json.dumps({'keyboard': KeyBoard(key_board).get_keyboard()})
                }
            )

    return JSONResponse(
        content={
            "ok": True
        }
    )

def _get_http_request() -> dict:
    """
    Получим данные от ТГ
    """
    method = '/getUpdates'
    params = {'limit': 100, "offset": base_names.global_id + 1}
    resp = requests.get(
        base_names.URL + base_names.TOKEN + method,
        params
    )
    print(f"ALARM - {resp.json().get('result')}")
    if resp.json().get('result'):
        result_list = resp.json()['result']
    else:
        result_list = {}

    return result_list


def _call_tg_method(method: str, params: dict) -> dict:
    """
    Получим данные от ТГ
    """
    resp = requests.get(
        f"{base_names.URL}{base_names.TOKEN}{method}",
        params
    )
    print(resp.json())
    result_list = resp.json()

    return result_list


def __download_file(document) -> requests.Response:
    """
    Скачивает файл
    """
    file_info = _call_tg_method("/getFile", {"file_id": document.file_id})
    resp: requests.Response = requests.get(
        f"https://api.telegram.org/file/bot{base_names.TOKEN}/{file_info.get('result').get('file_path')}"
    )
    resp.encoding = "utf-8"
    return resp


@router.put("/bot")
def send_message(**kwargs):
    """
    Метод отправки сообщений
    """
    method = '/sendMessage'
    response = requests.post(base_names.URL + base_names.TOKEN + method, data=kwargs)

    return response
