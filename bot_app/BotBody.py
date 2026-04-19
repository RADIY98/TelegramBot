import json
from fastapi.responses import JSONResponse
import os

from datetime import datetime

import requests
from fastapi import APIRouter, Request

from .KeyBoard import KeyBoard
from .application.dto.pressed_buttons import PressedButton
from .application.use_cases.handle_button import HandleButton
from .application.use_cases.handle_start_command import HandleStartCommand
from .domain.entities.user_entity import UserEntity
from .interface.telegram.mappers import request_to_button
from bot_app.interface.telegram.request_model import Msg
from . import base_names
from infrastructure.repositories.postgresql.user_repository import PostgresClientRepository


router = APIRouter()
STARTED_TIME = datetime.now()
path = os.path.realpath("bot_app")


@router.post(r"/bot")
async def get_updates(request: Request):
    """Метод получения обновлений"""
    record = await request.json()

    if record:
        message = record.get("message")
        user_id = message.get("chat").get("id")

        user_info: UserEntity = PostgresClientRepository().get_user_info(user_id)

        msg: Msg = Msg(record.get("message"))
        new_update_id: int = record.get("update_id")

        pushed_button: PressedButton = request_to_button(record)

        if pushed_button.text == "/start":
            HandleStartCommand(PostgresClientRepository).execute(user_id)

            PostgresClientRepository().change_update_id(user_id, new_update_id)

            return JSONResponse(
                content={
                    "ok": True,
                    "chat_id": user_id,
                    "text": base_names.WELCOME_MESSAGE,
                    "reply_markup": json.dumps({'keyboard': KeyBoard(base_names.StartButtons.buttons_array).get_keyboard()})
                }
            )

        if new_update_id <= user_info.update_id:
            return JSONResponse(
                content={
                    "ok": True
                }
            )

        button_strategy = HandleButton().execute(pushed_button)

        text_msg, key_board = button_strategy.get()

        return JSONResponse(
            content={
                "ok": True,
                "chat_id": user_id,
                "text": text_msg,
                "reply_markup": json.dumps({'keyboard': KeyBoard(key_board).get_keyboard()})
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
