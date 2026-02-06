import json
from fastapi.responses import JSONResponse
import os

from datetime import datetime

import requests
from fastapi import APIRouter, Request

from .KeyBoard import KeyBoard
from .client import Client
from .database import insert, select, update
from bot_app.train.service import TrainService, TrainStatus
from .schemas.Response import Msg
from .operation.status_operations import BaseOperation
from . import base_names


router = APIRouter()
STARTED_TIME = datetime.now()
path = os.path.realpath("bot_app")


@router.post(r"/bot")
async def get_updates(request: Request):
    """
    Метод получения обновлений
    """
    text_msg = None
    key_board = None
    record = await request.json()
    print(record)
    if record:
        try:
            message = record.get("message") if record.get("message") else record.get("my_chat_member")
            client_obj = Client(message.get("chat").get("id"))

            msg: Msg = Msg(record.get("message"))
            client_id = msg.chat.id
            update_id = record.get("update_id")
            print(update_id)

            if not client_obj.update_id:
                insert.insert_client(msg, update_id)
                text_msg = base_names.WELCOME_MESSAGE
                key_board = base_names.StartButtons.buttons_array

            elif update_id <= client_obj.update_id:
                pass

            if client_obj.status:
                text_msg, key_board = BaseOperation(client_obj).call_method(msg)
            else:
                if msg.text == base_names.MAIN_MENU:
                    text_msg = base_names.BACK_TO_MAIN_MENU
                    key_board = base_names.StartButtons.buttons_array

                elif msg.text == base_names.StartButtons.set_trains:
                    text_msg = base_names.LETS_SET_TRAIN_FROM_LIST
                    key_board = base_names.TrainSettingsButton.buttons_array

                elif msg.text == base_names.TrainSettingsButton.delete:
                    text_msg = base_names.GOING_TO_DELETE
                    key_board = client_obj.trains
                    update.update_client_status(client_id, TrainStatus.DELETE)

                elif msg.text == base_names.TrainSettingsButton.change:
                    text_msg = base_names.GOING_TO_CHANGE
                    key_board = client_obj.trains
                    update.update_client_status(client_id, TrainStatus.CHANGE)

                elif msg.text == base_names.TrainSettingsButton.create:
                    text_msg = base_names.ENTER_TRAIN_NAME
                    key_board = base_names.StartButtons.buttons_array
                    update.update_client_status(client_id, TrainStatus.CREATE)

                elif msg.text == base_names.StartButtons.trains:
                    if client_obj.trains:
                        text_msg = base_names.CHOOSE_TRAIN_FROM_LIST
                        key_board = client_obj.trains
                    else:
                        text_msg = base_names.LETS_CREATE_TRAIN
                        key_board = []

                elif msg.text in client_obj.trains:
                    update.update_client_selected_entity(client_id, msg.text)
                    update.update_client_status(client_id, base_names.EXERCISE_READ_STATUS)
                    train_id = select.get_client_selected_entity(client_id)
                    key_board = exercise_service.ExerciseOperationService(client_id).get_exercises_name_by_train(
                        train_id
                    )
                    text_msg = base_names.SELECTED_TRAIN.format(TrainService(client_id).read(train_id))
                elif msg.text == base_names.StartButtons.statistic:
                    pass

            if text_msg is not None:
                print(f"Keyboard - {key_board}")
                print(f"Text_msg - {text_msg}")

                send_message(
                    chat_id=client_id,
                    text=text_msg,
                    reply_markup=json.dumps(
                        {'keyboard': KeyBoard(key_board).get_keyboard()})
                )

            update.update_client_last_update(client_id, update_id)

            return JSONResponse(
                content={
                    "ok": True,
                    "chat_id": client_id,
                    "text": text_msg,
                    "reply_markup": json.dumps({'keyboard': KeyBoard(key_board).get_keyboard()})
                }
            )
        except Exception as e:
            return JSONResponse(
                content={
                    "ok": True,
                    "text": f"{e}"
                }
            )
    return JSONResponse(
        content={
            "ok": True
        }
    )

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
