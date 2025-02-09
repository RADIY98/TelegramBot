import asyncio
import json
import os

from datetime import datetime

import requests
from fastapi import APIRouter
from bot_app.KeyBoard import KeyBoard
from bot_app.trains.utils import parse_file
from . import base_names
from bot_app.database import insert, select, delete, update
from .schemas.Response import Msg
from .trains import get_all_trains_for_keyboard, get_all_exercises_for_keyboard, TrainOperations

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
    """
    Метод получения обновлений
    """
    text_msg = None
    key_board = None
    response_list = _get_http_request()
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

            if client_status in base_names.TrainStatus.status_array:
                text_msg, key_board = TrainOperations(client_id).get_operation(client_status, msg.text)
            else:
                trains = get_all_trains_for_keyboard(client_id)

                if msg.text == "/start":
                    continue
                    text_msg = msg.text
                    key_board = base_names.StartButtons.buttons_array
                    insert.insert_client(msg, update_id)
                elif msg.text == base_names.MAIN_MENU:
                    text_msg = msg.text
                    key_board = base_names.StartButtons.buttons_array

                elif msg.text == base_names.StartButtons.set_trains:
                    text_msg = msg.text
                    key_board = base_names.TrainSettingsButton.buttons_array

                elif msg.text == base_names.TrainSettingsButton.delete:
                    text_msg = msg.text
                    key_board = trains
                    update.update_client_status(client_id, base_names.TrainStatus.DELETE_TRAIN)

                elif msg.text == base_names.TrainSettingsButton.change:
                    text_msg = msg.text
                    key_board = trains
                    update.update_client_status(client_id, base_names.TrainStatus.CHANGE_TRAIN)

                elif msg.text == base_names.TrainSettingsButton.create:
                    text_msg = "Введите название тренировки"
                    key_board = base_names.StartButtons.buttons_array
                    update.update_client_status(client_id, base_names.TrainStatus.CREATE_TRAIN)

                elif msg.text == base_names.StartButtons.trains:
                    if trains:
                        text_msg = msg.text
                        key_board = trains
                    else:
                        text_msg = "Давайте добавим тренировку"
                        key_board = None

                elif msg.text in trains[:-1]:
                    text_msg = get_all_exercises_for_keyboard(client_id, msg.text)
                    key_board = trains

                elif msg.text == base_names.StartButtons.statistic:
                    pass
                elif msg.document is not None:
                    file = __download_file(msg.document)
                    train_obj = parse_file(file)
                    delete.delete_all_trains(client_id)
                    for train_name, train in train_obj.items():
                        insert.insert_train(train_name, client_id, train)
            if text_msg is not None:
                send_message(
                    chat_id=client_id,
                    text=text_msg,
                    reply_markup=json.dumps(
                        {'keyboard': KeyBoard(key_board).get_keyboard()})
                )

            res = update.update_client_last_update(client_id, update_id)
            print(res)
            send_message(chat_id=client_id, text=f"{client_id}, {update_id}")

    return response_list


def _get_http_request() -> dict:
    """
    Получим данные от ТГ
    """
    method = '/getUpdates'
    params = {'limit': 100, "offset": base_names.global_id + 10}
    resp = requests.get(
        base_names.URL + base_names.TOKEN + method,
        params
    )
    result_list = resp.json()['result']

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
